"""Allowlisted, deterministic release archives and verification."""
import argparse,hashlib,json,os,pathlib,re,stat,subprocess,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
COMMON=['index.html','app.js','styles.css','bootstrap.js','version.json']
def validate_members(names):
    for name in names:
        p=pathlib.PurePosixPath(name)
        if not name or name.startswith('/') or '\\' in name or ':' in name or '..' in p.parts:
            raise ValueError('Unsafe archive member')
    return names

def version():return json.loads((ROOT/'package.json').read_text())['version']
def run(*args):subprocess.run(args,cwd=ROOT,check=True,timeout=60)
def archive_name(kind):return f'hello-world-{version()}-{kind}.zip'
def kinds(phase):
    if phase!=1:raise ValueError('Platform phase is not implemented')
    return ['browser']
def write_zip(target,files):
    validate_members(list(files))
    target.parent.mkdir(parents=True,exist_ok=True);temporary=target.with_suffix('.partial')
    try:
        with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name,path in sorted(files.items()):
                info=zipfile.ZipInfo(name,date_time=(2020,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,path.read_bytes())
        os.replace(temporary,target)
    finally:
        if temporary.exists():temporary.unlink()
def files_for(kind):
    out=ROOT/'build'/kind
    files={n:out/n for n in COMMON}
    files.update({'INSTALL.md':ROOT/'docs/INSTALL.md','LICENSE':ROOT/'LICENSE'})
    for p in files.values():
        if not p.is_file() or p.is_symlink():raise ValueError('Missing or unsafe source file: '+p.name)
    return files

def verify_archive(path,kind):
    with zipfile.ZipFile(path) as z:
        names=z.namelist();validate_members(names)
        if len(names)!=len(set(names)):raise ValueError('Duplicate archive member')
        if any(stat.S_ISLNK(i.external_attr>>16) for i in z.infolist()):raise ValueError('Archive symlink')
        required=set(COMMON+['INSTALL.md','LICENSE'])
        if set(names)!=required:raise ValueError('Unexpected or missing archive members')
        metadata=json.loads(z.read('version.json'))
        if metadata['version']!=version() or metadata['platform']!=kind:raise ValueError('Archive version/platform mismatch')
        if not re.fullmatch('[0-9a-f]{40}',metadata['sourceRevision']):raise ValueError('Invalid source identity')
        for n in ['index.html','app.js','styles.css','bootstrap.js']:
            if z.read(n)!=(ROOT/'app'/n).read_bytes():raise ValueError('Shared asset mismatch: '+n)
        if z.testzip():raise ValueError('Archive CRC failure')
        return metadata

def release(phase):
    dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    for kind in kinds(phase):
        run('node','scripts/build.mjs',kind)
        write_zip(dist/archive_name(kind),files_for(kind))
    (dist/'INSTALL.md').write_bytes((ROOT/'docs/INSTALL.md').read_bytes())
    (dist/'SHA256SUMS').write_text(''.join(hashlib.sha256((dist/archive_name(k)).read_bytes()).hexdigest()+'  '+archive_name(k)+'\n' for k in kinds(phase)))
    verify(phase)

def verify(phase):
    dist=ROOT/'dist';expected={archive_name(k) for k in kinds(phase)}
    actual={p.name for p in dist.glob('hello-world-'+version()+'-*.zip')}
    if actual!=expected:raise ValueError('Incomplete or unexpected cumulative archive set')
    sums=dict(line.split('  ')[::-1] for line in (dist/'SHA256SUMS').read_text().splitlines())
    if set(sums)!=expected:raise ValueError('Checksum inventory mismatch')
    for kind in kinds(phase):
        path=dist/archive_name(kind);verify_archive(path,kind)
        if hashlib.sha256(path.read_bytes()).hexdigest()!=sums[path.name]:raise ValueError('Archive checksum mismatch')
    print('Verified',len(expected),'final platform archive(s)',version())

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['release','verify']);parser.add_argument('--phase',type=int,required=True);args=parser.parse_args()
    try:globals()[args.command](args.phase)
    except (ValueError,OSError,zipfile.BadZipFile,KeyError,json.JSONDecodeError) as e:parser.exit(1,str(e)+'\n')
