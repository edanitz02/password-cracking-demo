import psycopg2
import hashlib
import os
import sys
from dotenv import load_dotenv # installed in a virtual environment

load_dotenv()  # Loads from .env file in the same directory

# PostgreSQL configuration
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def generate_salt(length=8):
    return os.urandom(length).hex()

def hash_with_salt(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def hash_all_passwords_with_salt(accounts):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    try:
        # Load accounts.sql (assumes plain passwords)
        with open(accounts, 'r') as f:
            cursor.execute(f.read())
            print(f"Loaded {accounts} successfully.")

        # Alter table to add `salt` column if it doesn't exist
        cursor.execute("""
            ALTER TABLE accounts
            ADD COLUMN IF NOT EXISTS salt VARCHAR(255);
        """)

        # Get all usernames and plain passwords
        cursor.execute("SELECT username, password FROM accounts;")
        users = cursor.fetchall()

        # For each user, generate salt, hash password, and update
        for username, password in users:
            salt = generate_salt()
            hashed = hash_with_salt(password, salt)

            cursor.execute(
                "UPDATE accounts SET password = %s, salt = %s WHERE username = %s;",
                (hashed, salt, username)
            )
            print(f"Salted + hashed password for {username}: {hashed}")

        print("All passwords salted and hashed successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python hash_salted.py <accounts.sql>")
    else:
        hash_all_passwords_with_salt(sys.argv[1])
