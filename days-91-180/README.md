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

## 🧪 Tests & Files Directory

* [demoblaze/](demoblaze/) - Dedicated directory containing modular test suites and utilities for the DemoBlaze e-commerce platform.
  * [demoblaze/utils.py](demoblaze/utils.py) - Reusable helper functions for UI navigation, data extraction, Stripe API integration, and SQLite database logging.
  * [demoblaze/config.py](demoblaze/config.py) - Environment configurations, base URLs, element selectors, and database paths.
  * [demoblaze/test_ecommerce_flow.py](demoblaze/test_ecommerce_flow.py) - Pytest suite for e-commerce cart management (adding items, verifying cart content, removing items with `staleness_of` assertions).
  * [demoblaze/test_payment_checkout.py](demoblaze/test_payment_checkout.py) - Order completion suite validating purchase modals and mandatory field alerts.
  * [demoblaze/test_full_payment_integration.py](demoblaze/test_full_payment_integration.py) - Full 3-layer integration test connecting Selenium UI automation, Stripe API charges, and SQLite DB assertions.
  * [demoblaze/test_payment_error_handling.py](demoblaze/test_payment_error_handling.py) - Multi-layer error handling test simulating declined cards via Stripe API and verifying DB logging.
* [practicesoftwaretesting/](practicesoftwaretesting/) - E2E automation suite for the ToolShop Demo platform.
  * [practicesoftwaretesting/utils.py](practicesoftwaretesting/utils.py) - Helper utilities for guest registration, billing details, and credit card processing.
  * [practicesoftwaretesting/config.py](practicesoftwaretesting/config.py) - Centralized locators and guest user test data.
  * [practicesoftwaretesting/test_checkout.py](practicesoftwaretesting/test_checkout.py) - Complete multi-step guest checkout E2E test.
* [stripe-api-testing/](stripe-api-testing/) - Pure API test suite targeting Stripe PaymentIntents and Refunds.
  * [stripe-api-testing/config.py](stripe-api-testing/config.py) - StripeClient initialization and environment setup.
  * [stripe-api-testing/test_stripe_api.py](stripe-api-testing/test_stripe_api.py) - Pure API tests (successful charges, declined cards, refunds, and charge listing).
* [conftest.py](conftest.py) - Pytest configuration module providing session-scoped `browser` fixture and automated test logging (`autouse=True`).
* [day91.py](day91.py) - Initial basic Selenium automation script for DemoBlaze.
* [day92.py](day92.py) - Refactored automation script using dynamic explicit waits.
* [day100-milestone.md](day100-milestone.md) - Milestone reflection documenting 100 days of consistency, 226 total commits, skill progress, and roadmap for the next 80 days.

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
* **Full-Stack Integration Testing:** Combined Web UI data extraction, Stripe API payment processing, and SQLite DB verification into a single test asserting data integrity across all three layers (`UI Price == Stripe Amount == DB Amount`).
* **Multi-Layer Error Handling:** Validated failed payment workflows end-to-end by handling `stripe.error.CardError` exceptions, extracting failed charge IDs, and asserting consistent failure statuses (`failed`) across API responses and database records.
* **Modular Project Architecture:** Structured test suites into application-specific directories (`/demoblaze/`), separating reusable helpers, configurations, and test modules for cleaner maintainability.
* **Cross-Platform Test Adaptability:** Demonstrated ability to build scalable, platform-independent test suites by introducing a second e-commerce platform (`practicesoftwaretesting`) using separate utility modules and locator configurations.
* **Pure API Test Automation:** Built UI-independent API test suites using Stripe SDK (`StripeClient`), validating end-to-end payment intent creation, error handling (`CardError`), refund processing, and pagination/listing responses.


---

##  Next Steps in Phase 2
* **Days 98-105:** Page Object Model (POM) architecture implementation for UI tests.
* **Days 106-120:** API testing with Pytest, `requests`, and automated JSON response assertions.
* **Days 121-150:** Integration testing with SQLite database verification and CI/CD workflow setup.

---

👉 **[Return to Main Repository README →](../README.md)**