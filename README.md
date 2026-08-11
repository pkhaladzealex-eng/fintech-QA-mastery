# Fintech QA Mastery (Phase 2: Days 91-180)

Welcome to Phase 2 of my QA Automation Journey! 

Having established strong foundations in Python, Selenium UI testing, API payment verification, and SQLite database testing during Days 1-90, this repository is dedicated to advanced automation engineering, framework architecture, and interview readiness.

---

##  Repository Structure

* `days-91-180/` - Daily coding practice, advanced algorithm exercises, and technical challenges.
* `projects/` - End-to-end production-grade automation frameworks:
  * `project-1-ecommerce-automation/` - E-commerce UI/UX automated testing suites.
  * `project-2-api-testing/` - Advanced API testing & backend synchronization.
  * `project-3-payment-integration/` - End-to-end payment gateway validation (Stripe & microservices).
* `interview-prep/` - Technical Q&A, system architecture notes, and mock scenarios.

---

##  Tech Stack & Tools
* **Language:** Python 3
* **Automation:** Selenium WebDriver, Pytest
* **Backend & DB:** REST APIs (Stripe), SQLite3
* **Environment & Tools:** macOS Terminal, Git, GitHub, uTest Platform (Bronze Rated)

---

##  Previous Phase
*  **Phase 1 (Days 1-90):** [Fintech Learning Foundation](https://github.com/pkhaladzealex-eng/fintech-learning)

---

## 📅 Phase 2 Progress Log

### 🛒 Day 91: DemoBlaze E-Commerce Automated UI Flow
* **Objective:** Automate product selection, cart insertion, browser alert handling, and verification.
* **Key Actions:**
  * Used `WebDriverWait` with explicit conditions (`EC.element_to_be_clickable`).
  * Managed browser pop-up using `driver.switch_to.alert`.
  * Captured automated evidence screenshot of the shopping cart.
* **Files:**
  * 📜 [Automation Script](./days-91-180/day91.py)
  * 📸 [Cart Verification Screenshot](./days-91-180/demoblaze_cart.png)

---

### ⚡ Day 92: Refactoring UI Wait Logic (Zero Hardcoded Sleep)
* **Objective:** Remove all `time.sleep()` calls and replace them with explicit wait conditions[cite: 4].
* **Key Actions:**
  * Replaced fixed pauses with dynamic waits like `EC.alert_is_present()` and `EC.presence_of_element_located()`[cite: 4].
  * Ensured cart elements are loaded before capturing screenshots.
  * Improved execution speed and overall test reliability.
* **Files:**
  * 📜 [Refactored Script](./days-91-180/day92.py)
  * 📸 [Cart Verification Screenshot](./days-91-180/demoblaze_cart.png)

---

### 🧪 Day 93: Pytest Integration with Driver Fixtures
* **Objective:** Convert the standalone Selenium script into a structured Pytest test suite using fixtures.
* **Key Actions:**
  * Created a `@pytest.fixture` for browser setup, window maximization, and automated teardown (`yield` / `driver.quit()`).
  * Structured test flow with explicit assertions (`assert` on title, product URL, alert text, and cart page URL).
  * Maintained dynamic explicit waits and captured automated screenshot evidence upon success.
* **Files:**
  * 📜 [Pytest Script](./days-91-180/test_ecommerce_flow.py)
  * 📸 [Cart Verification Screenshot](./days-91-180/demoblaze_cart.png)

---

### 🗑️ Day 94: End-to-End Item Removal & Cart State Assertions
* **Objective:** Expand the Pytest suite with a second automated test to verify item deletion from the shopping cart.
* **Key Actions:**
  * Added `test_add_product_to_cart_and_remove` using XPATH locators for specific product targeting (`HTC One M9`)
  * Handled dynamic DOM changes using `EC.staleness_of` to confirm element removal after clicking 'Delete'.
  * Validated empty cart state with explicit assertion (`len(remaining_items) == 0`).
* **Files:**
  * 📜 [Pytest Script Suite](./days-91-180/test_ecommerce_flow.py)
  * 📸 [Cart Removal Screenshot Evidence](./days-91-180/demoblaze_cart_01.png)

---

### 🛠️ Day 95: Helper Utilities Refactoring (DRY Principle)
* **Objective:** Extract common Selenium UI actions into a separate utility module (`ecommerce_utils.py`) to reduce duplication.
* **Key Actions:**
  * Created reusable helper functions for opening site, clicking products by name, adding items, navigating to cart, and deleting items.
  * Refactored `test_ecommerce_flow.py` to import and utilize `ecommerce_utils` helper functions.
  * Kept assertions and test flows intact while keeping test methods clean and readable.
* **Files:**
  * 📜 [Helper Utilities File](./days-91-180/ecommerce_utils.py)
  * 📜 [Refactored Pytest Suite](./days-91-180/test_ecommerce_flow.py)
  
---

### 💳 Day 96: E-Commerce Payment Checkout & Order Completion
* **Objective:** Automate the complete end-to-end purchasing process from product selection to payment checkout and order confirmation.
* **Key Actions:**
  * Added checkout-specific helper functions (`click_place_order`, `fill_checkout_form`) to `ecommerce_utils.py.
  * Validated checkout modal display and populated order details dynamically without using hardcoded sleeps.
  * Asserted post-purchase success header (`Thank you for your purchase!`) and captured screenshot confirmation.
* **Files:**
  * 📜 [Payment Checkout Test](./days-91-180/test_payment_checkout.py)
  * 📜 [Updated Utilities Module](./days-91-180/ecommerce_utils.py)
  * 📸 [Purchase Confirmation Screenshot](./days-91-180/demoblaze_purchase.png)


---

### ⚠️ Day 97: Negative Checkout Flow & Alert Validation
* **Objective:** Test negative path handling during checkout when mandatory payment details are missing.
* **Key Actions:**
  * Created helper function `setup_and_add_to_cart` in `ecommerce_utils.py` to streamline multi-step test prerequisites.
  * Added `test_checkout_with_invalid_card` to attempt checkout with missing card information.
  * Validated system alert popup (`Please fill out Name and Creditcard.`) and handled browser alert dismissal.
* **Files:**
  * 📜 [Payment Checkout Test Suite](./days-91-180/test_payment_checkout.py)
  * 📜 [Updated Utilities Module](./days-91-180/ecommerce_utils.py)
  * 📸 [Invalid Checkout Screenshot](./days-91-180/demoblaze_invalid_checkout.png)