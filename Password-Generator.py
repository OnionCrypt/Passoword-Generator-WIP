# Libraries
import random
import string
from mnemonic import Mnemonic
import secrets
import time


# Creates a function
def passwordgen():
    length = int(input("Choose length for password: "))
    password = ""

    # The logic for the password generator, by combining letters, digits,
    # special characters and lower and uppercase.
    for _ in range(length):
        password += random.choice(string.ascii_letters + string.digits + string.punctuation)

    print("Generated password:", password)


def advanced_password():
    mnemo = Mnemonic("english")
    while True:
        try:
            length = int(input("Choose advanced password length (12, 18, 24 words): "))
            if length not in [12, 18, 24]:
                print("❌ Invalid length. Choose 12, 18, or 24.")
                continue
            entropy_bits = {12: 128, 18: 192, 24: 256}[length]
            entropy = secrets.token_bytes(entropy_bits // 8)
            phrase = mnemo.to_mnemonic(entropy)
            print("\n🔐 Your advanced mnemonic password:")
            print(phrase)
            return phrase
        except ValueError:
            print("❌ Please enter a valid number.")


# Ask user if they want to continue
def ask_continue():
    choice = input("\nDo you want to generate another password? (y/n): ").strip().lower()
    return choice == "y"


# Main password choice menu
def passwordchoice():
    while True:
        print("\n🔑 Password Generator")
        print("1. Normal password")
        print("2. Advanced mnemonic password")
        choice = input("Choose (1 or 2): ").strip()
        if choice == "1":
            passwordgen()
        elif choice == "2":
            advanced_password()
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
            continue

        if not ask_continue():
            print("\nGoodbye! 🔒")
            break
        
if __name__ == "__main__":
    passwordchoice()




#test 