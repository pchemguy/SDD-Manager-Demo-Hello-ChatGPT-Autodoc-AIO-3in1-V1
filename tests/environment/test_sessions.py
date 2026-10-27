from pathlib import Path
from playwright.sync_api import expect
def test_repeated_input_render_teardown(browser):
    b,name=browser
    for cycle in range(2):
        context=b.new_context(viewport={"width":320,"height":220})
        p=context.new_page();p.set_default_timeout(5000)
        p.set_content('<p id="message" style="font:bold 28px sans-serif;color:red">Environment probe</p><button onclick="document.querySelector(\'#message\').style.color=\'blue\'">Change</button>')
        p.get_by_role("button",name="Change").click()
        expect(p.locator("#message")).to_have_css("color","rgb(0, 0, 255)")
        target=Path(".test-results")/f"environment-{name}-{cycle}.png";target.parent.mkdir(exist_ok=True)
        assert len(p.screenshot(path=str(target)))>1000
        context.close()
