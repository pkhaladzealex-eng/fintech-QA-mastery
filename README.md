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

![DemoBlaze Cart Verification](./days-91-180/demoblaze_cart.png)