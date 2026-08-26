from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import utils
from . import config as cfg


def test_add_product_to_cart_and_remove(browser):
    wait = WebDriverWait(browser, cfg.DEFAULT_WAIT)

    # Setup: Open site
    utils.open_site(browser)
    assert "STORE" in browser.title

    # Execute: Click the product
    utils.click_product_by_name(browser, wait, "HTC One M9")
    assert "prod.html" in browser.current_url

    # Execute: Add to cart (alert handled inside utility function)
    utils.add_product_to_cart(browser, wait)

    # Execute: Navigate to cart
    utils.navigate_to_cart(browser, wait)

    # Assert: Verify cart page
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Cart']")))
    assert "cart.html" in browser.current_url

    # Find the item in the cart
    cart_item = wait.until(
        EC.presence_of_element_located((By.XPATH, "//td[normalize-space()='HTC One M9']"))
    )
    assert cart_item.is_displayed()

    # Execute: Remove item
    utils.remove_product_from_cart(browser, wait)

    # Verify item is gone from the cart (staleness + explicit re-query)
    wait.until(EC.staleness_of(cart_item))
    wait.until(
        lambda driver: len(driver.find_elements(By.XPATH, "//td[contains(text(), 'HTC One M9')]")) == 0
    )

    remaining_items = browser.find_elements(By.XPATH, "//td[contains(text(), 'HTC One M9')]")
    assert len(remaining_items) == 0, "Item was not removed from cart!"

    # Screenshot
    browser.save_screenshot("demoblaze_cart_01.png")