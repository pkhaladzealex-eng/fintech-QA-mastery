# URL & Timeouts
BASE_URL = "https://practicesoftwaretesting.com/"

IMPLICIT_WAIT_TIMEOUT = 10

# Test Data

GUEST_USER_DATA = {
    "email": "alex@testing.com",
    "first_name": "Alex",
    "last_name": "QA"
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

# Locators
# Find available item
PRODUCT_LOCATOR = "(//a[contains(@class, 'card')])[1]"
ADD_TO_CART_BTN_LOCATOR = "//button[@id='btn-add-to-cart']"

CART_LINK_LOCATOR = "//span[@id='lblCartCount']"

PROCEED_BTN_LOCATOR = "//div[@class='d-flex justify-content-between ng-star-inserted']//button[@type='button'][normalize-space()='Proceed to checkout']"


CONTINUE_AS_GUEST_LINK_LOCATOR = "//a[normalize-space()='Continue as Guest']"

# Guest Form Locators
GUEST_EMAIL_LOCATOR = "//input[@id='guest-email']"
GUEST_FIRST_NAME_LOCATOR = "//input[@id='guest-first-name']"
GUEST_LAST_NAME_LOCATOR = "//input[@id='guest-last-name']"
GUEST_CONTINUE_BTN_LOCATOR = "//input[@value='Continue as Guest']"
GUEST_PROCEED_BTN_LOCATOR = "//div[@class='float-end ng-star-inserted']//button[@type='button'][normalize-space()='Proceed to checkout']"

# Billing Address Locators
BILLING_COUNTRY_LOCATOR = "//select[@id='country']"
BILLING_POSTAL_CODE_LOCATOR = "//input[@id='postal_code']"
BILLING_HOUSE_NUMBER_LOCATOR = "//input[@id='house_number']"
BILLING_STREET_LOCATOR = "//input[@id='street']"
BILLING_CITY_LOCATOR = "//input[@id='city']"
BILLING_STATE_LOCATOR = "//input[@id='state']"
BILLING_CHECKOUT_BTN_LOCATOR = "//div[@class='float-end']//button[@type='button'][normalize-space()='Proceed to checkout']"

# Payment Locators
PAYMENT_METHOD_DROPDOWN_LOCATOR = "[data-test='payment-method']"
PAYMENT_CREDIT_CARD_OPTION_LOCATOR = "//option[contains(text(), 'Credit Card')]"
PAYMENT_CARD_NUMBER_LOCATOR = "//input[@id='credit_card_number']"
PAYMENT_EXPIRATION_DATE_LOCATOR = "//input[@id='expiration_date']"
PAYMENT_CVV_LOCATOR = "//input[@id='cvv']"
PAYMENT_CARD_HOLDER_LOCATOR = "//input[@id='card_holder_name']"
PAYMENT_CONFIRM_BTN_LOCATOR = "//button[normalize-space()='Confirm']"

SUCCESS_ALERT_LOCATOR = "//div[contains(@class, 'alert-success')]"
