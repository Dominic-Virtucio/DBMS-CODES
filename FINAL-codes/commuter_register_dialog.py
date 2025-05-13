from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QPushButton, QMessageBox, QVBoxLayout, QLabel
)

class CommuterRegisterDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Commuter Registration")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        # Set the main background color
        self.setStyleSheet("background-color: #E3F2FD;")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Form Fields
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("background-color: #BBDEFB;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("background-color: #BBDEFB;")
        self.first_name_input = QLineEdit()
        self.first_name_input.setStyleSheet("background-color: #BBDEFB;")
        self.last_name_input = QLineEdit()
        self.last_name_input.setStyleSheet("background-color: #BBDEFB;")
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("background-color: #BBDEFB;")

        # Add Rows with styled labels
        form_layout.addRow(self._make_label("Username*:"), self.username_input)
        form_layout.addRow(self._make_label("Password*:"), self.password_input)
        form_layout.addRow(self._make_label("First Name:"), self.first_name_input)
        form_layout.addRow(self._make_label("Last Name:"), self.last_name_input)
        form_layout.addRow(self._make_label("Email:"), self.email_input)

        # Register Button
        register_btn = QPushButton("Register")
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 8px 0px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        register_btn.clicked.connect(self.register_commuter)

        layout.addLayout(form_layout)
        layout.addWidget(register_btn)
        self.setLayout(layout)

    def _make_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("color: #1976D2; font-weight: bold;")
        return label

    def register_commuter(self):
        data = {
            'username': self.username_input.text().strip(),
            'password': self.password_input.text().strip(),
            'first_name': self.first_name_input.text().strip(),
            'last_name': self.last_name_input.text().strip(),
            'email': self.email_input.text().strip()
        }

        # Validation
        if not data['username'] or not data['password']:
            QMessageBox.warning(self, "Error", "Username and password are required")
            return

        try:
            self.db_manager.insert_commuter(
                username=data['username'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email']
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")