import subprocess
import hashlib
import sys
import os
import signal

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
JOHN_PATH = os.path.join(CURRENT_DIR, "john/john-1.8.0.9-jumbo-macosx_sse4/run/john")

def create_temp_hash_file(temp_file, username, password_hash):
    with open(temp_file, "w") as f:
        f.write(f"{username}:{password_hash}\n")

def run_john(temp_file):
    try:
        subprocess.run(
            ["arch", "-x86_64", JOHN_PATH, "--format=Raw-SHA256", temp_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=1200  # Stop after 20 minutes
        )
    except subprocess.TimeoutExpired:
        print("John timed out after 20 minutes.")

def show_cracked_passwords(temp_file):
    result = subprocess.run(
        ["arch", "-x86_64", JOHN_PATH, "--format=Raw-SHA256", "--show", temp_file],
        capture_output=True,
        text=True
    )
    print(result.stdout)

def cleanup_john():
    # Safely remove john.pot if it exists
    potfile = os.path.join(CURRENT_DIR, "john.pot")
    if os.path.exists(potfile):
        os.remove(potfile)

def main(temp_file):
    username = "testuser"

    try:
        while True:
            user_input = input("Enter password to test (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break

            password_hash = hashlib.sha256(user_input.encode()).hexdigest()
            create_temp_hash_file(temp_file, username, password_hash)

            run_john(temp_file)
            show_cracked_passwords(temp_file)

            cleanup_john()

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting cleanly.")
        cleanup_john()
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python john.py <temp_file>")
        sys.exit(1)

    main(sys.argv[1])