import subprocess,json
from pathlib import Path
from playwright.sync_api import expect
ROOT=Path(__file__).resolve().parents[2]
def test_firefox_build_manifest_and_local_assets():
    result=subprocess.run(['node','scripts/build.mjs','firefox'],cwd=ROOT,capture_output=True,text=True,timeout=15)
    assert result.returncode==0,result.stderr
    m=json.loads((ROOT/'build/firefox/manifest.json').read_text())
    assert m['manifest_version']==3 and m['version']==json.loads((ROOT/'package.json').read_text())['version']
    assert m['browser_specific_settings']['gecko']['strict_min_version']=='140.0'
    assert m['browser_specific_settings']['gecko']['id']=='hello-world@pchemguy'
    assert not m.get('permissions') and not m.get('host_permissions')
    assert (ROOT/'build/firefox'/m['sidebar_action']['default_panel']).exists()
    for n in ['index.html','app.js','styles.css','bootstrap.js']:
        assert (ROOT/'build/firefox'/n).read_bytes()==(ROOT/'app'/n).read_bytes()

def test_firefox_document_recreation_is_fresh(page):
    url=(ROOT/'build/firefox/index.html').as_uri();page.goto(url)
    page.get_by_text('green',exact=True).click()
    page.set_viewport_size({'width':200,'height':350})
    expect(page.get_by_role('heading')).to_have_css('color','rgb(0, 128, 0)')
    page.goto('about:blank');page.goto(url)
    expect(page.get_by_role('radio',name='red',exact=True)).to_be_checked()
