from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.demoblaze.com/")
    driver.maximize_window()
    print(driver.title)
    time.sleep(2)

    # Click first product
    first_product = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.card-block h4 a")
    ))
    first_product.click()
    print("Product page opened!")
    print(driver.current_url)
    time.sleep(5)

    # Add to cart
    add_to_cart = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.btn-success")
    ))
    add_to_cart.click()
    print("Added to cart!")
    time.sleep(2)

    # Handle popup alert
    alert = driver.switch_to.alert
    print(f"Popup message: {alert.text}")
    alert.accept()
    time.sleep(2)

    # Navigate to cart
    cart_link = wait.until(EC.element_to_be_clickable(
        (By.ID, "cartur")
    ))
    cart_link.click()
    print("Cart page opened!")
    print(driver.current_url)
    time.sleep(2)



    # Screenshot
    driver.save_screenshot("demoblaze_cart.png")
    print("Screenshot saved!")
    time.sleep(2)


except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
