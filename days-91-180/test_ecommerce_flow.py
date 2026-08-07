import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()


def test_add_product_to_cart(driver):
    wait = WebDriverWait(driver, 10)

    # Setup: Open site
    driver.get("https://www.demoblaze.com/")
    assert "STORE" in driver.title

    # Execute: Click first product
    first_product = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.card-block h4 a")
    ))
    first_product.click()
    assert "prod.html" in driver.current_url

    # Execute: Add to cart
    add_to_cart = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.btn-success")
    ))
    add_to_cart.click()

    # Execute: Handle alert
    alert = wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Product added"
    alert.accept()

    # Execute: Navigate to cart
    cart_link = wait.until(EC.element_to_be_clickable(
        (By.ID, "cartur")
    ))
    cart_link.click()

    # Assert: Verify cart page
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "table.table")
    ))
    assert "cart" in driver.current_url
    print("Cart verified!")

    # Screenshot
    driver.save_screenshot("demoblaze_cart.png")

def test_add_product_to_cart_and_remove(driver):
    wait = WebDriverWait(driver, 10)

    # Setup: Open site
    driver.get("https://www.demoblaze.com/")
    assert "STORE"  in driver.title

    # Execute: Click the product
    product = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='HTC One M9']")
    ))
    product.click()
    assert "prod.html" in driver.current_url

    # Execute: Add to cart
    add_to_cart = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Add to cart']"))
    )
    add_to_cart.click()

    # Execute: Handle alert
    alert = wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert alert.text == "Product added"
    alert.accept()

    # Execute: Navigate to cart
    cart_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Cart']"))
    )
    cart_link.click()

    # Assert: Verify cart page
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Cart']"))
    )
    assert "cart.html" in driver.current_url

    # Find the item on the cart
    cart_item = wait.until(
        EC.presence_of_element_located((By.XPATH,"//td[normalize-space()='HTC One M9']"))
    )
    assert cart_item.is_displayed()
    print("Product verified!")

    # Execute: Remove item
    remove_from_cart = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Delete']"))
    )
    remove_from_cart.click()


    # Verify product is removed from cart
    wait.until(EC.staleness_of(cart_item))

    # Assertion: Product removed from cart
    remaining_items = driver.find_elements(By.XPATH, "//td[contains(text(), 'HTC One M9')]")
    assert len(remaining_items) == 0, "Item was not removed from cart!"

    print("Product successfully removed from cart!")

    # Screenshot
    driver.save_screenshot("demoblaze_cart_01.png")







