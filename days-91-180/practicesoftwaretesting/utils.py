from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .config import *


def add_product_to_cart(driver, wait):
    # 1. Select product card
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'card')]"))
    ).click()

    # 2. Click Add to cart
    add_to_cart_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, ADD_TO_CART_BTN_LOCATOR))
    )
    add_to_cart_btn.click()

    # 3. Wait until the cart badge text dynamically updates to '1'
    wait.until(
        EC.text_to_be_present_in_element((By.XPATH, CART_LINK_LOCATOR), "1")
    )

    # 4. Read cart count badge
    cart_count_element = driver.find_element(By.XPATH, CART_LINK_LOCATOR)
    return cart_count_element.text.strip()

def navigate_to_checkout(driver, wait):
    # Navigate to the cart
    cart_link = wait.until(
        EC.element_to_be_clickable((By.XPATH,CART_LINK_LOCATOR))
    )
    cart_link.click()

    # Proceed to checkout
    proceed_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH,PROCEED_BTN_LOCATOR))
    )
    proceed_btn.click()

    #    Continue as a guest
    continue_as_guest = wait.until(
        EC.element_to_be_clickable((By.XPATH,CONTINUE_AS_GUEST_LINK_LOCATOR))
    )
    continue_as_guest.click()
    return driver.current_url

def fill_guest_form(driver, wait, user_data):
    #  Fill out the guest checkout form
    e_mail_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, GUEST_EMAIL_LOCATOR))
    )
    e_mail_field.send_keys(user_data["email"])
    first_name_field = wait.until(
        EC.element_to_be_clickable((By.XPATH,GUEST_FIRST_NAME_LOCATOR))
    )
    first_name_field.send_keys(user_data["first_name"])
    last_name_field = wait.until(
        EC.element_to_be_clickable((By.XPATH,GUEST_LAST_NAME_LOCATOR))
    )
    last_name_field.send_keys(user_data["last_name"])

    continue_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH,GUEST_CONTINUE_BTN_LOCATOR))
    )
    continue_btn.click()

    proceed_to_checkout_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH,GUEST_PROCEED_BTN_LOCATOR))
    )
    proceed_to_checkout_btn.click()

    country_field = wait.until(
        EC.visibility_of_element_located((By.XPATH, BILLING_COUNTRY_LOCATOR))
    )
    return country_field.is_displayed()

def fill_billing_address(driver, wait, address_data):

    country_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, BILLING_COUNTRY_LOCATOR))
    )
    country_field.send_keys(address_data["country"])

    postal_code_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, BILLING_POSTAL_CODE_LOCATOR))
    )
    postal_code_field.send_keys(address_data["postal_code"])

    house_number_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, BILLING_HOUSE_NUMBER_LOCATOR))
    )
    house_number_field.send_keys(address_data["house_number"])

    street_address_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, BILLING_STREET_LOCATOR))
    )
    street_address_field.send_keys(address_data["street"])

    city_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, BILLING_CITY_LOCATOR))
    )
    city_field.send_keys(address_data["city"])

    state_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, BILLING_STATE_LOCATOR))
    )
    state_field.send_keys(address_data["state"])

    check_out_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, BILLING_CHECKOUT_BTN_LOCATOR))
    )
    check_out_btn.click()


    payment_dropdown = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, PAYMENT_METHOD_DROPDOWN_LOCATOR))
    )
    return payment_dropdown.is_displayed()

def select_credit_card_payment(driver, wait):
    # Select payment method
    dropdown = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, PAYMENT_METHOD_DROPDOWN_LOCATOR))
    )
    dropdown.click()

    option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, PAYMENT_CREDIT_CARD_OPTION_LOCATOR)
        )
    )
    option.click()

    card_number_field = wait.until(
        EC.visibility_of_element_located((By.XPATH, PAYMENT_CARD_NUMBER_LOCATOR))
    )
    return card_number_field.is_displayed()

def fill_credit_card_details(driver, wait, card_data):
    credit_card_number = wait.until(
        EC.element_to_be_clickable((By.XPATH, PAYMENT_CARD_NUMBER_LOCATOR))
    )
    credit_card_number.send_keys(card_data["card_number"])

    expiration_date = wait.until(
        EC.element_to_be_clickable((By.XPATH, PAYMENT_EXPIRATION_DATE_LOCATOR))
    )
    expiration_date.send_keys(card_data["expiration_date"])

    cvv = wait.until(
        EC.element_to_be_clickable((By.XPATH, PAYMENT_CVV_LOCATOR))
    )
    cvv.send_keys(card_data["cvv"])

    card_holder_name = wait.until(
        EC.element_to_be_clickable((By.XPATH, PAYMENT_CARD_HOLDER_LOCATOR))
    )
    card_holder_name.send_keys(card_data["card_holder_name"])

    confirm_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, PAYMENT_CONFIRM_BTN_LOCATOR))
    )
    confirm_btn.click()


    success_alert = wait.until(
        EC.visibility_of_element_located((By.XPATH, SUCCESS_ALERT_LOCATOR))
    )
    return success_alert.text

def get_success_message(driver, wait):
    # Wait until the success alert is visible
    success_alert = wait.until(
        EC.visibility_of_element_located((By.XPATH, SUCCESS_ALERT_LOCATOR))
    )
    print("Payment Result:", success_alert.text)


