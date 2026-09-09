"""
Day 108: Advanced error handling & retry logic.

Tests how a Stripe API call behaves under retry logic built with tenacity:
- transient errors (rate limits, temporary API/connection issues) should be
  retried with exponential backoff
- a non-transient error (e.g. a declined card) should NOT be retried -
  retrying a failure that can never succeed just wastes time
- after exhausting all retry attempts, the original exception should
  propagate to the caller, not get silently swallowed

These tests use unittest.mock to simulate failures deterministically,
rather than relying on Stripe's real API to actually rate-limit or error
out on demand - that would make the test suite flaky and slow (exponential
backoff sleeping for real), and wouldn't reliably test the "max retries
exceeded" path at all.
"""
from unittest.mock import patch, MagicMock

import pytest
import stripe
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from stripe_api_testing import config as stripe_cfg

# Errors worth retrying: rate limits and temporary API/connection issues.
# APIConnectionError is a subclass of APIError, but listing both keeps the
# intent explicit for anyone reading this without needing to know Stripe's
# exact exception hierarchy.
RETRYABLE_ERRORS = (stripe.RateLimitError, stripe.APIError, stripe.APIConnectionError)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=3),
    retry=retry_if_exception_type(RETRYABLE_ERRORS),
    reraise=True,
)
def create_payment_intent_with_retry(amount, description):
    """
    Create a PaymentIntent, retrying up to 3 times with exponential backoff
    on transient Stripe errors. Non-retryable errors (e.g. CardError from a
    declined card) propagate immediately on the first attempt.
    `reraise=True` ensures the ORIGINAL Stripe exception is raised after
    retries are exhausted, instead of tenacity's own RetryError wrapper.
    """
    return stripe_cfg.client.v1.payment_intents.create({
        "amount": amount,
        "currency": "usd",
        "payment_method": "pm_card_visa",
        "confirm": True,
        "return_url": "https://example.com",
        "description": description,
    })


def test_retry_succeeds_after_transient_failures():
    """
    Simulate two transient failures (a connection error, then a rate
    limit) followed by success on the third attempt. The retry wrapper
    should recover automatically and return the successful result.
    """
    mock_success = MagicMock(id="pi_test_retry_success", status="succeeded")
    side_effects = [
        stripe.APIConnectionError("temporary network issue"),
        stripe.RateLimitError("rate limited"),
        mock_success,
    ]

    with patch.object(
        stripe_cfg.client.v1.payment_intents, "create", side_effect=side_effects
    ) as mock_create:
        result = create_payment_intent_with_retry(2000, "Test with retries")

    assert result.id == "pi_test_retry_success"
    assert result.status == "succeeded"
    assert mock_create.call_count == 3


def test_max_retries_exceeded_raises_original_error():
    """
    Simulate a transient error that NEVER resolves. After exhausting all
    3 attempts, the original APIError should propagate to the caller
    rather than retrying forever or being swallowed.
    """
    with patch.object(
        stripe_cfg.client.v1.payment_intents,
        "create",
        side_effect=stripe.APIError("persistent API error"),
    ) as mock_create:
        with pytest.raises(stripe.APIError):
            create_payment_intent_with_retry(2000, "Will fail after retries")

    assert mock_create.call_count == 3


def test_non_retryable_error_is_not_retried():
    """
    A CardError (e.g. a declined card) is not transient - no amount of
    retrying will make a declined card succeed. It should propagate
    immediately after exactly one attempt, not three.
    """
    with patch.object(
        stripe_cfg.client.v1.payment_intents,
        "create",
        side_effect=stripe.CardError("card declined", None, "card_declined"),
    ) as mock_create:
        with pytest.raises(stripe.CardError):
            create_payment_intent_with_retry(2000, "Should not retry")

    assert mock_create.call_count == 1