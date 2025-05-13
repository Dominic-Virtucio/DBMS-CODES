from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog, QApplication, QLabel, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from commuter_register_dialog import CommuterRegisterDialog
class LoginWindow(QWidget):
    login_successful = pyqtSignal(str, dict)

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Login")
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.75)
        height = int(screen.height() * 0.75)
        self.setFixedSize(width, height)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Set main background color: Very light blue (#E3F2FD)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#E3F2FD'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Spacer for vertical centering
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Centered form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(25)
        form_layout.setContentsMargins(60, 40, 60, 40)
        form_layout.setAlignment(Qt.AlignHCenter)

        # Title Label
        title_label = QLabel("Welcome to TARA KOMYUT! Please Log In")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1976D2;")
        title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title_label)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 18))
        self.username_input.setStyleSheet("background-color: #BBDEFB; padding: 10px; border-radius: 8px;")
        self.username_input.setMinimumHeight(48)
        form_layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 18))
        self.password_input.setStyleSheet("background-color: #BBDEFB; padding: 10px; border-radius: 8px;")
        self.password_input.setMinimumHeight(48)
        form_layout.addWidget(self.password_input)

        # Login Button
        login_btn = QPushButton("Login")
        login_btn.setFont(QFont("Arial", 18))
        login_btn.clicked.connect(self.attempt_login)
        login_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 8px;")
        login_btn.setMinimumHeight(48)
        form_layout.addWidget(login_btn)

        # Register Button
        register_btn = QPushButton("Register as Commuter")
        register_btn.setFont(QFont("Arial", 18))
        register_btn.clicked.connect(self.open_register_dialog)
        register_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 8px;")
        register_btn.setMinimumHeight(48)
        form_layout.addWidget(register_btn)

        main_layout.addLayout(form_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(main_layout)

    def open_register_dialog(self):
        dialog = CommuterRegisterDialog(self.db_manager)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Success", "Registration successful! You can now login.")

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        user = self.db_manager.authenticate_user(username, password)
        if user:
            self.login_successful.emit(user['user_type'], user)
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
