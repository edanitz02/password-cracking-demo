import hashlib
import csv
import sys

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_rainbow_table(PASSWORD_FILE, RAINBOW_FILE):
    with open(PASSWORD_FILE, "r") as pf:
        passwords = [line.strip() for line in pf if line.strip()]

    with open(RAINBOW_FILE, "w", newline="") as rf:
        writer = csv.writer(rf)
        writer.writerow(["hash", "password"])

        for pwd in passwords:
            hashed = hash_password(pwd)
            writer.writerow([hashed, pwd])
            print(f"Hashed: {pwd} -> {hashed}")

    print("\nRainbow table generated successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generateRainbow.py <file> <file>")
        sys.exit(1)
    generate_rainbow_table(sys.argv[1], sys.argv[2])
