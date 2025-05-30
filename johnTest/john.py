import subprocess
import hashlib
import sys
import os

JOHN_PATH = "/opt/john/run/john"

def create_temp_hash_file(temp_file, username, password_hash):
    with open(temp_file, "w") as f:
        f.write(f"{username}:{password_hash}\n")

def run_john(temp_file):
    try:
        subprocess.run(
            [JOHN_PATH, "--format=Raw-SHA256", temp_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=1200
        )
    except subprocess.TimeoutExpired:
        print("John timed out after 20 minutes.")

def show_cracked_passwords(temp_file):
    result = subprocess.run(
        [JOHN_PATH, "--format=Raw-SHA256", "--show", temp_file],
        capture_output=True,
        text=True
    )
    print(result.stdout)

def main(temp_file):
    username = "testuser"
    try:
        while True:
            user_input = input("Enter password to test (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break

            print(f"[DEBUG] Hashing input: {user_input}")
            password_hash = hashlib.sha256(user_input.encode()).hexdigest()
            create_temp_hash_file(temp_file, username, password_hash)

            print(f"[DEBUG] Running John the Ripper on SHA-256 hash...")
            run_john(temp_file)
            show_cracked_passwords(temp_file)

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting cleanly.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python john_demo.py <temp_file>")
        sys.exit(1)

    main(sys.argv[1])
