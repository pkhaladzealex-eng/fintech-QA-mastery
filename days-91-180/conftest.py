
import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    """Single browser instance for entire test session"""
    driver = webdriver.Chrome()
    driver.maximize_window()
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