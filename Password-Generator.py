import sys
import random
import string
import secrets
from mnemonic import Mnemonic
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QTextEdit,
    QSpinBox, QHBoxLayout
)
from PySide6.QtCore import Qt


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
        
class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Generator")
        self.setFixedSize(400, 400)

        self.mnemo = Mnemonic("english")

        self.layout = QVBoxLayout()

        # Mode selection
        self.mode_label = QLabel("Select Password Type")
        self.layout.addWidget(self.mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Normal Password", "Advanced Mnemonic"])
        self.layout.addWidget(self.mode_combo)

        # Length selection
        self.length_label = QLabel("Password Length")
        self.layout.addWidget(self.length_label)

        self.length_spin = QSpinBox()
        self.length_spin.setRange(4, 128)
        self.length_spin.setValue(12)
        self.layout.addWidget(self.length_spin)

        # Generate button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_password)
        self.layout.addWidget(self.generate_button)

        # Output field
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        # Theme toggle
        theme_layout = QHBoxLayout()
        self.theme_button = QPushButton("Switch to Light Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        theme_layout.addWidget(self.theme_button)
        self.layout.addLayout(theme_layout)

        self.setLayout(self.layout)

        # Default theme
        self.dark_mode = True
        self.apply_dark_theme()

    def generate_password(self):
        mode = self.mode_combo.currentText()
        length = self.length_spin.value()

        if mode == "Normal Password":
            password = "".join(
                random.choice(string.ascii_letters + string.digits + string.punctuation)
                for _ in range(length)
            )
            self.output.setText(password)

        else:
            if length not in [12, 18, 24]:
                self.output.setText("Advanced mnemonic must be 12, 18, or 24 words.")
                return

            entropy_bits = {12: 128, 18: 192, 24: 256}[length]
            entropy = secrets.token_bytes(entropy_bits // 8)
            phrase = self.mnemo.to_mnemonic(entropy)
            self.output.setText(phrase)

    def toggle_theme(self):
        if self.dark_mode:
            self.apply_light_theme()
            self.theme_button.setText("Switch to Dark Mode")
        else:
            self.apply_dark_theme()
            self.theme_button.setText("Switch to Light Mode")
        self.dark_mode = not self.dark_mode

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #333333;
                border: 1px solid #555555;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QTextEdit, QLineEdit, QSpinBox, QComboBox {
                background-color: #2b2b2b;
                border: 1px solid #555555;
            }
        """)

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                font-size: 14px;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #cccccc;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #d6d6d6;
            }
            QTextEdit, QLineEdit, QSpinBox, QComboBox {z
                background-color: #ffffff;
                border: 1px solid #cccccc;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    passwordchoice()

