from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # 1. Open Amazon
    driver.get("https://www.amazon.com/")
    time.sleep(3)

    # 2. Search for product
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
    search_box.send_keys("wireless mouse")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # 3. Click first result
    first_product = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.s-result-item h2 a")))
    first_product.click()
    time.sleep(3)

    # 4. Add to cart
    add_to_cart = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-button")))
    add_to_cart.click()
    time.sleep(3)

    # 5. Verify cart
    cart_count = wait.until(EC.visibility_of_element_located((By.ID, "nav-cart-count")))
    assert cart_count.text != "0", "Cart is empty!"
    print(f"Cart count: {cart_count.text}")

    # 6. Screenshot
    driver.save_screenshot("amazon_cart.png")
    print("Screenshot saved!")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()