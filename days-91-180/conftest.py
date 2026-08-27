import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def _build_chrome_options():
    """Single source of truth for Chrome options used in CI (headless-safe)."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    return options


@pytest.fixture(scope="function")
def browser():
    """Fresh browser per test - no cross-test session/cookie pollution."""
    driver = webdriver.Chrome(options=_build_chrome_options())
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Log test start/end automatically for every test (browser or API)."""
    print(f"\n[START] {request.node.name}")
    yield
    print(f"[END] {request.node.name}")


@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup test data after each test."""
    yield
    print("\n[Cleanup] Test completed - Stripe test data will auto-clear")


@pytest.fixture(autouse=True)
def failure_artifacts(request):
    """
    Save screenshot + page source ONLY for tests that actually use the
    `browser` fixture. Does NOT force Chrome to launch for API-only tests
    (e.g. stripe-api-testing).

    IMPORTANT: we pull in the `browser` fixture (via request.getfixturevalue)
    BEFORE yield - i.e. during setup, not teardown. This tells pytest that
    failure_artifacts depends on browser, so on teardown pytest tears this
    fixture down BEFORE calling browser's own teardown (driver.quit()).
    Without this, browser.quit() was running first and our screenshot call
    hit a closed/dead driver session (ConnectionRefused).
    """
    uses_browser = "browser" in request.fixturenames
    driver = request.getfixturevalue("browser") if uses_browser else None

    yield

    failed = getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed
    if failed and driver is not None:
        driver.save_screenshot(f"failure_{request.node.name}.png")
        with open(f"failure_{request.node.name}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose test result (pass/fail) to fixtures via item.rep_<phase>."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)