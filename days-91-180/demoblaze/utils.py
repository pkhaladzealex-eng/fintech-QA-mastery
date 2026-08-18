from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import stripe
import config as cfg

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

def setup_and_add_to_cart(driver, wait, product_name):
    """Navigate to product, add to cart, go to checkout"""
    open_site(driver)
    click_product_by_name(driver, wait, product_name)
    add_product_to_cart(driver, wait)
    navigate_to_cart(driver, wait)
    click_place_order(driver, wait)

# --- NEW HELPER FUNCTIONS (Day 103) ---

def extract_product_details(driver, wait):
    """Extract product name and price in cents from product details page"""
    name = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h2[@class='name']"))
    ).text

    price_text = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[@class='price-container']"))
    ).text.split()[0]

    price_cents = int(price_text.replace("$", "")) * 100
    return name, price_cents


def create_stripe_charge(amount, description, card_token="tok_visa"):
    """Create a charge in Stripe API and handle declined card exceptions"""
    stripe.api_key = cfg.STRIPE_API_KEY
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=card_token,
            description=description
        )
        return charge
    except stripe.error.CardError as e:
        charge_id = e.error.charge
        return stripe.Charge.retrieve(charge_id)


def insert_payment_to_db(charge_id, amount, status, description):
    """Insert payment record into SQLite database"""
    conn = sqlite3.connect(cfg.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO payments (payment_id, amount, status, description) VALUES (?, ?, ?, ?)",
        (charge_id, amount, status, description)
    )
    conn.commit()
    conn.close()