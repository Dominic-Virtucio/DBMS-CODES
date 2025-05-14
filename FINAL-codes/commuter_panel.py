import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QFormLayout, QGroupBox, QMessageBox, QTableView, QHeaderView, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from routes_fares import FareCalculatorApp

class CommuterPanel(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, db_manager, user_data):
        super().__init__()
        self.db_manager = db_manager
        self.user_data = user_data
        self.commuter_id = self.user_data.get('commuter_id')
        self.user_id = self.user_data.get('user_id')
        self.setWindowTitle("Commuter Panel")
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.75)
        height = int(screen.height() * 0.75)
        self.setFixedSize(width, height)
        self.routes_fares_window = None
        self.init_ui()
        self.load_commuter_data()

    def init_ui(self):
        image_path = os.path.join(os.path.dirname(__file__), "OIP.jpg")
        image_path = image_path.replace("\\", "/")
        self.setStyleSheet("background-color: #E3F2FD;")
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        self.user_label = QLabel(f"Logged in as: Commuter ({self.user_data.get('username', 'N/A')})")
        self.user_label.setStyleSheet("color: #1976D2; font-weight: bold; font-size: 18px;")
        header_layout.addWidget(self.user_label)
        header_layout.addStretch()
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; font-weight: bold; border-radius: 6px; padding: 8px 22px; font-size: 16px; }"
            "QPushButton:hover { background-color: #1976D2; }"
        )
        self.logout_button.clicked.connect(self.logout_requested.emit)
        header_layout.addWidget(self.logout_button)
        main_layout.addLayout(header_layout)
        user_info_group = QGroupBox("My Information")
        user_info_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; font-size: 16px; }")
        user_info_outer_layout = QHBoxLayout()
        user_info_outer_layout.setAlignment(Qt.AlignHCenter)
        user_info_layout = QFormLayout()
        user_info_layout.setLabelAlignment(Qt.AlignRight)
        field_max_width = 400
        label_style = "color: #1976D2; font-weight: bold;"
        input_style = "background-color: #BBDEFB; border-radius: 5px; padding: 8px; font-size: 15px; color: #1976D2;"
        self.username_value = QLabel()
        self.username_value.setStyleSheet(label_style)
        user_info_layout.addRow(QLabel("Username:"), self.username_value)
        self.full_name_label = QLabel()
        self.full_name_label.setStyleSheet(label_style)
        user_info_layout.addRow(QLabel("Name:"), self.full_name_label)
        self.first_name_input = QLineEdit()
        self.first_name_input.setStyleSheet(input_style)
        self.first_name_input.setMaximumWidth(field_max_width)
        user_info_layout.addRow(QLabel("First Name:"), self.first_name_input)
        self.last_name_input = QLineEdit()
        self.last_name_input.setStyleSheet(input_style)
        self.last_name_input.setMaximumWidth(field_max_width)
        user_info_layout.addRow(QLabel("Last Name:"), self.last_name_input)
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(input_style)
        self.email_input.setMaximumWidth(field_max_width)
        user_info_layout.addRow(QLabel("Email:"), self.email_input)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)
        self.password_input.setMaximumWidth(field_max_width)
        user_info_layout.addRow(QLabel("Password:"), self.password_input)
        self.contact_input = QLineEdit()
        self.contact_input.setStyleSheet(input_style)
        self.contact_input.setMaximumWidth(field_max_width)
        user_info_layout.addRow(QLabel("Contact No:"), self.contact_input)
        self.discount_combo = QComboBox()
        self.discount_combo.setStyleSheet(input_style)
        self.discount_combo.setMaximumWidth(field_max_width)
        self.discount_combo.addItems(['None', 'Senior Citizen', 'PWD', 'Student'])
        user_info_layout.addRow(QLabel("Discount Type:"), self.discount_combo)
        self.preferred_route_combo = QComboBox()
        self.preferred_route_combo.setStyleSheet(input_style)
        self.preferred_route_combo.setMaximumWidth(field_max_width)
        user_info_layout.addRow(QLabel("Preferred Route:"), self.preferred_route_combo)
        self.update_info_button = QPushButton("Update Information")
        self.update_info_button.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; font-weight: bold; border-radius: 6px; padding: 8px 22px; font-size: 16px; }"
            "QPushButton:hover { background-color: #1976D2; }"
        )
        self.update_info_button.setMaximumWidth(field_max_width)
        self.update_info_button.clicked.connect(self.update_commuter_info)
        user_info_layout.addRow(self.update_info_button)
        user_info_group.setLayout(user_info_layout)
        user_info_outer_layout.addWidget(user_info_group)
        main_layout.addLayout(user_info_outer_layout)
        self.view_routes_fares_button = QPushButton("View Routes and Fares")
        self.view_routes_fares_button.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; font-weight: bold; border-radius: 6px; padding: 10px 30px; font-size: 18px; }"
            "QPushButton:hover { background-color: #1976D2; }"
        )
        self.view_routes_fares_button.setMaximumWidth(300)
        self.view_routes_fares_button.clicked.connect(self.open_routes_fares_window)
        main_layout.addWidget(self.view_routes_fares_button, alignment=Qt.AlignCenter)
        feedback_group = QGroupBox("Submit Feedback")
        feedback_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; font-size: 16px; }")
        feedback_outer_layout = QHBoxLayout()
        feedback_outer_layout.setAlignment(Qt.AlignHCenter)
        feedback_layout = QFormLayout()
        feedback_layout.setLabelAlignment(Qt.AlignRight)
        self.feedback_commuter_id_value = QLabel(str(self.commuter_id))
        self.feedback_commuter_id_value.setStyleSheet(label_style)
        feedback_layout.addRow(QLabel("Your Commuter ID:"), self.feedback_commuter_id_value)
        self.feedback_driver_combo = QComboBox()
        self.feedback_driver_combo.setStyleSheet(input_style)
        self.feedback_driver_combo.setMaximumWidth(field_max_width)
        feedback_layout.addRow(QLabel("Feedback for Driver:"), self.feedback_driver_combo)
        self.feedback_conductor_combo = QComboBox()
        self.feedback_conductor_combo.setStyleSheet(input_style)
        self.feedback_conductor_combo.setMaximumWidth(field_max_width)
        feedback_layout.addRow(QLabel("Feedback for Conductor:"), self.feedback_conductor_combo)
        self.feedback_rating_input = QLineEdit()
        self.feedback_rating_input.setStyleSheet(input_style)
        self.feedback_rating_input.setMaximumWidth(field_max_width)
        feedback_layout.addRow(QLabel("Rating (0-5):"), self.feedback_rating_input)
        self.feedback_comment_input = QLineEdit()
        self.feedback_comment_input.setStyleSheet(input_style)
        self.feedback_comment_input.setMaximumWidth(field_max_width)
        feedback_layout.addRow(QLabel("Comment:"), self.feedback_comment_input)
        self.submit_feedback_button = QPushButton("Submit Feedback")
        self.submit_feedback_button.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; font-weight: bold; border-radius: 6px; padding: 8px 22px; font-size: 16px; }"
            "QPushButton:hover { background-color: #1976D2; }"
        )
        self.submit_feedback_button.setMaximumWidth(field_max_width)
        self.submit_feedback_button.clicked.connect(self.submit_feedback)
        feedback_layout.addRow(self.submit_feedback_button)
        feedback_group.setLayout(feedback_layout)
        feedback_outer_layout.addWidget(feedback_group)
        main_layout.addLayout(feedback_outer_layout)
        my_feedbacks_group = QGroupBox("My Submitted Feedback")
        my_feedbacks_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; font-size: 16px; }")
        my_feedbacks_layout = QVBoxLayout()
        self.my_feedbacks_table = QTableView()
        self.my_feedbacks_table.setEditTriggers(QTableView.NoEditTriggers)
        self.my_feedbacks_table.setSelectionBehavior(QTableView.SelectRows)
        self.my_feedbacks_table_model = QStandardItemModel()
        self.my_feedbacks_table.setModel(self.my_feedbacks_table_model)
        self.my_feedbacks_table.verticalHeader().setVisible(False)
        self.my_feedbacks_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #1976D2; color: white; font-weight: bold; font-size: 14px; padding: 6px; border: 1px solid #BBDEFB; }"
        )
        self.my_feedbacks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        my_feedbacks_layout.addWidget(self.my_feedbacks_table)
        my_feedbacks_group.setLayout(my_feedbacks_layout)
        main_layout.addWidget(my_feedbacks_group)
        self.setLayout(main_layout)

    def open_routes_fares_window(self):
        if self.routes_fares_window is None:
            self.routes_fares_window = FareCalculatorApp(self.db_manager)
        self.routes_fares_window.show()
        self.routes_fares_window.raise_()
        self.routes_fares_window.activateWindow()

    def resize_table_view_uniform(self, table_view):
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        table_view.resizeRowsToContents()

    def populate_table_view(self, model, data, headers, table_view, keys=None):
        try:
            model.clear()
            model.setHorizontalHeaderLabels(headers)
            if data:
                if keys is None:
                    keys = headers
                for row_data in data:
                    row_dict = dict(row_data) if hasattr(row_data, 'keys') else row_data
                    items = [QStandardItem(str(row_dict.get(k, ""))) for k in keys]
                    for item in items:
                        item.setTextAlignment(Qt.AlignCenter)
                    model.appendRow(items)
            self.resize_table_view_uniform(table_view)
        except Exception as e:
            QMessageBox.critical(self, "Table Error", f"Could not populate table: {e}")

    def load_commuter_data(self):
        try:
            self.username_value.setText(self.user_data.get('username', 'N/A'))
            first_name = self.user_data.get('first_name', '')
            last_name = self.user_data.get('last_name', '')
            self.full_name_label.setText(f"{first_name} {last_name}")
            self.first_name_input.setText(first_name)
            self.last_name_input.setText(last_name)
            self.email_input.setText(self.user_data.get('email', ''))
            self.password_input.setText(self.user_data.get('password', ''))
            contact_val = self.user_data.get('contact_no')
            self.contact_input.setText("" if contact_val is None or str(contact_val) == "None" else str(contact_val))
            discount_type = self.user_data.get('discount_type', 'None')
            idx = self.discount_combo.findText(discount_type if discount_type else 'None')
            if idx >= 0:
                self.discount_combo.setCurrentIndex(idx)
            routes = self.db_manager.get_routes()
            self.preferred_route_combo.clear()
            self.preferred_route_combo.addItem("Select Preferred Route", None)
            current_preferred_route = self.user_data.get('preferred_route')
            try:
                if current_preferred_route is not None:
                    current_preferred_route = int(current_preferred_route)
            except (TypeError, ValueError):
                current_preferred_route = None
            selected_index = 0
            if routes:
                for i, route in enumerate(routes):
                    route_id = int(route['route_id'])
                    label = f"{route['origin']} to {route['destination']}"
                    self.preferred_route_combo.addItem(label, route_id)
                    if current_preferred_route == route_id:
                        selected_index = i + 1
            self.preferred_route_combo.setCurrentIndex(selected_index)
            self.populate_driver_combo()
            self.populate_conductor_combo()
            if hasattr(self.db_manager, 'get_commuter_feedbacks'):
                feedbacks = self.db_manager.get_commuter_feedbacks(self.commuter_id)
                if feedbacks:
                    feedbacks = [dict(feedback) for feedback in feedbacks]
                else:
                    feedbacks = []
                headers = ["Feedback ID", "Driver ID", "Conductor ID", "Rating", "Comment", "Date"]
                keys = ["feedback_id", "driver_id", "conductor_id", "rating", "comment", "date"]
                self.populate_table_view(
                    self.my_feedbacks_table_model,
                    feedbacks,
                    headers,
                    self.my_feedbacks_table,
                    keys=keys
                )
        except Exception as e:
            QMessageBox.critical(self, "Data Error", f"Failed to load data: {str(e)}")

    def update_commuter_info(self):
        try:
            user_id = self.user_data['user_id']
            self.db_manager.begin_transaction()
            users_success = self.db_manager.execute_insert_update_delete(
                '''UPDATE users
                SET first_name=?, last_name=?, email=?, password=?
                WHERE user_id=?''',
                (self.first_name_input.text().strip(),
                 self.last_name_input.text().strip(),
                 self.email_input.text().strip(),
                 self.password_input.text(),
                 user_id),
                commit=False
            )
            preferred_route = self.preferred_route_combo.currentData()
            try:
                preferred_route = int(preferred_route) if preferred_route else None
            except (TypeError, ValueError):
                preferred_route = None
            commuters_success = self.db_manager.execute_insert_update_delete(
                '''UPDATE commuters
                SET contact_no=?, discount_type=?, preferred_route=?
                WHERE user_id=?''',
                (self.contact_input.text().strip(),
                 self.discount_combo.currentText(),
                 preferred_route,
                 user_id),
                commit=False
            )
            if users_success and commuters_success:
                self.db_manager.commit_transaction()
                QMessageBox.information(self, "Success", "Profile updated successfully")
                fresh_user_data = self.db_manager.execute_query(
                    '''SELECT u.*, c.*
                    FROM users u
                    JOIN commuters c ON u.user_id = c.user_id
                    WHERE u.user_id = ?''',
                    (user_id,)
                )[0]
                self.user_data.update(dict(fresh_user_data))
                self.load_commuter_data()
            else:
                self.db_manager.rollback_transaction()
                QMessageBox.warning(self, "Error", "Failed to update profile")
        except Exception as e:
            self.db_manager.rollback_transaction()
            QMessageBox.critical(self, "Error", f"Update failed: {str(e)}")

    def populate_driver_combo(self):
        try:
            self.feedback_driver_combo.clear()
            self.feedback_driver_combo.addItem("Select Driver (Optional)", None)
            drivers = self.db_manager.get_all_driver_ids()
            if drivers:
                for d in drivers:
                    d_dict = dict(d)
                    self.feedback_driver_combo.addItem(str(d_dict.get('driver_id')), d_dict.get('driver_id'))
        except Exception as e:
            print(f"Error populating driver combo: {e}")

    def populate_conductor_combo(self):
        try:
            self.feedback_conductor_combo.clear()
            self.feedback_conductor_combo.addItem("Select Conductor (Optional)", None)
            conductors = self.db_manager.get_all_conductor_ids()
            if conductors:
                for c in conductors:
                    c_dict = dict(c)
                    self.feedback_conductor_combo.addItem(str(c_dict.get('conductor_id')), c_dict.get('conductor_id'))
        except Exception as e:
            print(f"Error populating conductor combo: {e}")

    def submit_feedback(self):
        try:
            driver_id = self.feedback_driver_combo.currentData()
            conductor_id = self.feedback_conductor_combo.currentData()
            rating = self.feedback_rating_input.text().strip()
            comment = self.feedback_comment_input.text().strip()
            if not rating or not comment:
                QMessageBox.warning(self, "Missing Information", "Please provide both rating and comment")
                return
            try:
                rating_value = float(rating)
                if rating_value < 0 or rating_value > 5:
                    QMessageBox.warning(self, "Invalid Rating", "Rating must be between 0 and 5")
                    return
            except ValueError:
                QMessageBox.warning(self, "Invalid Rating", "Rating must be a number")
                return
            if not driver_id and not conductor_id:
                QMessageBox.warning(self, "Missing Selection", "Please select a driver or conductor")
                return
            success = self.db_manager.execute_insert_update_delete('''
                INSERT INTO feedbacks (commuter_id, driver_id, conductor_id, rating, comment)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.commuter_id, driver_id, conductor_id, rating, comment))
            if success:
                QMessageBox.information(self, "Success", "Feedback submitted successfully")
                self.feedback_rating_input.clear()
                self.feedback_comment_input.clear()
                self.feedback_driver_combo.setCurrentIndex(0)
                self.feedback_conductor_combo.setCurrentIndex(0)
                feedbacks = self.db_manager.get_commuter_feedbacks(self.commuter_id)
                if feedbacks:
                    feedbacks = [dict(feedback) for feedback in feedbacks]
                else:
                    feedbacks = []
                headers = ["Feedback ID", "Driver ID", "Conductor ID", "Rating", "Comment", "Date"]
                keys = ["feedback_id", "driver_id", "conductor_id", "rating", "comment", "date"]
                self.populate_table_view(
                    self.my_feedbacks_table_model,
                    feedbacks,
                    headers,
                    self.my_feedbacks_table,
                    keys=keys
                )
            else:
                QMessageBox.warning(self, "Error", "Failed to submit feedback")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Feedback submission failed: {str(e)}")
