import os
import stripe

stripe_key = os.environ.get("STRIPE_API_KEY", "")
client = stripe.StripeClient(stripe_key) if stripe_key else None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "fintech_main.db")
LOG_FILE_PATH = os.path.join(BASE_DIR, "..", "logs", "payment_logs.txt")

WEBHOOK_TIMEOUT = 30