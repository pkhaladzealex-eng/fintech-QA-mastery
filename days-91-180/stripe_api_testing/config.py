import os
import stripe

STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "")

if not STRIPE_API_KEY:
    raise RuntimeError(
        "STRIPE_API_KEY environment variable is not set. "
        "Set it locally (export STRIPE_API_KEY=sk_test_...) or make sure "
        "it's passed as a GitHub Actions secret before running the "
        "stripe-api-testing suite."
    )

# Single Stripe client for this suite - test_stripe_api.py used to create its
# own second client directly instead of importing this one, so the API key
# handling lived in two places.
client = stripe.StripeClient(STRIPE_API_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "fintech_main.db")

# Portable log path (works locally and on CI, not tied to one machine)
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, "payment_logs.txt")

WEBHOOK_TIMEOUT = 30