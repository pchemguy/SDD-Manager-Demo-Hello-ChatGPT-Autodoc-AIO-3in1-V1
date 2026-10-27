"""Allowlisted, deterministic release archives and verification."""
import argparse,hashlib,json,os,pathlib,re,stat,subprocess,zipfile,shutil,struct,time,urllib.request
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
    if phase not in [1,2]:raise ValueError('Platform phase is not implemented')
    return ['browser']+(['windows-x64'] if phase>=2 else [])
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
    if kind=='windows-x64':return windows_files()
    out=ROOT/'build'/kind
    files={n:out/n for n in COMMON}
    files.update({'INSTALL.md':ROOT/'docs/INSTALL.md','LICENSE':ROOT/'LICENSE'})
    for p in files.values():
        if not p.is_file() or p.is_symlink():raise ValueError('Missing or unsafe source file: '+p.name)
    return files

def verify_archive(path,kind):
    if kind=='windows-x64':return verify_windows(path)
    with zipfile.ZipFile(path) as z:
        names=z.namelist();validate_members(names)
        if len(names)!=len(set(names)):raise ValueError('Duplicate archive member')
        if any(stat.S_ISLNK(i.external_attr>>16) for i in z.infolist()):raise ValueError('Archive symlink')
        required=set(COMMON+['INSTALL.md','LICENSE'])
        if set(names)!=required:raise ValueError('Unexpected or missing archive members')
        for n in names:
            if re.search(rb'(github_pat_[A-Za-z0-9_]{10,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',z.read(n)):
                raise ValueError('Credential material in archive')
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
        if kind=='windows-x64':assemble_windows()
        else:run('node','scripts/build.mjs',kind)
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


def verify_download(path,expected):
    with path.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
    if actual!=expected:raise ValueError('Runtime checksum mismatch')

def runtime_zip():
    config=json.loads((ROOT/'toolchain.json').read_text())
    cache=ROOT/'.tools/electron';cache.mkdir(parents=True,exist_ok=True)
    target=cache/('electron-v'+config['electronVersion']+'-win32-x64.zip')
    if not target.exists():
        temporary=target.with_suffix('.download');start=time.monotonic()
        try:
            with urllib.request.urlopen(config['archiveURL'],timeout=60) as response,temporary.open('wb') as f:
                while chunk:=response.read(1024*1024):
                    f.write(chunk)
                    if time.monotonic()-start>180:raise TimeoutError('Runtime download deadline')
            if temporary.stat().st_size!=config['archiveSize']:raise ValueError('Runtime download size mismatch')
            verify_download(temporary,config['archiveSHA256']);os.replace(temporary,target)
        finally:
            if temporary.exists():temporary.unlink()
    verify_download(target,config['archiveSHA256'])
    return target

def runtime_entries():
    with zipfile.ZipFile(runtime_zip()) as z:
        validate_members(z.namelist())
        if len(z.namelist())!=len(set(z.namelist())):raise ValueError('Duplicate runtime member')
        if any(stat.S_ISLNK(i.external_attr>>16) for i in z.infolist()):raise ValueError('Runtime symlink')
        names={n for n in z.namelist() if not n.endswith('/') and n!='resources/default_app.asar'}
        if not {'electron.exe','resources.pak','icudtl.dat','LICENSE','LICENSES.chromium.html'}<=names:raise ValueError('Incomplete official runtime')
        return names

def assemble_windows():
    entries=runtime_entries();out=ROOT/'build/windows-x64'
    run('node','scripts/build.mjs','desktop')
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True)
    with zipfile.ZipFile(runtime_zip()) as z:
        for name in sorted(entries):
            dest=out/('HelloWorld.exe' if name=='electron.exe' else name);dest.parent.mkdir(parents=True,exist_ok=True)
            with z.open(name) as source,dest.open('wb') as target:shutil.copyfileobj(source,target,1024*1024)
    shutil.copytree(ROOT/'build/desktop/app',out/'resources/app')

def windows_files():
    out=ROOT/'build/windows-x64';files={p.relative_to(out).as_posix():p for p in out.rglob('*') if p.is_file()}
    if any(p.is_symlink() for p in out.rglob('*')):raise ValueError('Unsafe staged Windows file')
    files['INSTALL.md']=ROOT/'docs/INSTALL.md'
    return files

def verify_windows(path):
    runtime=runtime_entries();expected={('HelloWorld.exe' if n=='electron.exe' else n) for n in runtime}
    appnames=['package.json','main.cjs','LICENSE']+['renderer/'+n for n in COMMON]
    expected|={'resources/app/'+n for n in appnames};expected.add('INSTALL.md')
    with zipfile.ZipFile(path) as z:
        names=z.namelist();validate_members(names)
        if set(names)!=expected or len(names)!=len(set(names)):raise ValueError('Incomplete or unexpected Windows package inventory')
        if any(stat.S_ISLNK(i.external_attr>>16) for i in z.infolist()):raise ValueError('Windows package symlink')
        exe=z.read('HelloWorld.exe');offset=struct.unpack_from('<I',exe,0x3c)[0]
        if exe[:2]!=b'MZ' or exe[offset:offset+4]!=b'PE\0\0' or struct.unpack_from('<H',exe,offset+4)[0]!=0x8664:raise ValueError('Windows executable is not x64 PE')
        meta=json.loads(z.read('resources/app/renderer/version.json'));app=json.loads(z.read('resources/app/package.json'))
        if meta['version']!=version() or app['version']!=version() or app['main']!='main.cjs':raise ValueError('Desktop metadata mismatch')
        if z.read('resources/app/main.cjs')!=(ROOT/'platforms/electron/main.cjs').read_bytes():raise ValueError('Desktop entry mismatch')
        for name in COMMON[:4]:
            if z.read('resources/app/renderer/'+name)!=(ROOT/'app'/name).read_bytes():raise ValueError('Desktop shared asset mismatch')
        for name in appnames:
            data=z.read('resources/app/'+name)
            if re.search(rb'(github_pat_[A-Za-z0-9_]{10,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',data):raise ValueError('Credential material in desktop package')
        with zipfile.ZipFile(runtime_zip()) as original:
            for name in runtime:
                if z.read('HelloWorld.exe' if name=='electron.exe' else name)!=original.read(name):raise ValueError('Official runtime content mismatch')
        if z.testzip():raise ValueError('Windows archive CRC failure')
        return meta

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['release','verify']);parser.add_argument('--phase',type=int,required=True);args=parser.parse_args()
    try:globals()[args.command](args.phase)
    except (ValueError,OSError,zipfile.BadZipFile,KeyError,json.JSONDecodeError) as e:parser.exit(1,str(e)+'\n')
