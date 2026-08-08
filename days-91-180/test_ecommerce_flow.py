import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import ecommerce_utils as utils

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_add_product_to_cart(driver):
    wait = WebDriverWait(driver, 10)

    # Setup: Open site
    utils.open_site(driver)
    assert "STORE" in driver.title

    # Execute: Click first product
    first_product = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.card-block h4 a")
    ))
    first_product.click()
    assert "prod.html" in driver.current_url

    # Execute: Add to cart and handle alert inside utility function
    utils.add_product_to_cart(driver, wait)


    # Execute: Navigate to cart
    utils.navigate_to_cart(driver, wait)

    # Assert: Verify cart page
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "table.table")
    ))
    assert "cart" in driver.current_url

    # Screenshot
    driver.save_screenshot("demoblaze_cart.png")

def test_add_product_to_cart_and_remove(driver):
    wait = WebDriverWait(driver, 10)

    # Setup: Open site
    utils.open_site(driver)
    assert "STORE"  in driver.title

    # Execute: Click the product
    utils.click_product_by_name(driver, wait, "HTC One M9")
    assert "prod.html" in driver.current_url

    # Execute: Add to cart and handle alert inside utility function
    utils.add_product_to_cart(driver, wait)

    # Execute: Navigate to cart
    utils.navigate_to_cart(driver, wait)

    # Assert: Verify cart page
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Cart']"))
    )
    assert "cart.html" in driver.current_url

    # Find the item on the cart
    cart_item = wait.until(
        EC.presence_of_element_located((By.XPATH,"//td[normalize-space()='HTC One M9']"))
    )
    assert cart_item.is_displayed()
    print("Product verified!")

    # Execute: Remove item
    utils.remove_product_from_cart(driver, wait)

    # Verify product is removed from cart
    wait.until(EC.staleness_of(cart_item))

    # Assertion: Product removed from cart
    remaining_items = driver.find_elements(By.XPATH, "//td[contains(text(), 'HTC One M9')]")
    assert len(remaining_items) == 0, "Item was not removed from cart!"

    # Screenshot
    driver.save_screenshot("demoblaze_cart_01.png")







