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

# Confirmed from a real screenshot of the product listing: an out-of-stock
# product shows red "Out of stock" text in place of the price, inside the
# same card. This locator excludes any card containing that text, so we
# always land on a purchasable product instead of hardcoding the first card
# (which sometimes turned out to be out of stock).
IN_STOCK_PRODUCT_LOCATOR = "//a[contains(@class, 'card')][not(.//*[contains(text(), 'Out of stock')])]"

ADD_TO_CART_BTN_LOCATOR = "//button[@id='btn-add-to-cart']"

# Confirmed from a real screenshot: this exact toast text appears after a
# successful add-to-cart. Waiting for it replaces the old blind
# time.sleep(10)/time.sleep(2) that previously guessed how long the cart
# update would take.
ADD_TO_CART_SUCCESS_TOAST_LOCATOR = "//*[contains(text(), 'Product added to shopping cart')]"

# CSS version - matches what actually worked in production, not the unused
# XPath variant that used to sit here unreferenced.
NAV_CART_LOCATOR = "a[data-test='nav-cart'], a[routerlink='/checkout'], a.nav-link[href*='checkout']"

# Scoped to the exact Cart-step button only. The previous version
# ("//button[contains(@class,'btn-success') or contains(text(),'Proceed to
# checkout')]") was dangerously broad: THREE different wizard steps (Cart's
# proceed-1, Guest-confirm's proceed-2-guest, Address's proceed-3) all use
# the same class and the same visible text. If more than one of those
# buttons is briefly present in the DOM during Angular's initial render
# (before "hidden" is applied), that locator could match and click the
# WRONG step's button, producing exactly the kind of inconsistent,
# hard-to-reproduce failures seen across multiple CI runs.
PROCEED_BTN_LOCATOR = "//button[@data-test='proceed-1']"

# The "Continue as Guest" element is a Bootstrap TAB anchor (href="#guest-tab"),
# not a separate proceed button. Confirmed from a real CI failure's page
# source dump. It must be targeted uniquely: the text "Proceed to checkout"
# also appears on two OTHER wizard steps (Cart's proceed-1, Address's
# proceed-3) which briefly remain in the DOM during the step transition -
# a locator that OR's in that text can race-condition-click the wrong,
# stale button instead of this tab. Scoping to data-bs-toggle='tab' avoids
# that collision entirely.
CONTINUE_AS_GUEST_LINK_LOCATOR = "//a[@data-bs-toggle='tab' and contains(text(), 'Continue as Guest')]"

# Guest Form Locators
GUEST_EMAIL_LOCATOR = "//input[@id='guest-email']"
GUEST_FIRST_NAME_LOCATOR = "//input[@id='guest-first-name']"
GUEST_LAST_NAME_LOCATOR = "//input[@id='guest-last-name']"

# Confirmed from real page source: this is an <input type="submit"
# data-test="guest-submit">, NOT a <button> - the old locator
# ("//button[@data-test='proceed-2' ...]") never matched anything real.
GUEST_PROCEED_BTN_LOCATOR = "//input[@data-test='guest-submit']"

# After the guest form submits, the site shows a confirmation line
# ("Continuing as guest: ...") with its OWN separate "Proceed to checkout"
# button before actually advancing to Billing Address. Confirmed from real
# page source - previously missing entirely from this flow.
GUEST_CONFIRM_PROCEED_LOCATOR = "//button[@data-test='proceed-2-guest']"

# Billing Address Locators
# Confirmed from real page source: country is a <select>, not an <input>.
BILLING_COUNTRY_LOCATOR = "//select[@id='country']"
BILLING_POSTAL_CODE_LOCATOR = "//input[@id='postal_code']"
BILLING_HOUSE_NUMBER_LOCATOR = "//input[@id='house_number']"
BILLING_STREET_LOCATOR = "//input[@id='street']"
BILLING_CITY_LOCATOR = "//input[@id='city']"
BILLING_STATE_LOCATOR = "//input[@id='state']"
# Scoped to the exact Address-step button only - same reasoning as
# PROCEED_BTN_LOCATOR above.
BILLING_CHECKOUT_BTN_LOCATOR = "//button[@data-test='proceed-3']"

# Payment Locators
PAYMENT_METHOD_DROPDOWN_LOCATOR = "[data-test='payment-method'], select#payment-method"
PAYMENT_CREDIT_CARD_OPTION_LOCATOR = "//option[contains(text(), 'Credit Card')]"
PAYMENT_CARD_NUMBER_LOCATOR = "//input[@id='credit_card_number']"
PAYMENT_EXPIRATION_DATE_LOCATOR = "//input[@id='expiration_date']"
PAYMENT_CVV_LOCATOR = "//input[@id='cvv']"
PAYMENT_CARD_HOLDER_LOCATOR = "//input[@id='card_holder_name']"
PAYMENT_CONFIRM_BTN_LOCATOR = "//button[@data-test='finish' or contains(text(), 'Confirm')]"

SUCCESS_ALERT_LOCATOR = "//div[contains(@class, 'alert-success')] | //div[@data-test='checkout-success']"