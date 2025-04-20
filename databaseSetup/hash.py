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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def hash_all_passwords(accounts):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    try:
        # Load the SQL file with plain passwords
        with open(accounts, 'r') as f:
            cursor.execute(f.read())
            print(f"Loaded {accounts} successfully.")

        # Select all users and their plain passwords
        cursor.execute("SELECT username, password FROM accounts;")
        users = cursor.fetchall()

        # Hash and update passwords
        for username, password in users:
            hashed = hash_password(password)
            cursor.execute(
                "UPDATE accounts SET password = %s WHERE username = %s;",
                (hashed, username)
            )
            print(f"Hashed password for {username}: {hashed}")

        # Success
        print("All passwords hashed successfully.")

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
        hash_all_passwords(sys.argv[1])
