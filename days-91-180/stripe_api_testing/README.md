# 💳 Stripe API Test Suite

This directory contains pure API automation tests for verifying Stripe payment workflows without UI overhead.

---

## 🧪 Included API Tests (`test_stripe_api.py`)
1. **`test_create_successful_charge`**: Validates PaymentIntent creation and immediate confirmation (`status = "succeeded"`).
2. **`test_create_declined_charge`**: Tests negative payment flows using `pm_card_visa_chargeDeclined` and asserts `stripe.CardError` exception handling.
3. **`test_retrieve_charge`**: Verifies PaymentIntent retrieval by ID and asserts data consistency across requests.
4. **`test_create_refund`**: Creates a successful payment and issues a full refund, asserting `refund.status = "succeeded"`.
5. **`test_list_charges`**: Creates multiple transactions and verifies the API list endpoint returns expected records.

---

## 🚀 How to Run Tests

Run this suite from the `days-91-180` directory:

```bash
pytest stripe-api-testing -v -s