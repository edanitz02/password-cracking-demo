import psycopg2
import os
import hashlib
import itertools
import sys
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL configuration
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

CHARSET = 'eariotnslcEARIOTNSLC0123456789'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def hash_with_salt(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def get_accounts(conn):
    cursor = conn.cursor()
    
    # Check for salt column
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name='accounts' AND column_name='salt';
    """)
    salted = cursor.fetchone() is not None

    if salted:
        cursor.execute("SELECT username, password, salt FROM accounts;")
        accounts = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
    else:
        cursor.execute("SELECT username, password FROM accounts;")
        accounts = {row[0]: (row[1], None) for row in cursor.fetchall()}

    cursor.close()
    return accounts, salted

def brute_force_crack(accounts, salted, max_length):
    print(f"Starting real brute-force attack (max length: {max_length})...\n")
    cracked_accounts = []

    for username, (stored_pw, salt) in accounts.items():
        print(f"Cracking: {username}")
        cracked = False

        for length in range(1, max_length + 1):
            for guess_tuple in itertools.product(CHARSET, repeat=length):
                guess = ''.join(guess_tuple)

                # Hashing appropriately
                if salt:
                    guess_hash = hash_with_salt(guess, salt)
                else:
                    guess_hash = hash_password(guess)

                if guess == stored_pw or guess_hash == stored_pw:
                    print(f"\nCRACKED {username}: {guess}")
                    cracked_accounts.append((username, guess))
                    cracked = True
                    break
            if cracked:
                break
        # if not cracked:
        #     print(f"Failed to crack {username}")
    return cracked_accounts

def main():
    if len(sys.argv) != 2:
        print("Usage: python brute_force.py <max_length>")
        sys.exit(1)

    try:
        max_length = int(sys.argv[1])
    except ValueError:
        print("Error: max_length must be an integer.")
        sys.exit(1)
    
    conn = connect()
    accounts, salted = get_accounts(conn)
    cracked = brute_force_crack(accounts, salted, max_length)
    conn.close()

    print("\nResults:")
    for username, password in cracked:
        print(f"{username}: {password}")

if __name__ == "__main__":
    main()
