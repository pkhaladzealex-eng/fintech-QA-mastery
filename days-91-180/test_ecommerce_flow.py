import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()


def test_add_product_to_cart(driver):
    wait = WebDriverWait(driver, 10)

    # Setup: Open site
    driver.get("https://www.demoblaze.com/")
    assert "STORE" in driver.title

    # Execute: Click first product
    first_product = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.card-block h4 a")
    ))
    first_product.click()
    assert "prod.html" in driver.current_url

    # Execute: Add to cart
    add_to_cart = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.btn-success")
    ))
    add_to_cart.click()

    # Execute: Handle alert
    alert = wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Product added"
    alert.accept()

    # Execute: Navigate to cart
    cart_link = wait.until(EC.element_to_be_clickable(
        (By.ID, "cartur")
    ))
    cart_link.click()

    # Assert: Verify cart page
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "table.table")
    ))
    assert "cart" in driver.current_url
    print("Cart verified!")

    # Screenshot
    driver.save_screenshot("demoblaze_cart.png")