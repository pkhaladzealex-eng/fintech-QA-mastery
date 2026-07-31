from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # 1. Open site
    driver.get("https://www.saucedemo.com/")

    # 2. Login
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # 3. Add product to cart
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()

    # 4. Verify cart
    cart = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert cart.text == "1", "Cart is empty!"
    print(f"Cart count: {cart.text}")

    # 5. Screenshot
    driver.save_screenshot("cart_screenshot.png")
    print("Screenshot saved!")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()