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
    subprocess.run(['python','scripts/package.py','release','--phase','1'],cwd=ROOT,check=True,timeout=30)
    source=ROOT/'dist'/pack.archive_name('browser')
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
