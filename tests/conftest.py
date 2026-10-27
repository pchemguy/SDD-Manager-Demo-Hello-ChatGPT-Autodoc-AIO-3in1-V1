import os
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH",str(ROOT/".tools/browsers"))
@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p: yield p
@pytest.fixture(params=["chromium","firefox"])
def browser(request,pw):
    options={"headless":True,"timeout":10000}
    if request.param=="firefox" and os.environ.get("HELLO_FIREFOX_UNSANDBOXED")=="1":
        options["env"]={**os.environ,"MOZ_DISABLE_CONTENT_SANDBOX":"1"}
    b=getattr(pw,request.param).launch(**options)
    yield b,request.param
    b.close()
@pytest.fixture
def page(browser):
    b,name=browser
    context=b.new_context(viewport={"width":320,"height":400})
    p=context.new_page();p.set_default_timeout(5000);p.set_default_navigation_timeout(10000)
    yield p
    context.close()
