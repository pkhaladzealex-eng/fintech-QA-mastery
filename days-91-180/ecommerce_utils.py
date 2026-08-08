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

def remove_product_from_cart(driver, wait):
    # Locate and click the 'Delete' button in the cart table
    delete_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[normalize-space()='Delete']")
    ))
    delete_btn.click()

