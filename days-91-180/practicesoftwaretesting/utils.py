from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

from . import config as cfg


def add_product_to_cart(driver, wait):
    product = wait.until(EC.presence_of_element_located((By.XPATH, cfg.PRODUCT_LOCATOR)))
    driver.execute_script("arguments[0].click();", product)

    add_btn = wait.until(EC.presence_of_element_located((By.XPATH, cfg.ADD_TO_CART_BTN_LOCATOR)))
    driver.execute_script("arguments[0].click();", add_btn)

    # NOTE: kept as a short fixed pause - the cart badge/counter has no stable
    # data-test attribute to wait on explicitly. If one becomes available,
    # replace this with an explicit EC.text_to_be_present_in_element wait.
    time.sleep(2)
    return True


def navigate_to_checkout(driver, wait):
    cart_icon = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cfg.NAV_CART_LOCATOR))
    )
    driver.execute_script("arguments[0].click();", cart_icon)

    proceed_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, cfg.PROCEED_BTN_LOCATOR))
    )
    driver.execute_script("arguments[0].click();", proceed_btn)

    # Click the "Continue as Guest" tab (a Bootstrap tab anchor, not a
    # separate proceed button - see config.py comment for why the locator
    # is scoped precisely).
    continue_guest = wait.until(
        EC.element_to_be_clickable((By.XPATH, cfg.CONTINUE_AS_GUEST_LINK_LOCATOR))
    )
    driver.execute_script("arguments[0].click();", continue_guest)

    return driver.current_url


def fill_guest_form(driver, wait, user_data):
    e_mail = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.GUEST_EMAIL_LOCATOR)))
    e_mail.send_keys(user_data["email"])

    f_name = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.GUEST_FIRST_NAME_LOCATOR)))
    f_name.send_keys(user_data["first_name"])

    l_name = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.GUEST_LAST_NAME_LOCATOR)))
    l_name.send_keys(user_data["last_name"])

    proceed_btn = wait.until(EC.element_to_be_clickable((By.XPATH, cfg.GUEST_PROCEED_BTN_LOCATOR)))
    driver.execute_script("arguments[0].click();", proceed_btn)

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

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, cfg.BILLING_CHECKOUT_BTN_LOCATOR)))
    driver.execute_script("arguments[0].click();", btn)

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

    confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, cfg.PAYMENT_CONFIRM_BTN_LOCATOR)))
    driver.execute_script("arguments[0].click();", confirm_btn)

    alert = wait.until(EC.visibility_of_element_located((By.XPATH, cfg.SUCCESS_ALERT_LOCATOR)))
    return alert.text