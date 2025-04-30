import psycopg2
import os
import csv
import sys
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL configuration
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

RAINBOW_FILE = "rainbow.csv"

def load_rainbow_table(RAINBOW_FILE):
    table = {}
    with open(RAINBOW_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            table[row["hash"]] = row["password"]
    return table

def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def rainbow_attack(rainbow_table):
    conn = connect()
    cursor = conn.cursor()

    cracked_accounts = []

    try:
        cursor.execute("SELECT username, password FROM accounts;")
        users = cursor.fetchall()

        print("Starting rainbow table attack...\n")

        for username, stored_hash in users:
            cracked_password = rainbow_table.get(stored_hash)
            if cracked_password:
                print(f"CRACKED {username}: {cracked_password}")
                cracked_accounts.append((username, cracked_password))
            else:
                print(f"Failed to crack {username}")

    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
    return cracked_accounts

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rainbow.py <file>")
        sys.exit(1)
    table = load_rainbow_table(sys.argv[1])
    cracked = rainbow_attack(table)
    print("\nResults")
    for username, password in cracked:
        print(f"{username}: {password}")
