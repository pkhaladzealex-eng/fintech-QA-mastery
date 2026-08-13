```markdown
# Phase 2: Days 91-180 Detailed Progress & Test Suites

Welcome to the detailed log for Phase 2! This directory contains daily exercises, refactored test suites, helper modules, and automated execution evidence for e-commerce and payment flows.
```
---

## 📋 Phase 2 Overview
The focus of this phase is moving from simple scripts to production-grade automation patterns:
* Eliminating hardcoded pauses (`time.sleep`) in favor of dynamic explicit waits (`WebDriverWait`).
* Converting standalone scripts into modular **Pytest** test suites with reusable fixtures.
* Extracting common actions into helper utility modules (`ecommerce_utils.py`) to keep tests clean and DRY (Don't Repeat Yourself).
* Automating both positive happy-paths and negative validation scenarios (e.g., checkout without payment details).

---

## 🧪 Tests & Files Directory

* [day91.py](day91.py)  - Initial basic Selenium automation script for DemoBlaze (product selection and cart interaction).
* [day92.py](day92.py) - Refactored script with zero hardcoded sleeps using dynamic explicit wait conditions.
* [ecommerce_utils.py](ecommerce_utils.py) - Reusable helper module containing UI interaction functions (navigation, product selection, checkout, alert handling).
* [test_ecommerce_flow.py](test_ecommerce_flow.py) - Pytest suite for e-commerce cart management (adding items, verifying cart content, removing items with `staleness_of` assertions).
* [test_payment_checkout.py](test_payment_checkout.py) - Pytest suite for order completion (filling checkout forms, validating purchase modals, and handling missing payment detail alerts).
* [conftest.py](conftest.py) - Pytest configuration module providing session-scoped `browser` fixture and automated test logging (`autouse=True`)
* [day100-milestone.md](day100-milestone.md) - Milestone reflection documenting 100 days of consistency, 226 total commits, skill progress, and roadmap for the next 80 days.
---

## 🚀 How to Run Tests

Ensure you are inside the `days-91-180` directory, then run the Pytest suite using:

```bash
pytest . -v -s
```
## 🛠️ Key QA Automation Skills Demonstrated

* **Explicit Waits:** Leveraging WebDriverWait with EC.element_to_be_clickable, EC.presence_of_element_located, EC.alert_is_present, and EC.staleness_of.

* **Pytest Fixtures:** Reusable @pytest.fixture for driver setup, browser maximization, and clean teardown (yield / driver.quit()).

* **Modular Code Structure:** Reusable helper functions inside ecommerce_utils.py.

* **Positive & Negative Path Testing:** Validating successful purchase confirmation vs. missing payment alert popups.

* **Dynamic DOM Assertions:** Verifying element state changes and item counts after cart deletions.

## 📸 Test Execution Evidence & Screenshots
[demoblaze_cart.png](demoblaze_cart.png) - Verification of item successfully added to the shopping cart.

[demoblaze_cart_01.png](demoblaze_cart_01.png) - Verification of cart state after item removal.

[demoblaze_purchase.png](demoblaze_purchase.png) - Confirmation modal after filling checkout details and placing an order.

[demoblaze_invalid_checkout.png](demoblaze_invalid_checkout.png) - Alert validation popup when attempting checkout with missing mandatory fields.

---

##  Next Steps in Phase 2
* **Days 98-105:** Page Object Model (POM) architecture implementation for UI tests.
* **Days 106-120:** API testing with Pytest, `requests`, and automated JSON response assertions.
* **Days 121-150:** Integration testing with SQLite database verification and CI/CD workflow setup.

---

👉 **[Return to Main Repository README →](../README.md)**