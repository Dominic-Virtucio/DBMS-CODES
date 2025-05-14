from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableView, QFormLayout, QGroupBox, QHeaderView, QInputDialog, QMessageBox
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
        
        vehicle_group = QGroupBox("Assigned Vehicle")
        vehicle_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; }")
        vehicle_layout = QFormLayout()
        
        self.vehicle_id_value = QLabel("N/A")
        vehicle_layout.addRow(QLabel("Vehicle ID:"), self.vehicle_id_value)
        
        self.plate_no_value = QLabel("N/A")
        vehicle_layout.addRow(QLabel("Plate No:"), self.plate_no_value)
        
        vehicle_group.setLayout(vehicle_layout)
        main_layout.addWidget(vehicle_group)
        
        transaction_group = QGroupBox("Transaction Management")
        transaction_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; }")
        transaction_layout = QVBoxLayout()
        
        self.add_transaction_btn = QPushButton("Add New Transaction")
        self.add_transaction_btn.setStyleSheet(
            "background-color: #1976D2; color: white; font-weight: bold; border-radius: 5px; padding: 7px 18px;"
        )
        self.add_transaction_btn.clicked.connect(self.add_transaction)
        transaction_layout.addWidget(self.add_transaction_btn)
        
        transactions_label = QLabel("Recent Transactions:")
        transactions_label.setStyleSheet("color: #1976D2; font-weight: bold;")
        transaction_layout.addWidget(transactions_label)
        
        self.transactions_table = QTableView()
        self.transactions_model = QStandardItemModel()
        self.transactions_table.setModel(self.transactions_model)
        self.transactions_table.setEditTriggers(QTableView.NoEditTriggers)
        self.transactions_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #1976D2; color: white; font-weight: bold; }"
        )
        self.transactions_table.verticalHeader().setVisible(False)
        transaction_layout.addWidget(self.transactions_table)
        
        transaction_group.setLayout(transaction_layout)
        main_layout.addWidget(transaction_group)
        
        feedback_group = QGroupBox("Passenger Feedback")
        feedback_group.setStyleSheet("QGroupBox { color: #1976D2; font-weight: bold; }")
        feedback_layout = QVBoxLayout()
        
        feedback_label = QLabel("Recent Feedback:")
        feedback_label.setStyleSheet("color: #1976D2; font-weight: bold;")
        feedback_layout.addWidget(feedback_label)
        
        self.feedback_table = QTableView()
        self.feedback_model = QStandardItemModel()
        self.feedback_table.setModel(self.feedback_model)
        self.feedback_table.setEditTriggers(QTableView.NoEditTriggers)
        self.feedback_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #1976D2; color: white; font-weight: bold; }"
        )
        self.feedback_table.verticalHeader().setVisible(False)
        feedback_layout.addWidget(self.feedback_table)
        
        feedback_group.setLayout(feedback_layout)
        main_layout.addWidget(feedback_group)
        
        self.setLayout(main_layout)
    
    def add_transaction(self):
        """Handles the complete transaction creation workflow"""
        try:
            commuters = self.db_manager.get_all_commuter_ids()
            if not commuters:
                QMessageBox.warning(self, "No Commuters", "No registered commuters found.")
                return
            
            commuter_id = self.get_selection("Select Commuter", "Commuter ID:",
                                          [str(c['commuter_id']) for c in commuters])
            if not commuter_id:
                return
            
            routes = self.db_manager.get_all_route_ids()
            if not routes:
                QMessageBox.warning(self, "No Routes", "No available routes configured.")
                return
            
            route_info = [f"{r['route_id']}: {r['route_desc']}" for r in routes]
            route_id = self.get_selection("Select Route", "Available Routes:", route_info)
            if not route_id:
                return
            
            route_id = int(route_id.split(":")[0])
            
            fares = self.db_manager.get_all_fare_ids()
            if not fares:
                QMessageBox.warning(self, "No Fares", "No fare configurations available.")
                return
            
            fare_id = self.get_selection("Select Fare", "Fare ID:",
                                      [str(f['fare_id']) for f in fares])
            if not fare_id:
                return
            
            total_fare, ok = QInputDialog.getDouble(
                self, "Transaction Amount", "Enter total fare amount:",
                0, 0, 10000, 2
            )
            
            if not ok or total_fare <= 0:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a valid fare amount.")
                return
        
            vehicle_id = self.get_assigned_vehicle_id()
            if not vehicle_id:
                QMessageBox.critical(self, "Vehicle Not Assigned",
                                  "You must be assigned a vehicle to record transactions.")
                return
            
            success = self.db_manager.execute_insert_update_delete(
                """INSERT INTO transactions (
                    commuter_id, route_id,
                    vehicle_id, conductor_id, fare_id, total_fare, transaction_date
                ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))""",
                (commuter_id, route_id, vehicle_id, self.conductor_id, fare_id, total_fare)
            )
            
            if success:
                QMessageBox.information(self, "Success", "Transaction recorded successfully!")
                self.load_transactions()
            else:
                QMessageBox.critical(self, "Database Error", "Failed to save transaction.")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Transaction failed: {str(e)}")
        
    def get_selection(self, title, label, items):
        """Helper method for consistent selection dialogs"""
        item, ok = QInputDialog.getItem(
            self, title, label, items, 0, False
        )
        return item if ok else None
    
    def load_conductor_data(self):
        """Populates conductor information from DB."""
        user_id = self.user_data.get('user_id')
        conductor_data = self.db_manager.get_conductor_data(user_id)
        
        if conductor_data and len(conductor_data) > 0:
            data = dict(conductor_data[0])
            self.username_value.setText(data.get('username', 'N/A'))
            self.name_value.setText(f"{data.get('first_name', '')} {data.get('last_name', '')}")
            self.email_value.setText(data.get('email', 'N/A'))
            self.license_value.setText(str(data.get('license_no', 'N/A')))
        else:
            self.username_value.setText(self.user_data.get('username', 'N/A'))
            self.name_value.setText(f"{self.user_data.get('first_name', '')} {self.user_data.get('last_name', '')}")
            self.email_value.setText(self.user_data.get('email', 'N/A'))
            self.license_value.setText(str(self.user_data.get('license_no', 'N/A')))
    
    def get_assigned_vehicle_id(self):
        """Helper method to get the most recently assigned vehicle ID"""
        query = """
        SELECT va.vehicle_id
        FROM vehicle_assignment va
        WHERE va.conductor_id = ?
        ORDER BY va.assignment_date DESC
        LIMIT 1
        """
        result = self.db_manager.execute_query(query, (self.conductor_id,))
        if result and len(result) > 0:
            return result[0]['vehicle_id']
        return None
    
    def load_assigned_vehicle(self):
        """Loads the most recent vehicle assignment data"""
        query = """
        SELECT va.vehicle_id, v.plate_no 
        FROM vehicle_assignment va
        JOIN vehicles v ON va.vehicle_id = v.vehicle_id
        WHERE va.conductor_id = ?
        ORDER BY va.assignment_date DESC
        LIMIT 1
        """
        result = self.db_manager.execute_query(query, (self.conductor_id,))
        
        if result and len(result) > 0:
            vehicle_id = result[0]['vehicle_id']
            plate_no = result[0]['plate_no']
            self.vehicle_id_value.setText(str(vehicle_id))
            self.plate_no_value.setText(str(plate_no))
        else:
            self.vehicle_id_value.setText("Not Assigned")
            self.plate_no_value.setText("Not Assigned")
    
    def load_transactions(self):
        """Reloads transaction data into table view"""
        transactions = self.db_manager.get_conductor_transactions(self.conductor_id)
        headers = ["Transaction ID", "Commuter ID", "Route", "Vehicle", "Amount", "Date"]
        self.populate_table(
            self.transactions_model, transactions, headers,
            currency_cols=["Amount"], date_cols=["Date"]
        )
        self.resize_table_columns(self.transactions_table)
    
    def load_feedbacks(self):
        """Reloads feedback data into table view"""
        feedbacks = self.db_manager.get_conductor_feedbacks(self.conductor_id)
        headers = ["Feedback ID", "Commuter ID", "Rating", "Comment", "Date"]
        self.populate_table(
            self.feedback_model, feedbacks, headers,
            date_cols=["Date"]
        )
        self.resize_table_columns(self.feedback_table)
    
    def populate_table(self, model, data, headers, currency_cols=None, date_cols=None):
        """Generic table population with formatting"""
        model.clear()
        model.setHorizontalHeaderLabels(headers)
        
        currency_cols = currency_cols or []
        date_cols = date_cols or []
        
        if data:  
            for row in data:
                formatted_row = []
                for idx, value in enumerate(row):
                    if idx < len(headers):
                        col_name = headers[idx]
                        if col_name in currency_cols:
                            formatted_value = f"₱{value:,.2f}"
                        elif col_name in date_cols:
                            formatted_value = self.format_datetime(value)
                        else:
                            formatted_value = str(value)
                        
                        item = QStandardItem(formatted_value)
                        item.setTextAlignment(Qt.AlignCenter)
                        formatted_row.append(item)
                
                model.appendRow(formatted_row)
    
    def format_datetime(self, dt_str):
        """Formats datetime string for display"""
        try:
            from datetime import datetime
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%b %d, %Y %H:%M")
        except:
            return dt_str
    
    def resize_table_columns(self, table):
        """Uniform column resizing"""
        header = table.horizontalHeader()
        for col in range(table.model().columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Stretch)
