import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
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