import os,subprocess,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_host_startup_resources_and_security(tmp_path):
    source=Path(os.environ.get('HELLO_DESKTOP_ENTRY',str(ROOT/'build/desktop/app/main.cjs')))
    target=tmp_path/'package with spaces'
    shutil.copytree(source.parent,target)
    result=subprocess.run(['node','tests/fixtures/desktop-host.cjs',str(target/'main.cjs')],cwd=ROOT,capture_output=True,text=True,timeout=15)
    assert result.returncode==0,result.stdout+result.stderr
