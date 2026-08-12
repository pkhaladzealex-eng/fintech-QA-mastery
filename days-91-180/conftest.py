
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
