import subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_chromium_lifecycle_worker():
    result=subprocess.run(['node','tests/fixtures/chromium-worker.cjs'],cwd=ROOT,capture_output=True,text=True,timeout=15)
    assert result.returncode==0,result.stdout+result.stderr

def test_chromium_manifest():
    m=json.loads((ROOT/'build/chromium/manifest.json').read_text())
    assert m['manifest_version']==3 and m['minimum_chrome_version']=='142'
    assert m['permissions']==['sidePanel'] and not m.get('host_permissions')
    assert m['version']==json.loads((ROOT/'package.json').read_text())['version']
    assert (ROOT/'build/chromium'/m['side_panel']['default_path']).is_file()

def test_chromium_panel_reopen_duplicate_stale_and_reconnect(page):
    from playwright.sync_api import expect
    page.add_init_script('''window.TestPorts=[];window.chrome={windows:{getCurrent:async()=>({id:11})},runtime:{id:'own',connect:()=>{const message=[],disconnect=[];const p={sent:[],onMessage:{addListener:f=>message.push(f)},onDisconnect:{addListener:f=>disconnect.push(f)},postMessage:m=>p.sent.push(m),emit:m=>message.forEach(f=>f(m)),disconnect:()=>disconnect.forEach(f=>f())};window.TestPorts.push(p);document.documentElement?.setAttribute('data-ports',String(TestPorts.length));return p;}}};''')
    page.goto((ROOT/'build/chromium/index.html').as_uri())
    expect(page.locator('html')).to_have_attribute('data-ports','1')
    def send(token,seq,reset=True,window=11,index=-1):
        page.evaluate('(m)=>TestPorts.at(m.index).emit(m.value)',{'index':index,'value':{'type':'session','windowId':window,'token':token,'sequence':seq,'reset':reset}})
    send('one',1)
    page.get_by_text('blue',exact=True).click();send('one',2)
    expect(page.get_by_role('heading')).to_have_css('color','rgb(0, 0, 255)')
    page.evaluate("TestPorts[0].emit({type:'session',windowId:11,token:'bogus',sequence:999,reset:false})")
    expect(page.get_by_role('heading')).to_have_css('color','rgb(0, 0, 255)')
    send('other',100,True,99);send('two',3)
    expect(page.get_by_role('radio',name='red',exact=True)).to_be_checked()
    page.get_by_text('green',exact=True).click();send('one',4)
    expect(page.get_by_role('heading')).to_have_css('color','rgb(0, 128, 0)')
    page.evaluate('TestPorts[0].disconnect()');expect(page.locator('html')).to_have_attribute('data-ports','2')
    send('two',1,False);send('three',8,True,11,0)
    expect(page.get_by_role('heading')).to_have_css('color','rgb(0, 128, 0)')
    send('three',2)
    expect(page.get_by_role('radio',name='red',exact=True)).to_be_checked()
