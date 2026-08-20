import os
import stripe

client = stripe.StripeClient(os.environ["STRIPE_API_KEY"])
DATABASE_PATH = '/Users/alexpkhaladze/desktop/fintech-learning/global_data/fintech_main.db'


LOG_FILE_PATH = '/Users/alexpkhaladze/desktop/fintech-QA-mastery/days-91-180/logs/payment_logs.txt'

WEBHOOK_TIMEOUT = 30