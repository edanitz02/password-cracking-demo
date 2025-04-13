import psycopg2
from psycopg2 import sql
import os
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

def create_accounts_table():
    # Connect to the new database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                PRIMARY KEY(username)
            );
        """)
        print("Table 'accounts' created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def main():
    create_database()
    create_accounts_table()

if __name__ == "__main__":
    main()
