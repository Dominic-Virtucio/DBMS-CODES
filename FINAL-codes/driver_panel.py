from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableView, QFormLayout, QGroupBox, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class DriverPanel(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, db_manager, user_data):
        super().__init__()
        self.db_manager = db_manager
        self.user_data = user_data
        self.driver_id = self.user_data.get('driver_id')
        self.setWindowTitle("Driver Panel")
        self.init_ui()
        self.load_driver_data()
        self.load_assigned_vehicle()
        self.load_fares()
        self.load_feedbacks()

    def init_ui(self):
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        self.user_label = QLabel(f"Logged in as: Driver ({self.user_data.get('username', 'N/A')})")
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

        driver_info_group = QGroupBox("My Information")
        driver_info_group.setStyleSheet("QGroupBox { color: #0D2240; font-weight: bold; }")
        driver_info_layout = QFormLayout()
        self.username_value = QLabel()
        driver_info_layout.addRow(QLabel("Username:"), self.username_value)
        self.name_value = QLabel()
        driver_info_layout.addRow(QLabel("Name:"), self.name_value)
        self.email_value = QLabel()
        driver_info_layout.addRow(QLabel("Email:"), self.email_value)
        self.license_value = QLabel()
        driver_info_layout.addRow(QLabel("License No:"), self.license_value)
        driver_info_group.setLayout(driver_info_layout)
        main_layout.addWidget(driver_info_group)

        vehicle_group = QGroupBox("Assigned Vehicle")
        vehicle_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; }")
        vehicle_layout = QFormLayout()
        self.vehicle_id_value = QLabel("N/A")
        vehicle_layout.addRow(QLabel("Vehicle ID:"), self.vehicle_id_value)
        self.plate_no_value = QLabel("N/A")
        vehicle_layout.addRow(QLabel("Plate No:"), self.plate_no_value)
        vehicle_group.setLayout(vehicle_layout)
        main_layout.addWidget(vehicle_group)

        data_views_group = QGroupBox("Data Views")
        data_views_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; }")
        data_views_layout = QVBoxLayout()
        fares_label = QLabel("Route and Fare Details:")
        fares_label.setStyleSheet("color: #1976D2; font-weight: bold;")
        data_views_layout.addWidget(fares_label)
        self.fares_table = QTableView()
        self.fares_table_model = QStandardItemModel()
        self.fares_table.setModel(self.fares_table_model)
        self.fares_table.setEditTriggers(QTableView.NoEditTriggers)
        self.fares_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #1976D2; color: white; font-weight: bold; }"
        )
        self.fares_table.verticalHeader().setVisible(False)
        data_views_layout.addWidget(self.fares_table)
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

    def load_driver_data(self):
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

    def load_fares(self):
        fares = self.db_manager.get_fares_with_routes()
        self.populate_table_view(
            self.fares_table_model,
            fares,
            ["Fare ID", "Route ID", "Origin", "Destination", "Distance", "Price", "Discount Price"]
        )
        self.resize_table_view_uniform(self.fares_table)

    def load_feedbacks(self):
        feedbacks = self.db_manager.get_driver_feedbacks(self.driver_id)
        self.populate_table_view(
            self.feedbacks_table_model,
            feedbacks,
            ["Feedback ID", "Commuter ID", "Rating", "Comment"]
        )
        self.resize_table_view_uniform(self.feedbacks_table)

    def populate_table_view(self, model, data, headers):
        model.clear()
        model.setHorizontalHeaderLabels(headers)
        if data:
            for row_data in data:
                items = []
                for i, header in enumerate(headers):
                    value = row_data[i]
                    if header == "Distance":
                        value = f"{value} km"
                    elif header in ("Price", "Discount Price"):
                        value = f"₱{value}"
                    item = QStandardItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    items.append(item)
                model.appendRow(items)

    def resize_table_view_uniform(self, table_view):
        header = table_view.horizontalHeader()
        column_count = table_view.model().columnCount()
        if column_count == 0:
            return
        for col in range(column_count):
            header.setSectionResizeMode(col, QHeaderView.Stretch)
