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


    # Click first product
    first_product = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.card-block h4 a")
    ))
    first_product.click()
    print("Product page opened!")
    print(driver.current_url)

    # Add to cart
    add_to_cart = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.btn-success")
    ))
    add_to_cart.click()
    print("Added to cart!")

    # Handle popup alert
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(f"Popup message: {alert.text}")
    alert.accept()
    time.sleep(1)

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


except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
