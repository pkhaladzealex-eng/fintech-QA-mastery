import pytest
import stripe
import os

client = stripe.StripeClient(os.environ.get("STRIPE_API_KEY"))

def test_create_successful_charge():
    payment_intent = client.v1.payment_intents.create({
        "amount": 2000,
        "currency": "usd",
        "payment_method": "pm_card_visa",
        "confirm": True,
        "return_url": "https://example.com"
    })
    assert payment_intent.id is not None
    assert payment_intent.status == "succeeded"
    assert payment_intent.amount == 2000


def test_create_declined_charge():
    # 2. Create a charge (declined card)
    with pytest.raises(stripe.CardError) as exc_info:
        client.v1.payment_intents.create({
            "amount": 2000,
            "currency": "usd",
            "payment_method": "pm_card_visa_chargeDeclined",
            "confirm": True,
            "return_url": "https://example.com"
        })

    # Assertions
    err = exc_info.value.error
    assert err.payment_intent is not None



def test_retrieve_charge():
    # 3. Retrieve a charge
    created_pi = client.v1.payment_intents.create({
        "amount": 3000,
        "currency": "usd",
        "payment_method": "pm_card_visa",
        "confirm": True,
        "return_url": "https://example.com"
    })

    retrieved_pi = client.v1.payment_intents.retrieve(created_pi.id)

    # Assertions
    assert retrieved_pi.id == created_pi.id
    assert retrieved_pi.amount == created_pi.amount
    assert retrieved_pi.status == created_pi.status



def test_create_refund():
    # 4. Create a refund
    created_pi = client.v1.payment_intents.create({
        "amount": 2000,
        "currency": "usd",
        "payment_method": "pm_card_visa",
        "confirm": True,
        "return_url": "https://example.com"
    })

    refund = client.v1.refunds.create({
        "payment_intent": created_pi.id
    })

    # Assertions
    assert refund.status == "succeeded"


def test_list_charges():
    # 5. List charges
    for i in range(3):
        client.v1.payment_intents.create({
            "amount": 1000 * (i + 1),
            "currency": "usd",
            "payment_method": "pm_card_visa",
            "confirm": True,
            "return_url": "https://example.com"
        })

    payment_intents_list = client.v1.payment_intents.list(params={"limit": 10})

    # Assertions
    assert len(payment_intents_list.data) >= 3