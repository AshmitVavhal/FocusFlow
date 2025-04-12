import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QSize


DATA_FILE = "datasheet.txt"


def save_user_data(name, username, email, password):
    with open(DATA_FILE, "a") as f:
        f.write(f"Full Name: {name}\n")
        f.write(f"Username: {username}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Password: {password}\n")
        f.write("---\n")


def is_user_registered(email, password):
    if not os.path.exists(DATA_FILE):
        return False

    with open(DATA_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for i in range(0, len(lines), 5):
        try:
            email_line = lines[i + 2].split("Email: ")[1].strip()
            password_line = lines[i + 3].split("Password: ")[1].strip()
            if email_line == email and password_line == password:
                return True
        except IndexError:
            continue

    return False


class SignupScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Light Theme Sign Up")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        image_label = QLabel()
        pixmap = QPixmap("bg.png")
        image_label.setPixmap(pixmap.scaled(500, 600, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(image_label)

        signup_container = QWidget()
        signup_container.setStyleSheet("background-color: #ffffff; border-top-left-radius: 30px; border-bottom-left-radius: 30px;")
        signup_container.setFixedWidth(500)
        signup_layout = QVBoxLayout()

        welcome_label = QLabel("Create Account")
        welcome_label.setFont(QFont("Arial", 22, QFont.Bold))
        welcome_label.setStyleSheet("color: #1d1b31;")
        welcome_label.setAlignment(Qt.AlignLeft)

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(15)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.name_input.setStyleSheet("padding: 12px; border-radius: 10px; border: 1px solid #ccc;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 12px; border-radius: 10px; border: 1px solid #ccc;")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setStyleSheet("padding: 12px; border-radius: 10px; border: 1px solid #ccc;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 12px; border-radius: 10px; border: 1px solid #ccc;")

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setStyleSheet("padding: 12px; border-radius: 10px; border: 1px solid #ccc;")

        form_layout.addRow(self.name_input)
        form_layout.addRow(self.username_input)
        form_layout.addRow(self.email_input)
        form_layout.addRow(self.password_input)
        form_layout.addRow(self.confirm_input)

        signup_btn = QPushButton("Sign Up")
        signup_btn.setStyleSheet("padding: 12px; border-radius: 10px; background-color: #1d1b31; color: white; font-weight: bold;")
        signup_btn.clicked.connect(self.handle_signup)

        terms_label = QLabel()
        terms_label.setTextFormat(Qt.RichText)
        terms_label.setOpenExternalLinks(True)
        terms_label.setText(
            '<div style="font-size: 12px; color: #888888; text-align: center;">'
            'By creating an account you agree to FocusFlow '
            '<a href="https://example.com/terms" style="color:#1a73e8;">terms of service</a> '
            'and '
            '<a href="https://example.com/privacy" style="color:#1a73e8;">privacy policy</a>.'
            '</div>'
        )
        terms_label.setAlignment(Qt.AlignCenter)

        signup_layout.addSpacing(30)
        signup_layout.addWidget(welcome_label)
        signup_layout.addSpacing(20)
        signup_layout.addLayout(form_layout)
        signup_layout.addSpacing(10)
        signup_layout.addWidget(signup_btn)
        signup_layout.addWidget(terms_label)
        signup_layout.addStretch()

        signup_container.setLayout(signup_layout)
        main_layout.addWidget(signup_container)
        self.setLayout(main_layout)

    def handle_signup(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not all([name, username, email, password, confirm]):
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        save_user_data(name, username, email, password)
        QMessageBox.information(self, "Success", "Registration successful!")
        self.close()
        self.login_window = LoginScreen()
        self.login_window.show()


class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Light Theme Login")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        image_label = QLabel()
        pixmap = QPixmap("bg.png")
        image_label.setPixmap(pixmap.scaled(500, 600, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(image_label)

        login_container = QWidget()
        login_container.setStyleSheet("background-color: #ffffff; border-top-left-radius: 30px; border-bottom-left-radius: 30px;")
        login_container.setFixedWidth(500)
        login_layout = QVBoxLayout()

        welcome_label = QLabel("FocusFlow")
        welcome_label.setFont(QFont("Arial", 22, QFont.Bold))
        welcome_label.setStyleSheet("color: #1d1b31;")
        welcome_label.setAlignment(Qt.AlignCenter)

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(15)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setStyleSheet("padding: 12px; border-radius: 10px; border: 1px solid #ccc;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 12px; border-radius: 10px; border: 1px solid #ccc;")

        form_layout.addRow(self.email_input)
        form_layout.addRow(self.password_input)

        forgot_label = QLabel("Forgot Password?")
        forgot_label.setStyleSheet("color: #1d1b31; font-size: 13px;")

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet("padding: 12px; border-radius: 10px; background-color: #1d1b31; color: white; font-weight: bold;")
        login_btn.clicked.connect(self.handle_login)

        logo_layout = QHBoxLayout()
        for icon_path in ["google.png", "meta.png", "apple.png"]:
            btn = QPushButton()
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(30, 30))
            btn.setFixedSize(50, 50)
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    background-color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            logo_layout.addWidget(btn, alignment=Qt.AlignCenter)

        signup_label = QLabel("Don’t have an account? <a href='#'>Sign up</a>")
        signup_label.setOpenExternalLinks(False)
        signup_label.setStyleSheet("color: #1d1b31; font-size: 13px;")
        signup_label.setAlignment(Qt.AlignCenter)
        signup_label.linkActivated.connect(self.open_signup)

        login_layout.addSpacing(50)
        login_layout.addWidget(welcome_label)
        login_layout.addSpacing(30)
        login_layout.addLayout(form_layout)
        login_layout.addWidget(forgot_label)
        login_layout.addSpacing(10)
        login_layout.addWidget(login_btn)
        login_layout.addSpacing(15)
        login_layout.addLayout(logo_layout)
        login_layout.addSpacing(20)
        login_layout.addWidget(signup_label)
        login_layout.addStretch()

        login_container.setLayout(login_layout)
        main_layout.addWidget(login_container)
        self.setLayout(main_layout)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter email and password.")
            return

        if is_user_registered(email, password):
            QMessageBox.information(self, "Login Successful", "Welcome back!")
            self.close()
            subprocess.Popen([sys.executable, "4.py", email])

        else:
            QMessageBox.critical(self, "Login Failed", "User not found.")



    def open_signup(self):
        self.signup_window = SignupScreen()
        self.signup_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec_())
