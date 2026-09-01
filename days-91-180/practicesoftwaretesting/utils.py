import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from . import config as cfg


def _click_with_retry(driver, wait, by, locator, retries=3):
    """
    Re-locates and clicks an element, retrying on StaleElementReferenceException
    OR TimeoutException.

    This site (Angular + an async "live activity" widget) re-renders parts
    of the DOM in the background. A perfectly valid element found by
    wait.until(...) can become stale in the small gap before .click() runs,
    because Angular replaced that DOM node in the meantime - OR the same
    re-render can make the element briefly not-clickable during a single
    wait.until() poll window, which surfaces as a TimeoutException instead.
    Both are symptoms of the same underlying flakiness, so both are retried
    with a fresh WebDriverWait each attempt rather than trusting one poll
    window to catch the element in a stable state.
    """
    last_exc = None
    for _ in range(retries):
        try:
            attempt_wait = WebDriverWait(driver, cfg.DEFAULT_WAIT)
            el = attempt_wait.until(EC.element_to_be_clickable((by, locator)))
            el.click()
            return el
        except (StaleElementReferenceException, TimeoutException) as exc:
            last_exc = exc
            continue
    raise last_exc


def add_product_to_cart(driver, wait):
    _click_with_retry(driver, wait, By.XPATH, cfg.PRODUCT_LOCATOR)
    _click_with_retry(driver, wait, By.XPATH, cfg.ADD_TO_CART_BTN_LOCATOR)

    # NOTE: kept as a short fixed pause - the cart badge/counter has no stable
    # data-test attribute to wait on explicitly. If one becomes available,
    # replace this with an explicit EC.text_to_be_present_in_element wait.
    time.sleep(2)
    return True


def navigate_to_checkout(driver, wait):
    _click_with_retry(driver, wait, By.CSS_SELECTOR, cfg.NAV_CART_LOCATOR)

    _click_with_retry(driver, wait, By.XPATH, cfg.PROCEED_BTN_LOCATOR)

    # Explicit checkpoint: confirm the wizard actually advanced to the
    # Sign In step (its tab list becomes present) BEFORE hunting for the
    # guest tab specifically. If the proceed click silently no-ops, this
    # fails here with a clear message instead of a confusing timeout two
    # steps later.
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'nav-tabs')]")))

    # Click the "Continue as Guest" tab (a Bootstrap tab anchor, not a
    # separate proceed button - see config.py comment for why the locator
    # is scoped precisely).
    _click_with_retry(driver, wait, By.XPATH, cfg.CONTINUE_AS_GUEST_LINK_LOCATOR)

    return driver.current_url


def fill_guest_form(driver, wait, user_data):
    e_mail = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.GUEST_EMAIL_LOCATOR)))
    e_mail.send_keys(user_data["email"])

    f_name = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.GUEST_FIRST_NAME_LOCATOR)))
    f_name.send_keys(user_data["first_name"])

    l_name = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.GUEST_LAST_NAME_LOCATOR)))
    l_name.send_keys(user_data["last_name"])

    _click_with_retry(driver, wait, By.XPATH, cfg.GUEST_PROCEED_BTN_LOCATOR)

    # After guest form submits, a confirmation line appears ("Continuing as
    # guest: ...") with its own separate proceed button - the wizard does
    # NOT advance to Billing Address until this is also clicked.
    _click_with_retry(driver, wait, By.XPATH, cfg.GUEST_CONFIRM_PROCEED_LOCATOR)

    country = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.BILLING_COUNTRY_LOCATOR)))
    return country.is_displayed()


def fill_billing_address(driver, wait, address_data):
    country_dropdown = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.BILLING_COUNTRY_LOCATOR)))
    Select(country_dropdown).select_by_value(address_data["country"])

    driver.find_element(By.XPATH, cfg.BILLING_POSTAL_CODE_LOCATOR).send_keys(address_data["postal_code"])
    driver.find_element(By.XPATH, cfg.BILLING_HOUSE_NUMBER_LOCATOR).send_keys(address_data["house_number"])
    driver.find_element(By.XPATH, cfg.BILLING_STREET_LOCATOR).send_keys(address_data["street"])
    driver.find_element(By.XPATH, cfg.BILLING_CITY_LOCATOR).send_keys(address_data["city"])
    driver.find_element(By.XPATH, cfg.BILLING_STATE_LOCATOR).send_keys(address_data["state"])

    _click_with_retry(driver, wait, By.XPATH, cfg.BILLING_CHECKOUT_BTN_LOCATOR)

    dropdown = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, cfg.PAYMENT_METHOD_DROPDOWN_LOCATOR)))
    return dropdown.is_displayed()


def select_credit_card_payment(driver, wait):
    dropdown = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, cfg.PAYMENT_METHOD_DROPDOWN_LOCATOR)))
    Select(dropdown).select_by_value("credit-card")

    card_field = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.PAYMENT_CARD_NUMBER_LOCATOR)))
    return card_field.is_displayed()


def fill_credit_card_details(driver, wait, card_data):
    card_input = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.PAYMENT_CARD_NUMBER_LOCATOR)))
    card_input.send_keys(card_data["card_number"])

    driver.find_element(By.XPATH, cfg.PAYMENT_EXPIRATION_DATE_LOCATOR).send_keys(card_data["expiration_date"])
    driver.find_element(By.XPATH, cfg.PAYMENT_CVV_LOCATOR).send_keys(card_data["cvv"])
    driver.find_element(By.XPATH, cfg.PAYMENT_CARD_HOLDER_LOCATOR).send_keys(card_data["card_holder_name"])

    _click_with_retry(driver, wait, By.XPATH, cfg.PAYMENT_CONFIRM_BTN_LOCATOR)

    alert = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.SUCCESS_ALERT_LOCATOR)))
    return alert.text