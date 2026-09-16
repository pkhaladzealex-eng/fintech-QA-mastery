"""
Day 109: Database transaction testing.

Tests that multi-step database operations behave correctly when something
fails partway through - the core guarantee of a transaction is that it's
all-or-nothing, and that's what's verified here.

Design notes:
- Each test gets its OWN temporary database (via the `db_conn` fixture),
  created fresh and thrown away afterwards. Writing to the real
  fintech_main.db would leave test rows behind and make the second run
  fail on duplicate primary keys.
- Every test asserts against what's ACTUALLY in the database afterwards.
  A bare `assert True` would pass even if the transaction silently did
  nothing, which defeats the purpose of the test.
"""
import sqlite3
import tempfile
import os

import pytest


@pytest.fixture
def db_conn():
    """
    Fresh, isolated SQLite database per test, with the schema the payment
    flow expects and one seeded customer to update against.
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE payments (
            payment_id TEXT PRIMARY KEY,
            amount INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)
    # CHECK constraint gives us a realistic, genuinely-failing operation to
    # test rollback against (see test_rollback_on_constraint_violation).
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            balance INTEGER NOT NULL CHECK (balance >= 0)
        )
    """)
    cursor.execute("INSERT INTO customers (id, balance) VALUES (?, ?)", (1, 10000))
    conn.commit()

    yield conn

    conn.close()
    os.remove(path)


def test_successful_transaction(db_conn):
    """A multi-step transaction that commits should persist BOTH changes."""
    cursor = db_conn.cursor()

    cursor.execute("BEGIN TRANSACTION")
    cursor.execute(
        "INSERT INTO payments (payment_id, amount, status) VALUES (?, ?, ?)",
        ("charge_1", 5000, "succeeded"),
    )
    cursor.execute(
        "UPDATE customers SET balance = balance - ? WHERE id = ?", (5000, 1)
    )
    cursor.execute("COMMIT")

    # Assert against real data, not `assert True` - confirm the payment row
    # landed AND the balance actually moved.
    cursor.execute("SELECT amount, status FROM payments WHERE payment_id = ?", ("charge_1",))
    payment = cursor.fetchone()
    assert payment is not None, "Payment should exist after commit"
    assert payment[0] == 5000
    assert payment[1] == "succeeded"

    cursor.execute("SELECT balance FROM customers WHERE id = ?", (1,))
    assert cursor.fetchone()[0] == 5000, "Balance should be reduced by the payment amount"


def test_transaction_rollback_on_error(db_conn):
    """An explicit ROLLBACK should undo work already done in the transaction."""
    cursor = db_conn.cursor()

    cursor.execute("BEGIN TRANSACTION")
    cursor.execute(
        "INSERT INTO payments (payment_id, amount, status) VALUES (?, ?, ?)",
        ("charge_2", 3000, "succeeded"),
    )

    with pytest.raises(sqlite3.OperationalError):
        cursor.execute("INVALID SQL STATEMENT")

    db_conn.rollback()

    cursor.execute("SELECT * FROM payments WHERE payment_id = ?", ("charge_2",))
    assert cursor.fetchone() is None, "Payment should not exist after rollback"


def test_rollback_on_constraint_violation(db_conn):
    """
    A partial transaction that hits a real constraint violation must leave
    the database completely untouched.

    Note on the failure used here: a naive "UPDATE ... WHERE id = 99999"
    does NOT raise in SQLite - it just matches zero rows and succeeds
    quietly, so it can't test rollback at all. Overdrawing the balance past
    the CHECK (balance >= 0) constraint is a failure that genuinely raises,
    and mirrors a real business rule.
    """
    cursor = db_conn.cursor()

    cursor.execute("SELECT balance FROM customers WHERE id = ?", (1,))
    starting_balance = cursor.fetchone()[0]

    try:
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute(
            "INSERT INTO payments (payment_id, amount, status) VALUES (?, ?, ?)",
            ("charge_3", 999999, "succeeded"),
        )
        # Overdraws the account - violates CHECK (balance >= 0) and raises.
        cursor.execute(
            "UPDATE customers SET balance = balance - ? WHERE id = ?", (999999, 1)
        )
        cursor.execute("COMMIT")
        pytest.fail("Expected an IntegrityError from the balance constraint")
    except sqlite3.IntegrityError:
        db_conn.rollback()

    # Neither half of the transaction should have survived.
    cursor.execute("SELECT * FROM payments WHERE payment_id = ?", ("charge_3",))
    assert cursor.fetchone() is None, "Payment should be rolled back with the failed update"

    cursor.execute("SELECT balance FROM customers WHERE id = ?", (1,))
    assert cursor.fetchone()[0] == starting_balance, "Balance must be unchanged after rollback"


def test_duplicate_payment_id_is_rejected(db_conn):
    """
    Inserting the same payment_id twice must fail on the PRIMARY KEY
    constraint - this is what stops a retried webhook or a double-clicked
    button from recording the same charge twice.
    """
    cursor = db_conn.cursor()

    cursor.execute(
        "INSERT INTO payments (payment_id, amount, status) VALUES (?, ?, ?)",
        ("charge_4", 2000, "succeeded"),
    )
    db_conn.commit()

    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            "INSERT INTO payments (payment_id, amount, status) VALUES (?, ?, ?)",
            ("charge_4", 7777, "succeeded"),
        )
    db_conn.rollback()

    # The original row must be intact - not overwritten by the failed insert.
    cursor.execute("SELECT amount FROM payments WHERE payment_id = ?", ("charge_4",))
    assert cursor.fetchone()[0] == 2000
    