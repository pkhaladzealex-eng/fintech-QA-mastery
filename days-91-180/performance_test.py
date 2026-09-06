"""
Performance monitoring for checkout flows.

These tests don't check functional correctness (test_ecommerce_flow.py,
test_checkout.py etc. already do that) - they measure how long the SAME
flows take to run, and fail if a flow gets dramatically slower than
expected. That's a signal worth catching: a site redesign adding an extra
step, a broken retry loop silently retrying 3x every time, or a network
regression would all show up here before anyone notices "the tests feel
slower lately".

Thresholds are intentionally generous - the goal is to catch a MAJOR
regression (a flow taking 2-3x longer than normal), not to enforce a tight
SLA that would make this test flaky on a slow CI runner.
"""
import time

from selenium.webdriver.support.ui import WebDriverWait

from demoblaze import utils as demoblaze_utils
from practicesoftwaretesting import utils as pst_utils
from practicesoftwaretesting import config as pst_cfg


def test_demoblaze_add_to_cart_performance(browser):
    """Measure how long it takes to add a product to the demoblaze cart."""
    wait = WebDriverWait(browser, 15)

    start_time = time.time()

    demoblaze_utils.open_site(browser)
    demoblaze_utils.click_product_by_name(browser, wait, "HTC One M9")
    demoblaze_utils.add_product_to_cart(browser, wait)
    demoblaze_utils.navigate_to_cart(browser, wait)

    duration = time.time() - start_time

    assert duration < 30, f"demoblaze add-to-cart flow took {duration:.2f}s, should be < 30s"
    print(f"[demoblaze] Add-to-cart completed in {duration:.2f} seconds")


def test_practicesoftwaretesting_guest_checkout_performance(browser):
    """
    Measure how long the guest checkout flow takes, from opening the site
    through submitting the guest form (Cart -> Sign In -> Guest tab -> Guest
    form -> confirmation).
    """
    wait = WebDriverWait(browser, pst_cfg.DEFAULT_WAIT)

    start_time = time.time()

    browser.get(pst_cfg.BASE_URL)
    pst_utils.add_product_to_cart(browser, wait)
    pst_utils.navigate_to_checkout(browser, wait)
    guest_data = pst_cfg.get_guest_user_data()
    pst_utils.fill_guest_form(browser, wait, guest_data)

    duration = time.time() - start_time

    # Higher budget than the demoblaze flow: this one goes through more
    # steps (guest tab, guest form, guest confirmation) and uses a
    # click-with-retry helper that can legitimately take longer under
    # transient load before it's considered a real regression.
    assert duration < 60, f"Guest checkout flow took {duration:.2f}s, should be < 60s"
    print(f"[practicesoftwaretesting] Guest checkout (through guest form) completed in {duration:.2f} seconds")