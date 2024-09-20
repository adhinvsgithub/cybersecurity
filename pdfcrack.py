# python pdfcrack.py pdf_with_password.pdf
# python pdfcrack.py pdf_with_password.pdf wordlist.txt

import pikepdf
from tqdm import tqdm
import sys
import itertools
import string
import os

# the PDF file you want to crack its password
pdf_file = sys.argv[1]

# Define the character set for brute-force attack
charset = string.ascii_letters + string.digits + string.punctuation

# Set the maximum length for the brute-force attack (you can adjust this)
max_length = 4  # Customize this as needed

def generate_passwords():
    """Generate all possible passwords with increasing length for brute-force."""
    for length in range(1, max_length + 1):
        for password in itertools.product(charset, repeat=length):
            yield ''.join(password)

def crack_with_wordlist(wordlist_file):
    """Attempt to crack PDF password using a wordlist."""
    try:
        with open(wordlist_file, 'r') as file:
            passwords = [line.strip() for line in file]
        
        for password in tqdm(passwords, "Decrypting PDF"):
            try:
                # Try to open the PDF with the current password
                with pikepdf.open(pdf_file, password=password) as pdf:
                    # If successful, print the found password and break the loop
                    print(f"[+] Password found: {password}")
                    break
            except pikepdf.PasswordError:
                # Wrong password, continue trying
                continue
    except FileNotFoundError:
        print(f"Wordlist file '{wordlist_file}' not found.")
        sys.exit(1)

def crack_with_bruteforce():
    """Attempt to crack PDF password using brute-force."""
    for password in tqdm(generate_passwords(), "Decrypting PDF"):
        try:
            # Try to open the PDF with the current password
            with pikepdf.open(pdf_file, password=password) as pdf:
                # If successful, print the found password and break the loop
                print(f"[+] Password found: {password}")
                break
        except pikepdf.PasswordError:
            # Wrong password, continue trying
            continue

# Main logic
if len(sys.argv) == 3:
    # If a wordlist file is provided, use it for the attack
    wordlist_file = sys.argv[2]
    if os.path.exists(wordlist_file):
        crack_with_wordlist(wordlist_file)
    else:
        print(f"Wordlist file '{wordlist_file}' does not exist.")
else:
    # No wordlist provided, use brute-force attack
    print("No wordlist provided, proceeding with brute-force attack...")
    crack_with_bruteforce()
