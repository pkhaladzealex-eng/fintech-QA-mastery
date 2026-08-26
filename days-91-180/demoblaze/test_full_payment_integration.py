from selenium.webdriver.support.ui import WebDriverWait
import sqlite3

from . import config as cfg
from . import utils


def test_full_payment_integration(browser):
    wait = WebDriverWait(browser, cfg.DEFAULT_WAIT)

    # 1. UI Automation
    utils.open_site(browser)
    utils.click_product_by_name(browser, wait, "HTC One M9")
    utils.add_product_to_cart(browser, wait)

    # 2. Extract Product Details via Helper
    product_name, ui_price = utils.extract_product_details(browser, wait)

    # 3. Stripe API Charge via Helper
    charge = utils.create_stripe_charge(ui_price, product_name, card_token="tok_visa")

    # 4. Insert into Database via Helper
    utils.insert_payment_to_db(charge.id, charge.amount, charge.status, charge.description)

    # 5. DB Verification & Assertion
    conn = sqlite3.connect(cfg.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, description FROM payments WHERE payment_id = ?", (charge.id,))
    db_row = cursor.fetchone()

    assert ui_price == charge.amount == db_row[0]
    assert product_name == charge.description == db_row[1]

    # Cleanup
    cursor.execute("DELETE FROM payments WHERE payment_id = ?", (charge.id,))
    conn.commit()
    conn.close()