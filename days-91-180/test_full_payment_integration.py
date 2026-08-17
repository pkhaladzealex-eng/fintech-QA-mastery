from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ecommerce_utils as utils
import stripe
import config as cfg
import sqlite3





# Use Selenium to add product to cart (UI automation)
def test_full_payment_integration(browser):
    wait = WebDriverWait(browser, 10)

    utils.open_site(browser)
    assert "STORE" in browser.title

    utils.click_product_by_name(browser, wait,"HTC One M9")
    assert "prod.html" in browser.current_url

    utils.add_product_to_cart(browser,wait)


    # Extract product details from page (price, name)
    name_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h2[@class='name']"))
    )
    product_name = name_element.text

    price_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[@class='price-container']"))
    )
    # "$700 *includes tax" -> 70000 cents
    raw_price_text = price_element.text.split()[0]  # "$700"
    UI_price = int(raw_price_text.replace("$", "")) * 100

    print(f"{product_name}: {UI_price}")


    # Use Stripe API to create test charge with that amount
    stripe.api_key = cfg.STRIPE_API_KEY
    #  Creating a charge in USD using a test card
    charge = stripe.Charge.create(
        amount=UI_price,
        currency="usd",
        source="tok_visa",
        description=product_name
    )


    resource = stripe.Charge.retrieve(charge.id)
    # 2. Convert Stripe object to a standard Python dictionary
    data = resource.to_dict()

    # 3. Data Extraction with safer access
    stripe_amount = charge.amount / 100
    status = data.get('status', 'unknown')
    description = data.get('description', '')








    # Insert charge into SQLite database
    connection = sqlite3.connect(cfg.DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO payments (payment_id, amount, status, description) VALUES (?, ?, ?, ?)",
        (charge.id, charge.amount, charge.status, charge.description)
    )
    connection.commit()



    # Query database to verify charge is recorded

    cursor.execute("SELECT amount, description FROM payments WHERE payment_id = ?", (charge.id,))
    db_row = cursor.fetchone()

    # Extract values from DB result
    db_amount = db_row[0]
    db_description = db_row[1]

    print(f"UI Price: ${UI_price/100:.2f}")
    print(f"Stripe Charge: {charge.id} - ${charge.amount/100:.2f}")
    print(f"DB Record: {db_amount/100:.2f}")

    #  Assert: UI price = Stripe amount = Database amount
    assert UI_price == charge.amount == db_amount
    assert product_name == charge.description == db_description
    
    cursor.execute("DELETE FROM payments WHERE payment_id = ?", (charge.id,))
    connection.commit()
    connection.close()
    connection.close()


