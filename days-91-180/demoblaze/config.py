import os

STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', 'st_test_mock_key_12345')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "fintech_main.db")


LOG_FILE_PATH = '/Users/alexpkhaladze/desktop/fintech-QA-mastery/days-91-180/logs/payment_logs.txt'

WEBHOOK_TIMEOUT = 30