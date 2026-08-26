import os

STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', 'st_test_mock_key_12345')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "fintech_main.db")

# Portable log path - works locally AND on CI (was hardcoded to a local Mac path before)
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, "payment_logs.txt")

WEBHOOK_TIMEOUT = 30

# Centralized explicit-wait timeout - was hardcoded as 10 or 15 inconsistently
# across test files. Change once here instead of in every test.
DEFAULT_WAIT = 15