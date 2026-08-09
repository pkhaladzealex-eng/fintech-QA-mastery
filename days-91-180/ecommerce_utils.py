from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_site(driver):
    # Navigate to the target website and maximize the browser window
    driver.get("https://www.demoblaze.com/")
    driver.maximize_window()

def click_product_by_name(driver, wait, product_name):
    # Locate a product on the home page by its exact visible name and click it
    product = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//a[normalize-space()='{product_name}']")
    ))
    product.click()


def add_product_to_cart(driver, wait):
    # Locate and click the 'Add to cart' button, then handle alert
    add_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='Add to cart']")
    ))
    add_btn.click()

    # Handle the popup alert
    alert = wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Product added"
    alert.accept()

def navigate_to_cart(driver, wait):
    # Locate and click the 'Cart' link in the navigation menu
    cart_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='Cart']")
    ))
    cart_link.click()


def get_cart_link(driver, wait):
    # Return the 'Cart' navigation link element
    return wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='Cart']")
    ))

def click_place_order(driver,wait):
    place_order_button =wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Place Order']"))
    )
    place_order_button.click()

def fill_checkout_form(driver,wait,name,country,city,card,month,year):
    name_input = wait.until(
        EC.visibility_of_element_located((By.ID, "name"))
    )
    name_input.send_keys(name)
    country_input = wait.until(
        EC.visibility_of_element_located((By.ID, "country"))
    )
    country_input.send_keys(country)

    city_input = wait.until(
        EC.visibility_of_element_located((By.ID,"city"))
    )
    city_input.send_keys(city)
    card_input = wait.until(
        EC.visibility_of_element_located((By.ID, "card"))
    )
    card_input.send_keys(card)

    month_input = wait.until(
        EC.visibility_of_element_located((By.ID, "month"))
    )
    month_input.send_keys(str(month))

    year_input = wait.until(
        EC.visibility_of_element_located((By.ID, "year"))
    )
    year_input.send_keys(str(year))
    # Click purchase button
    purchase_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Purchase']"))
    )
    purchase_btn.click()

def remove_product_from_cart(driver, wait):
    # Locate and click the 'Delete' button in the cart table
    delete_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='Delete']")
    ))
    delete_btn.click()

