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

def test_payment_checkout(driver):
    wait = WebDriverWait(driver,10)

    # Open  site
    utils.open_site(driver)
    assert "STORE" in driver.title

    # Choose the product
    utils.click_product_by_name(driver, wait, "Sony vaio i5")
    assert "prod.html" in driver.current_url

    # Add product to cart
    utils.add_product_to_cart(driver, wait)

    # Navigate to cart
    utils.navigate_to_cart(driver, wait)

    # Click to place order
    utils.click_place_order(driver, wait)

    # Assert: Verify modal window is displayed by checking its title
    modal_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='orderModal']//div[@class='modal-header']"))
    )
    assert modal_title.is_displayed()

    # Fill checkout form
    utils.fill_checkout_form(driver,wait,"Alex","Czechia", "Prague","1234123412341234","8","2026")

    # Verify success message
    final_modal_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='Thank you for your purchase!']"))
    )
    assert final_modal_title.is_displayed()

    # Screenshot

    driver.save_screenshot("demoblaze_purchase.png")


