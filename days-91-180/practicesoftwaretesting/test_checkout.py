from selenium.webdriver.support.ui import WebDriverWait

from . import config as cfg
from . import utils


def test_successful_guest_checkout(browser):
    wait = WebDriverWait(browser, cfg.DEFAULT_WAIT)

    # Step 1: Open site
    browser.get(cfg.BASE_URL)

    # Step 2: Add product to cart and verify addition
    is_added = utils.add_product_to_cart(browser, wait)
    assert is_added is True, "Failed to add product to cart"

    # Step 3: Navigate to checkout and verify URL
    current_url = utils.navigate_to_checkout(browser, wait)
    assert "checkout" in current_url, f"Expected 'checkout' in URL, but got '{current_url}'"

    # Step 4: Fill guest form (unique email per run) and verify billing step appears
    guest_data = cfg.get_guest_user_data()
    is_billing_visible = utils.fill_guest_form(browser, wait, guest_data)
    assert is_billing_visible is True, "Billing address step did not appear!"

    # Step 5: Fill billing address and verify payment step is visible
    is_payment_visible = utils.fill_billing_address(browser, wait, cfg.BILLING_ADDRESS_DATA)
    assert is_payment_visible is True, "Payment method step did not appear!"

    # Step 6: Select credit card payment and verify card inputs are visible
    is_card_input_visible = utils.select_credit_card_payment(browser, wait)
    assert is_card_input_visible is True, "Credit card detail fields did not appear!"

    # Step 7: Fill credit card details and verify success message
    success_message = utils.fill_credit_card_details(browser, wait, cfg.CREDIT_CARD_DATA)
    assert "successful" in success_message.lower(), f"Expected 'successful' in message, but got: {success_message}"

    # Screenshot
    browser.save_screenshot("practicesoftwaretesting.png")