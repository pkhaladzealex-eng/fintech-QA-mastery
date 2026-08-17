from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ecommerce_utils as utils
import stripe
import config as cfg
import sqlite3


# Use Selenium to add product to cart (UI automation)
def test_payment_error_handling(browser):
    wait = WebDriverWait(browser, 10)

    utils.open_site(browser)
    assert "STORE" in browser.title

    utils.click_product_by_name(browser, wait, "HTC One M9")
    assert "prod.html" in browser.current_url

    utils.add_product_to_cart(browser, wait)


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
    ui_price = int(raw_price_text.replace("$", "")) * 100

    print(f"{product_name}: {raw_price_text}")




    # Use Stripe API to create a charge with a "DECLINED card" (`tok_chargeDeclined`) for that amount
    stripe.api_key = cfg.STRIPE_API_KEY
    #  Creating a charge in USD using a test card
    try:
        charge = stripe.Charge.create(
        amount=ui_price,
        currency="usd",
        source="tok_chargeDeclined",
        description=product_name
    )
    except stripe.error.CardError as e:
        charge_id = e.error.charge

        charge = stripe.Charge.retrieve(charge_id)

        #  Convert Stripe object to a standard Python dictionary
        data = charge.to_dict()

        #  Data Extraction with safer access
        stripe_amount = charge.amount / 100
        status = data.get('status', 'unknown')
        description = data.get('description', '')

    #  Assert charge.status = "failed"
    assert charge.status == "failed"



    # Insert failed  charge into SQLite database
    conn = sqlite3.connect(cfg.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO payments (payment_id, amount, status, description) VALUES (?, ?, ?, ?)''',
                   (charge.id, charge.amount, charge.status,charge.description)

   )
    conn.commit()

    # Query database to verify failed status is recorded
    cursor.execute('''
        SELECT status, amount FROM payments WHERE payment_id = ?''', (charge.id,))
    db_row = cursor.fetchone()

    # Add logging for debugging
    print(f"[UI] Product: {product_name}, Price: {ui_price/100:.2f}")
    print(f"[Stripe] Charge ID: {charge.id}, Status: {charge.status}")
    print(f"[Database] Status: {db_row[0]}, Amount: {db_row[1]/100:.2f}")
    print("Error handling test passed - All layers consistent")

    # Assert database shows same failure status as Stripe
    assert db_row is not None, "Record was not found in the database!"
    assert db_row[0] == charge.status == "failed"
    assert db_row[1] == ui_price

    # Cleanup test data
    cursor.execute("DELETE FROM payments WHERE payment_id = ?", (charge.id,))
    conn.commit()
    conn.close()

