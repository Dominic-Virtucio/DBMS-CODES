from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableView, QFormLayout, QGroupBox, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ConductorPanel(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, db_manager, user_data):
        super().__init__()
        self.db_manager = db_manager
        self.user_data = user_data
        self.conductor_id = self.user_data.get('conductor_id')
        self.setWindowTitle("Conductor Panel")
        self.init_ui()
        self.load_conductor_data()
        self.load_assigned_vehicle()
        self.load_transactions()
        self.load_feedbacks()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        self.user_label = QLabel(f"Logged in as: Conductor ({self.user_data.get('username', 'N/A')})")
        self.user_label.setStyleSheet("color: #1976D2; font-weight: bold; font-size: 16px;")
        header_layout.addWidget(self.user_label)
        header_layout.addStretch()
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet(
            "background-color: #2196F3; color: white; font-weight: bold; border-radius: 5px; padding: 7px 18px;"
        )
        self.logout_button.clicked.connect(self.logout_requested.emit)
        header_layout.addWidget(self.logout_button)
        main_layout.addLayout(header_layout)

        # Conductor Information Group
        conductor_info_group = QGroupBox("My Information")
        conductor_info_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; }")
        conductor_info_layout = QFormLayout()
        self.username_value = QLabel()
        conductor_info_layout.addRow(QLabel("Username:"), self.username_value)
        self.name_value = QLabel()
        conductor_info_layout.addRow(QLabel("Name:"), self.name_value)
        self.email_value = QLabel()
        conductor_info_layout.addRow(QLabel("Email:"), self.email_value)
        self.license_value = QLabel()
        conductor_info_layout.addRow(QLabel("License No:"), self.license_value)
        conductor_info_group.setLayout(conductor_info_layout)
        main_layout.addWidget(conductor_info_group)

        # Assigned Vehicle Group
        vehicle_group = QGroupBox("Assigned Vehicle")
        vehicle_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; }")
        vehicle_layout = QFormLayout()
        self.vehicle_id_value = QLabel("N/A")
        vehicle_layout.addRow(QLabel("Vehicle ID:"), self.vehicle_id_value)
        self.plate_no_value = QLabel("N/A")
        vehicle_layout.addRow(QLabel("Plate No:"), self.plate_no_value)
        vehicle_group.setLayout(vehicle_layout)
        main_layout.addWidget(vehicle_group)

        # Data Views Section
        data_views_group = QGroupBox("Trip Information")
        data_views_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; }")
        data_views_layout = QVBoxLayout()

        # Transactions Table
        transactions_label = QLabel("Transactions Handled:")
        transactions_label.setStyleSheet("color: #1976D2; font-weight: bold;")
        data_views_layout.addWidget(transactions_label)
        self.transactions_table = QTableView()
        self.transactions_table_model = QStandardItemModel()
        self.transactions_table.setModel(self.transactions_table_model)
        self.transactions_table.setEditTriggers(QTableView.NoEditTriggers)
        self.transactions_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #1976D2; color: white; font-weight: bold; }"
        )
        self.transactions_table.verticalHeader().setVisible(False)
        data_views_layout.addWidget(self.transactions_table)

        # Feedbacks Table
        feedbacks_label = QLabel("Feedback for Me:")
        feedbacks_label.setStyleSheet("color: #1976D2; font-weight: bold;")
        data_views_layout.addWidget(feedbacks_label)
        self.feedbacks_table = QTableView()
        self.feedbacks_table_model = QStandardItemModel()
        self.feedbacks_table.setModel(self.feedbacks_table_model)
        self.feedbacks_table.setEditTriggers(QTableView.NoEditTriggers)
        self.feedbacks_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #1976D2; color: white; font-weight: bold; }"
        )
        self.feedbacks_table.verticalHeader().setVisible(False)
        data_views_layout.addWidget(self.feedbacks_table)

        data_views_group.setLayout(data_views_layout)
        main_layout.addWidget(data_views_group)
        self.setLayout(main_layout)

    def load_conductor_data(self):
        self.username_value.setText(self.user_data.get('username', 'N/A'))
        self.name_value.setText(f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}")
        self.email_value.setText(self.user_data.get('email', ''))
        self.license_value.setText(str(self.user_data.get('license_no', 'N/A')))

    def load_assigned_vehicle(self):
        vehicle_id = self.user_data.get('vehicle_id')
        plate_no = self.user_data.get('plate_no')
        if vehicle_id:
            self.vehicle_id_value.setText(str(vehicle_id))
            self.plate_no_value.setText(str(plate_no))
        else:
            self.vehicle_id_value.setText("Not Assigned")
            self.plate_no_value.setText("Not Assigned")

    def load_transactions(self):
        transactions = self.db_manager.get_conductor_transactions(self.conductor_id)
        
        # Define headers that match exactly what's returned by the query
        headers = ["Transaction ID", "Commuter ID", "Route", "Vehicle Plate", "Total Fare", "Date"]
        
        self.populate_table_view(
            self.transactions_table_model,
            transactions,
            headers
        )
        
        self.resize_table_view_uniform(self.transactions_table)
        
    def load_feedbacks(self):
        feedbacks = self.db_manager.get_conductor_feedbacks(self.conductor_id)
        self.populate_table_view(
            self.feedbacks_table_model,
            feedbacks,
            ["Feedback ID", "Commuter ID", "Rating", "Comment", "Date"]
        )
        self.resize_table_view_uniform(self.feedbacks_table)

    def populate_table_view(self, model, data, headers):
        model.clear()
        model.setHorizontalHeaderLabels(headers)
        
        if data:
            for row_data in data:
                items = []
                for i, header in enumerate(headers):
                    if i < len(row_data):  # Make sure we don't access beyond available data
                        value = row_data[i]
                        
                        # Format Total Fare
                        if header == "Total Fare":
                            value = f"₱{value}"
                        
                        # Format Date columns
                        if header == "Date" and value:
                            try:
                                # Try to format as date if it's a date string
                                from datetime import datetime
                                date_obj = datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
                                value = date_obj.strftime("%Y-%m-%d %H:%M")
                            except:
                                # If it's not a valid date format, keep as is
                                pass
                        
                        item = QStandardItem(str(value))
                        item.setTextAlignment(Qt.AlignCenter)
                        items.append(item)
                    else:
                        # Add empty item if data is missing
                        items.append(QStandardItem(""))
                
                model.appendRow(items)


    def resize_table_view_uniform(self, table_view):
        header = table_view.horizontalHeader()
        column_count = table_view.model().columnCount()
        if column_count == 0:
            return
        for col in range(column_count):
            header.setSectionResizeMode(col, QHeaderView.Stretch)