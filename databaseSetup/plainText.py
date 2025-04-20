import psycopg2
from psycopg2 import sql
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

def create_database():
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(
        dbname="postgres",  # Connect to the default 'postgres' database
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True  # Set autocommit to true for creating the database

    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print(f"Database '{DB_NAME}' created successfully!")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{DB_NAME}' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        conn.close()

def load_accounts_from_sql(accounts):
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    try:
        with open(accounts, 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.execute(sql_script)
            print(f"Executed SQL from '{accounts}' successfully!")
    except Exception as e:
        print(f"Error executing SQL file: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def main(accounts):
    create_database()
    load_accounts_from_sql(accounts)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plainText.py <accounts.sql>")
    else:
        main(sys.argv[1])
