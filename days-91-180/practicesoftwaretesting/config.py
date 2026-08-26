import uuid

# URL & Timeouts
BASE_URL = "https://practicesoftwaretesting.com/"
DEFAULT_WAIT = 15  # was dead code before (IMPLICIT_WAIT_TIMEOUT, never referenced anywhere)


def get_guest_user_data():
    """
    Returns guest checkout data with a UNIQUE email on every call.
    Previously this was a static dict with a hardcoded email - every CI run
    (and every retry of a failed run) sent the exact same address. Generating
    a fresh one avoids any duplicate-guest edge cases and makes each run's
    data traceable in logs/screenshots.
    """
    unique_id = uuid.uuid4().hex[:8]
    return {
        "email": f"alex.qa.{unique_id}@testing.com",
        "first_name": "Alex",
        "last_name": "QA",
    }


BILLING_ADDRESS_DATA = {
    "country": "US",
    "postal_code": "12321",
    "house_number": "22",
    "street": "Tester's Street",
    "city": "NYC",
    "state": "State",
}

CREDIT_CARD_DATA = {
    "card_number": "1111-2211-4321-1234",
    "expiration_date": "03/2027",
    "cvv": "111",
    "card_holder_name": "QA tester",
}

# --- Locators ---
# Single source of truth. utils.py previously hardcoded some of these inline
# with slightly different values, so a real site change would have needed
# fixing in two places. Consolidated here.

PRODUCT_LOCATOR = "//a[contains(@class, 'card')]"
ADD_TO_CART_BTN_LOCATOR = "//button[@id='btn-add-to-cart']"

# CSS version - matches what actually worked in production, not the unused
# XPath variant that used to sit here unreferenced.
NAV_CART_LOCATOR = "a[data-test='nav-cart'], a[routerlink='/checkout'], a.nav-link[href*='checkout']"
PROCEED_BTN_LOCATOR = "//button[contains(@class, 'btn-success') or contains(text(), 'Proceed to checkout')]"
GUEST_CHECKOUT_RADIO_LOCATOR = "//input[@id='guest-checkout' or @value='guest']"
CONTINUE_AS_GUEST_LINK_LOCATOR = "//button[@data-test='proceed-2'] | //a[contains(text(), 'Continue as Guest')] | //button[contains(text(), 'Proceed to checkout')]"

# Guest Form Locators
GUEST_EMAIL_LOCATOR = "//input[@id='guest-email']"
GUEST_FIRST_NAME_LOCATOR = "//input[@id='guest-first-name']"
GUEST_LAST_NAME_LOCATOR = "//input[@id='guest-last-name']"
GUEST_PROCEED_BTN_LOCATOR = "//button[@data-test='proceed-2' or contains(text(), 'Proceed to checkout')]"

# Billing Address Locators
BILLING_COUNTRY_LOCATOR = "//input[@id='country'] | //select[@id='country']"
BILLING_POSTAL_CODE_LOCATOR = "//input[@id='postal_code']"
BILLING_HOUSE_NUMBER_LOCATOR = "//input[@id='house_number']"
BILLING_STREET_LOCATOR = "//input[@id='street']"
BILLING_CITY_LOCATOR = "//input[@id='city']"
BILLING_STATE_LOCATOR = "//input[@id='state']"
BILLING_CHECKOUT_BTN_LOCATOR = "//button[@data-test='proceed-3' or contains(text(), 'Proceed to checkout')]"

# Payment Locators
PAYMENT_METHOD_DROPDOWN_LOCATOR = "[data-test='payment-method'], select#payment-method"
PAYMENT_CREDIT_CARD_OPTION_LOCATOR = "//option[contains(text(), 'Credit Card')]"
PAYMENT_CARD_NUMBER_LOCATOR = "//input[@id='credit_card_number']"
PAYMENT_EXPIRATION_DATE_LOCATOR = "//input[@id='expiration_date']"
PAYMENT_CVV_LOCATOR = "//input[@id='cvv']"
PAYMENT_CARD_HOLDER_LOCATOR = "//input[@id='card_holder_name']"
PAYMENT_CONFIRM_BTN_LOCATOR = "//button[@data-test='finish' or contains(text(), 'Confirm')]"

SUCCESS_ALERT_LOCATOR = "//div[contains(@class, 'alert-success')] | //div[@data-test='checkout-success']"