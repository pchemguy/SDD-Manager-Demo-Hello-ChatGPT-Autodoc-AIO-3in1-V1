import importlib.util,json,zipfile,hashlib,subprocess
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('pack',ROOT/'scripts/package.py');pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
@pytest.mark.parametrize('bad',['../secret','/absolute','C:/secret','dir/../../secret','dir\\secret'])
def test_reject_unsafe_paths(bad):
    with pytest.raises(ValueError):pack.validate_members([bad])
def test_valid_root_members():
    assert pack.validate_members(['index.html','assets/style.css'])==['index.html','assets/style.css']

def test_actual_archive_integrity_and_rejections(tmp_path):
    source=ROOT/'dist'/pack.archive_name('browser')
    if not source.exists():
        subprocess.run(['python','scripts/package.py','release','--phase',str(json.loads((ROOT/'package.json').read_text()).get('deliveryPhase',1))],cwd=ROOT,check=True,timeout=120)
    pack.verify_archive(source,'browser')
    with zipfile.ZipFile(source) as z:files={n:z.read(n) for n in z.namelist()}
    files['gh.tkn']=b'synthetic-not-a-secret'
    bad=tmp_path/'unexpected.zip'
    with zipfile.ZipFile(bad,'w') as z:
        for n,b in files.items():z.writestr(n,b)
    with pytest.raises(ValueError,match='Unexpected'):pack.verify_archive(bad,'browser')
    del files['gh.tkn'];del files['app.js']
    with zipfile.ZipFile(bad,'w') as z:
        for n,b in files.items():z.writestr(n,b)
    with pytest.raises(ValueError,match='missing'):pack.verify_archive(bad,'browser')

def test_credentials_rejected_even_when_canonical_assets_match(tmp_path,monkeypatch):
    source=ROOT/'dist'/pack.archive_name('browser')
    with zipfile.ZipFile(source) as z:files={n:z.read(n) for n in z.namelist()}
    files['app.js']+=b'\nconst secret="github_pat_synthetic12345678901234567890";'
    (tmp_path/'app').mkdir();(tmp_path/'package.json').write_bytes((ROOT/'package.json').read_bytes())
    for n in ['index.html','app.js','styles.css','bootstrap.js']:(tmp_path/'app'/n).write_bytes(files[n])
    archive=tmp_path/'credential.zip'
    with zipfile.ZipFile(archive,'w') as z:
        for n,b in files.items():z.writestr(n,b)
    monkeypatch.setattr(pack,'ROOT',tmp_path)
    with pytest.raises(ValueError,match='Credential'):pack.verify_archive(archive,'browser')

def test_cumulative_sources_must_agree(tmp_path,monkeypatch):
    (tmp_path/'package.json').write_text('{"version":"0.2.0"}')
    dist=tmp_path/'dist';dist.mkdir()
    names=['hello-world-0.2.0-browser.zip','hello-world-0.2.0-windows-x64.zip']
    for name in names:(dist/name).write_bytes(b'validated archive fixture')
    (dist/'SHA256SUMS').write_text(''.join(hashlib.sha256((dist/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in names))
    monkeypatch.setattr(pack,'ROOT',tmp_path)
    monkeypatch.setattr(pack,'verify_archive',lambda path,kind:{'sourceRevision':('a' if kind=='browser' else 'b')*40})
    with pytest.raises(ValueError,match='source'):pack.verify(2)

def test_final_platform_set_is_cumulative():
    assert pack.kinds(3)==['browser','windows-x64','chromium-dev','firefox-dev']

@pytest.mark.parametrize('platform',['chromium','firefox'])
def test_extension_archive_rejects_new_storage_capability(platform,tmp_path,monkeypatch):
    path=ROOT/'dist'/pack.archive_name(platform+'-dev')
    pack.verify_extension(path,platform)
    with zipfile.ZipFile(path) as z:files={n:z.read(n) for n in z.namelist()}
    manifest=json.loads(files['manifest.json']);manifest['permissions']=['storage'];files['manifest.json']=json.dumps(manifest).encode()
    folder=tmp_path/'platforms'/platform;folder.mkdir(parents=True)
    template=dict(manifest);del template['version'];(folder/'manifest.json').write_text(json.dumps(template))
    (tmp_path/'package.json').write_bytes((ROOT/'package.json').read_bytes())
    bad=tmp_path/'bad.zip'
    with zipfile.ZipFile(bad,'w') as z:
        for n,b in files.items():z.writestr(n,b)
    monkeypatch.setattr(pack,'ROOT',tmp_path)
    with pytest.raises(ValueError,match='contract mismatch'):pack.verify_extension(bad,platform)
