
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument("--headless=new")  # CI გარემოსთვის აუცილებელია
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

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
    # Note: Stripe test data auto-clears after 30 days
    # In production, we'd delete created resources here
    print("\n[Cleanup] Test completed - Stripe test data will auto-clear")