from selenium.webdriver.support.ui import WebDriverWait
import time

from config import *
from utils import *

def test_successful_guest_checkout(browser):

    wait = WebDriverWait(browser, IMPLICIT_WAIT_TIMEOUT)

    try:
        # Step 1: Open site
        browser.get(BASE_URL)

        ## Step 2: Add product to cart and verify cart counter
        cart_count = add_product_to_cart(browser, wait)
        assert cart_count == "1", f"Expected '1', but got '{cart_count}'"

        # Step 3: Navigate to checkout and verify URL
        current_url = navigate_to_checkout(browser, wait)
        assert "checkout" in current_url, f"Expected 'checkout' in URL, but got '{current_url}'"

        # Step 4: Fill guest form and verify billing address step is visible
        is_billing_visible = fill_guest_form(browser, wait, GUEST_USER_DATA)
        assert is_billing_visible is True, "Billing address step did not appear!"

        # Step 5: Fill billing address and verify payment step is visible
        is_payment_visible = fill_billing_address(browser, wait, BILLING_ADDRESS_DATA)
        assert is_payment_visible is True, "Payment method step did not appear!"

        # Step 6: Select credit card payment and verify card inputs are visible
        is_card_input_visible = select_credit_card_payment(browser, wait)
        assert is_card_input_visible is True, "Credit card detail fields did not appear!"

        # Step 7: Fill credit card details and verify success message
        success_message = fill_credit_card_details(browser, wait, CREDIT_CARD_DATA)
        assert "successful" in success_message.lower(), f"Expected 'successful' in message, but got: {success_message}"
        time.sleep(2)

        # Screenshot
        browser.save_screenshot("practicesoftwaretesting.png")

    finally:
        browser.quit()