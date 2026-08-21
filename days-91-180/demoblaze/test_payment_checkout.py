import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import utils
from . import config as cfg


def test_payment_checkout(browser):
    wait = WebDriverWait(browser,10)

    # Open  site
    utils.open_site(browser)
    assert "STORE" in browser.title

    # Choose the product
    utils.click_product_by_name(browser, wait, "Sony vaio i5")
    assert "prod.html" in browser.current_url

    # Add product to cart
    utils.add_product_to_cart(browser, wait)

    # Navigate to cart
    utils.navigate_to_cart(browser, wait)

    # Click to place order
    utils.click_place_order(browser, wait)

    # Assert: Verify modal window is displayed by checking its title
    modal_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='orderModal']//div[@class='modal-header']"))
    )
    assert modal_title.is_displayed()

    # Fill checkout form
    utils.fill_checkout_form(browser,wait,"Alex","Czechia", "Prague","1234123412341234","8","2026")

    # Verify success message
    final_modal_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='Thank you for your purchase!']"))
    )
    assert final_modal_title.is_displayed()

    # Screenshot

    browser.save_screenshot("demoblaze_purchase.png")

#Second test with invalid card
def test_checkout_with_invalid_card(browser):
    wait = WebDriverWait(browser,10)


    utils.setup_and_add_to_cart(browser, wait, "HTC One M9")

    # Assert: Verify modal window is displayed by checking its title
    modal_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='orderModal']//div[@class='modal-header']"))
    )
    assert modal_title.is_displayed()

    # Fill checkout form (leaving card empty to trigger validation error)
    utils.fill_checkout_form(browser, wait, "Alex", "Czechia", "Prague", "", "8", "2026")
    # Verify error message via alert popup
    alert = wait.until(EC.alert_is_present())
    alert_obj = browser.switch_to.alert
    assert alert_obj.text == "Please fill out Name and Creditcard."
    alert_obj.accept()

    # Screenshot
    browser.save_screenshot("demoblaze_invalid_checkout.png")


