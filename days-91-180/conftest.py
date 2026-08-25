import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def log_test_info(request):
    """Log test start/end automatically"""
    print(f"\n[START] {request.node.name}")
    yield
    print(f"[END] {request.node.name}")

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup test data after each test"""
    yield
    print("\n[Cleanup] Test completed - Stripe test data will auto-clear")

from selenium.webdriver.chrome.options import Options

def get_browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)

@pytest.fixture(autouse=True)
def failure_artifacts(request, browser):
    yield
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        browser.save_screenshot(f"failure_{request.node.name}.png")
        with open(f"failure_{request.node.name}.html", "w") as f:
            f.write(browser.page_source)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)