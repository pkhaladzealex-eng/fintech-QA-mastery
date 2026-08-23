def fill_guest_form(driver, wait, user_data):

    e_mail = wait.until(EC.visibility_of_element_located((By.XPATH, GUEST_EMAIL_LOCATOR)))
    e_mail.send_keys(user_data["email"])

    f_name = wait.until(EC.visibility_of_element_located((By.XPATH, GUEST_FIRST_NAME_LOCATOR)))
    f_name.send_keys(user_data["first_name"])

    l_name = wait.until(EC.visibility_of_element_located((By.XPATH, GUEST_LAST_NAME_LOCATOR)))
    l_name.send_keys(user_data["last_name"])

    proceed_btn = wait.until(EC.element_to_be_clickable((By.XPATH, GUEST_PROCEED_BTN_LOCATOR)))
    driver.execute_script("arguments[0].click();", proceed_btn)

    country = wait.until(EC.visibility_of_element_located((By.XPATH, BILLING_COUNTRY_LOCATOR)))
    return country.is_displayed()


def fill_billing_address(driver, wait, address_data):
    country = wait.until(EC.visibility_of_element_located((By.XPATH, BILLING_COUNTRY_LOCATOR)))
    country.send_keys(address_data["country"])

    driver.find_element(By.XPATH, BILLING_POSTAL_CODE_LOCATOR).send_keys(address_data["postal_code"])
    driver.find_element(By.XPATH, BILLING_HOUSE_NUMBER_LOCATOR).send_keys(address_data["house_number"])
    driver.find_element(By.XPATH, BILLING_STREET_LOCATOR).send_keys(address_data["street"])
    driver.find_element(By.XPATH, BILLING_CITY_LOCATOR).send_keys(address_data["city"])
    driver.find_element(By.XPATH, BILLING_STATE_LOCATOR).send_keys(address_data["state"])

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, BILLING_CHECKOUT_BTN_LOCATOR)))
    driver.execute_script("arguments[0].click();", btn)

    dropdown = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, PAYMENT_METHOD_DROPDOWN_LOCATOR)))
    return dropdown.is_displayed()


def select_credit_card_payment(driver, wait):
    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, PAYMENT_METHOD_DROPDOWN_LOCATOR)))
    dropdown.click()

    option = wait.until(EC.element_to_be_clickable((By.XPATH, PAYMENT_CREDIT_CARD_OPTION_LOCATOR)))
    option.click()

    card_field = wait.until(EC.visibility_of_element_located((By.XPATH, PAYMENT_CARD_NUMBER_LOCATOR)))
    return card_field.is_displayed()


def fill_credit_card_details(driver, wait, card_data):
    card_input = wait.until(EC.visibility_of_element_located((By.XPATH, PAYMENT_CARD_NUMBER_LOCATOR)))
    card_input.send_keys(card_data["card_number"])

    driver.find_element(By.XPATH, PAYMENT_EXPIRATION_DATE_LOCATOR).send_keys(card_data["expiration_date"])
    driver.find_element(By.XPATH, PAYMENT_CVV_LOCATOR).send_keys(card_data["cvv"])
    driver.find_element(By.XPATH, PAYMENT_CARD_HOLDER_LOCATOR).send_keys(card_data["card_holder_name"])

    confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, PAYMENT_CONFIRM_BTN_LOCATOR)))
    driver.execute_script("arguments[0].click();", confirm_btn)

    alert = wait.until(EC.visibility_of_element_located((By.XPATH, SUCCESS_ALERT_LOCATOR)))
    return alert.text