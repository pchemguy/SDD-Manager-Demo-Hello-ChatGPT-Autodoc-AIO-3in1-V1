import os
from pathlib import Path
import pytest
from playwright.sync_api import expect
ROOT=Path(__file__).resolve().parents[2]
@pytest.fixture
def app(page):
    path=Path(os.environ.get('HELLO_UI_ROOT',str(ROOT/'build/browser')))/'index.html'
    assert path.is_file(),'Deliverable browser index.html is missing'
    page.goto(path.as_uri());return page

def test_immediate_exclusive_selection_and_keyboard(app):
    message=app.get_by_role('heading',name='Hello World')
    expect(message).to_have_css('color','rgb(255, 0, 0)')
    assert app.get_by_role('radio').count()==3
    for value,rgb in [('blue','0, 0, 255'),('green','0, 128, 0'),('red','255, 0, 0'),('red','255, 0, 0')]:
        app.get_by_text(value,exact=True).click()
        expect(app.get_by_role('radio',name=value,exact=True)).to_be_checked()
        assert app.locator('input:checked').count()==1
        expect(message).to_have_css('color',f'rgb({rgb})')
    app.get_by_role('radio',name='red',exact=True).focus();app.keyboard.press('ArrowDown')
    expect(app.get_by_role('radio',name='blue',exact=True)).to_be_checked()
    expect(message).to_have_css('color','rgb(0, 0, 255)')
    app.keyboard.press('Space');expect(message).to_have_text('Hello World')
    assert app.evaluate('document.activeElement.matches(":focus-visible")')

def test_responsive_zoom_and_visible_glyphs(app,browser):
    _,name=browser
    for width in [200,320,1200]:
        for zoom in [1,2]:
            app.set_viewport_size({'width':width,'height':220})
            app.evaluate('(z)=>document.documentElement.style.zoom=z',str(zoom))
            assert app.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
            boxes=[app.get_by_role('radio',name=n,exact=True).bounding_box() for n in ['red','blue','green']]
            assert boxes[0]['y']<boxes[1]['y']<boxes[2]['y']
            app.get_by_text('green',exact=True).click()
            expect(app.get_by_role('heading')).to_have_css('color','rgb(0, 128, 0)')
    app.evaluate('document.documentElement.style.zoom="1"');app.set_viewport_size({'width':320,'height':350})
    app.get_by_text('red',exact=True).click();out=ROOT/'.test-results'/f'app-{name}.png'
    assert len(app.screenshot(path=str(out),full_page=True))>1500

def test_restore_independence_and_listener_disposal(app):
    app.get_by_text('blue',exact=True).click()
    other=app.context.new_page();other.goto(app.url)
    expect(other.get_by_role('radio',name='red',exact=True)).to_be_checked()
    expect(app.get_by_role('radio',name='blue',exact=True)).to_be_checked();other.close()
    app.reload();expect(app.get_by_role('radio',name='red',exact=True)).to_be_checked()
    app.get_by_text('green',exact=True).click()
    app.goto('about:blank');app.go_back()
    expect(app.get_by_role('radio',name='red',exact=True)).to_be_checked()
    app.get_by_text('green',exact=True).click()
    app.evaluate('dispatchEvent(new PageTransitionEvent("pageshow",{persisted:true}))')
    expect(app.get_by_role('radio',name='red',exact=True)).to_be_checked()
    app.evaluate('window.HelloColorApp.mount(document).dispose();window.HelloColorApp.mount(document).reset()')
    app.get_by_text('blue',exact=True).click();expect(app.get_by_role('heading')).to_have_css('color','rgb(0, 0, 255)')

def test_static_subpath(page,tmp_path):
    import http.server,threading,functools,shutil
    target=tmp_path/'nested'/'hello';target.parent.mkdir()
    shutil.copytree(ROOT/'build/browser',target)
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(tmp_path))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        page.goto(f'http://127.0.0.1:{server.server_port}/nested/hello/index.html')
        page.get_by_text('blue',exact=True).click()
        expect(page.get_by_role('heading')).to_have_css('color','rgb(0, 0, 255)')
    finally:
        server.shutdown();server.server_close();thread.join(timeout=5)
