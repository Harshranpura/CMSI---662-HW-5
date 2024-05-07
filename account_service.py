import sqlite3

def get_balance(account_number, owner):
    """Retrieve the balance for a given account number and owner."""
    try:
        with sqlite3.connect('bank.db') as con:
            cur = con.cursor()
            cur.execute('''
                SELECT balance FROM accounts WHERE id=? AND owner=?''',
                (account_number, owner))
            row = cur.fetchone()
            if row is None:
                return None
            return row[0]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

def do_transfer(source, target, amount):
    """Perform a transfer between two accounts, ensuring the transaction is atomic."""
    try:
        with sqlite3.connect('bank.db') as con:
            cur = con.cursor()
            # Check if the target account exists
            cur.execute('SELECT id FROM accounts WHERE id=?', (target,))
            if cur.fetchone() is None:
                return False

            # Start transaction
            cur.execute('BEGIN TRANSACTION')

            # Deduct from the source account
            cur.execute('UPDATE accounts SET balance=balance-? WHERE id=?', (amount, source))
            if cur.rowcount == 0:
                con.rollback()  # Roll back if no rows were updated
                return False

            # Add to the target account
            cur.execute('UPDATE accounts SET balance=balance+? WHERE id=?', (amount, target))
            if cur.rowcount == 0:
                con.rollback()  # Roll back if no rows were updated
                return False

            con.commit()
            return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        con.rollback()
        return False
