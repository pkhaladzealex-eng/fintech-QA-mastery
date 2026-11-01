# Freelance Project 1: E-commerce Checkout Testing

> Simulated freelance project for my portfolio. The test sites are public practice
> websites. Findings are about these sites, not about a real client's product.

## 1. Context
A small online shop wants its checkout checked before a release. I work as a freelance
QA engineer. The shop is simulated by https://automationexercise.com (a public practice site).

## 2. Goal
Show how reliable the checkout is. I deliver automated tests and clear bug reports.

## 3. Scope
**In scope**
- Sign up and login
- Add products to the cart and open the cart
- Checkout and order confirmation
- Payment form: card number, expiry, CVC, name (positive and negative cases)
- Simple timing of the checkout flow

**Out of scope**
- Security and load testing
- Mobile and other browsers (Chrome only)
- Payment backend and bank systems

## 4. Environment
- Part A (manual + automated): https://automationexercise.com
- Part B (manual only): https://demo.pxp.io/dropin, a study of payment form validation
- Tools: Python, pytest, Selenium (exact versions in requirements.txt)
- Test data: only fake data and documented test cards. No real personal data or
  real card numbers. No passwords are stored in this repository.

## 5. Approach
1. Explore the site by hand and take notes.
2. Write a test plan: positive and negative cases.
3. Automate the checkout flow with pytest and Selenium (Part A).
4. Test the payment form by hand on the PXP demo (Part B).
5. Write bug reports for what I find.
6. Measure how long the checkout takes.

## 6. Expected behavior
There is no official spec, so I use these references:
- PCI Booking card validation docs: https://developers.pcibooking.net/docs/card-validation-error
- Salesforce card verification docs: https://documentation.b2c.commercecloud.salesforce.com/DOC2/topic/com.demandware.dochelp/DWAPI/pipeletapi/html/api/pipelet.VerifyPaymentCard.html
- PXP demo store docs and behavior: https://developer.pxp.io/guides/checkout/components/demo-store

Where no reference exists, the expected result is my assumption, and I say so in the bug report.

## 7. Deliverables
| File | Purpose |
|---|---|
| README.md | Project brief |
| requirements.txt | Dependencies |
| conftest.py | Shared fixtures |
| test_suite.py | Automated tests |
| bug_reports.md | Defects found |
| performance_results.txt | Timing results |

## 8. Assumptions and risks
- Practice sites can change at any time.
- Ads on the site may block clicks during automated tests.
- On the PXP demo, the card fields are inside a closed shadow root. Normal Selenium
  locators cannot reach them, so Part B is manual.
