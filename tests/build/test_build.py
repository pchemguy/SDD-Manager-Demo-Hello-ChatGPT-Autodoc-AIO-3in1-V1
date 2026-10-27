import subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_builder_preserves_canonical_assets():
    subprocess.run(['node','scripts/build.mjs','browser'],cwd=ROOT,check=True,timeout=15)
    for n in ['index.html','app.js','styles.css','bootstrap.js']:
        assert (ROOT/'build/browser'/n).read_bytes()==(ROOT/'app'/n).read_bytes()
    assert json.loads((ROOT/'build/browser/version.json').read_text())['version']==json.loads((ROOT/'package.json').read_text())['version']
def test_unknown_build_target_fails():
    result=subprocess.run(['node','scripts/build.mjs','unknown'],cwd=ROOT,capture_output=True,timeout=15)
    assert result.returncode!=0
