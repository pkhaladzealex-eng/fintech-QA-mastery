from selenium.webdriver.support.ui import WebDriverWait
import sqlite3

from . import config as cfg
from . import utils

def test_payment_error_handling(browser):
    wait = WebDriverWait(browser, 10)

    # 1. UI Automation
    utils.open_site(browser)
    utils.click_product_by_name(browser, wait, "HTC One M9")
    utils.add_product_to_cart(browser, wait)

    # 2. Extract Details
    product_name, ui_price = utils.extract_product_details(browser, wait)

    # 3. Create Declined Charge via Helper
    charge = utils.create_stripe_charge(ui_price, product_name, card_token="tok_chargeDeclined")

    # 4. Assert Stripe Status
    assert charge.status == "failed"

    # 5. Insert Failed Payment to DB via Helper
    utils.insert_payment_to_db(charge.id, charge.amount, charge.status, charge.description)

    # 6. Verify in DB
    conn = sqlite3.connect(cfg.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status, amount FROM payments WHERE payment_id = ?", (charge.id,))
    db_row = cursor.fetchone()

    assert db_row is not None
    assert db_row[0] == charge.status == "failed"
    assert db_row[1] == ui_price

    # Cleanup
    cursor.execute("DELETE FROM payments WHERE payment_id = ?", (charge.id,))
    conn.commit()
    conn.close()