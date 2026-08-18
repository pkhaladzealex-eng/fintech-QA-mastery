import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import utils
import config as cfg


def test_add_product_to_cart(browser):
    wait = WebDriverWait(browser, 10)

    # Setup: Open site
    utils.open_site(browser)
    assert "STORE" in browser.title

    # Execute: Click first product
    first_product = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.card-block h4 a")
    ))
    first_product.click()
    assert "prod.html" in browser.current_url

    # Execute: Add to cart and handle alert inside utility function
    utils.add_product_to_cart(browser, wait)


    # Execute: Navigate to cart
    utils.navigate_to_cart(browser, wait)

    # Assert: Verify cart page
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "table.table")
    ))
    assert "cart" in browser.current_url

    # Screenshot
    browser.save_screenshot("demoblaze_cart.png")

def test_add_product_to_cart_and_remove(browser):
    wait = WebDriverWait(browser, 10)

    # Setup: Open site
    utils.open_site(browser)
    assert "STORE"  in browser.title

    # Execute: Click the product
    utils.click_product_by_name(browser, wait, "HTC One M9")
    assert "prod.html" in browser.current_url

    # Execute: Add to cart and handle alert inside utility function
    utils.add_product_to_cart(browser, wait)

    # Execute: Navigate to cart
    utils.navigate_to_cart(browser, wait)

    # Assert: Verify cart page
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Cart']"))
    )
    assert "cart.html" in browser.current_url

    # Find the item on the cart
    cart_item = wait.until(
        EC.presence_of_element_located((By.XPATH,"//td[normalize-space()='HTC One M9']"))
    )
    assert cart_item.is_displayed()
    print("Product verified!")

    # Execute: Remove item
    utils.remove_product_from_cart(browser, wait)

    # Verify product is removed from cart
    wait.until(EC.staleness_of(cart_item))

    # Assertion: Product removed from cart
    remaining_items = browser.find_elements(By.XPATH, "//td[contains(text(), 'HTC One M9')]")
    assert len(remaining_items) == 0, "Item was not removed from cart!"

    # Screenshot
    browser.save_screenshot("demoblaze_cart_01.png")







