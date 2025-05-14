import sqlite3
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableView, QMessageBox, QInputDialog, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSql import (
    QSqlDatabase, QSqlRelationalTableModel, QSqlRelation, QSqlTableModel
)

def connect_to_database():
    """Connect to the SQLite database using Qt SQL module."""
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("transport_app.db")
    if not db.open():
        QMessageBox.critical(
            None,
            "Database Connection Error",
            f"Unable to establish a database connection:\n{db.lastError().text()}"
        )
        return False
    return True

# Call this before using any SQL models
if not connect_to_database():
    raise SystemExit("Database connection failed.")
    
class AdminPanel(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, db_manager, user_data):  # Add user_data parameter
        super().__init__()
        self.db_manager = db_manager
        self.user_data = user_data  # Store user_data
        self.current_table = None
        self.models = {}
        self.views = {}
        self.setWindowTitle("Admin Panel")
        self.init_ui()
        self.init_db_model()


    def init_ui(self):
        self.setStyleSheet("background-color: #F5F5F5;")
        main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        self.user_label = QLabel("Admin Panel")
        self.user_label.setStyleSheet("color: #1976D2; font-weight: bold; font-size: 24px;")
        header_layout.addWidget(self.user_label)
        header_layout.addStretch()
        
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; font-weight: bold; border-radius: 6px; padding: 8px 22px; }"
            "QPushButton:hover { background-color: #1976D2; }"
        )
        self.logout_button.clicked.connect(self.logout_requested.emit)
        header_layout.addWidget(self.logout_button)
        main_layout.addLayout(header_layout)

        # Table Selection Buttons
        tables = ["users", "admins", "drivers", "commuters", "conductors", 
                 "vehicles", "routes", "fares", "transactions", "feedbacks", 
                 "vehicle_assignment"]
        buttons_layout = QHBoxLayout()
        for table in tables:
            btn = QPushButton(table.capitalize())
            btn.setStyleSheet(
                "QPushButton { background-color: #BBDEFB; color: #1976D2; padding: 8px; border-radius: 4px; }"
                "QPushButton:hover { background-color: #90CAF9; }"
                "QPushButton:checked { background-color: #64B5F6; }"
            )
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, t=table: self.show_table(t))
            buttons_layout.addWidget(btn)
        main_layout.addLayout(buttons_layout)

        # Table View
        self.table_view = QTableView()
        self.table_view.setEditTriggers(QTableView.DoubleClicked)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        main_layout.addWidget(self.table_view)

        # Control Buttons
        control_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Row")
        self.add_button.setStyleSheet(self.logout_button.styleSheet())
        self.add_button.clicked.connect(self.add_row)
        
        self.delete_button = QPushButton("Delete Row")
        self.delete_button.setStyleSheet(self.logout_button.styleSheet())
        self.delete_button.clicked.connect(self.delete_row)
        
        self.save_button = QPushButton("Save Changes")
        self.save_button.setStyleSheet(self.logout_button.styleSheet())
        self.save_button.clicked.connect(self.save_changes)

        control_layout.addWidget(self.add_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.save_button)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)

    def init_db_model(self):
        table_configs = {
            'users': {'model_type': QSqlRelationalTableModel, 'relations': {}},
            'admins': {'model_type': QSqlRelationalTableModel, 'relations': {
                1: ('users', 'user_id', 'username')
            }},
            'drivers': {'model_type': QSqlRelationalTableModel, 'relations': {
                1: ('users', 'user_id', 'username')
            }},
            'commuters': {'model_type': QSqlTableModel, 'relations': {}},
            'conductors': {'model_type': QSqlRelationalTableModel, 'relations': {
                1: ('users', 'user_id', 'username')
            }},
            'vehicles': {'model_type': QSqlRelationalTableModel, 'relations': {}},
            'routes': {'model_type': QSqlRelationalTableModel, 'relations': {}},
            'fares': {'model_type': QSqlRelationalTableModel, 'relations': {
                1: ('route_view', 'route_id', 'origin_to_destination')
            }},

            'transactions': {'model_type': QSqlRelationalTableModel, 'relations': {
                1: ('commuters', 'commuter_id', 'commuter_id'),
                2: ('route_view', 'route_id', 'origin_to_destination'),  # Use the view!
                3: ('vehicles', 'vehicle_id', 'plate_no'),
                4: ('conductors', 'conductor_id', 'conductor_id'),
                5: ('fares', 'fare_id', 'price_fare')
            }},

            'feedbacks': {'model_type': QSqlRelationalTableModel, 'relations': {
                1: ('commuters', 'commuter_id', 'commuter_id'),
                2: ('drivers', 'driver_id', 'driver_id'),
                3: ('conductors', 'conductor_id', 'conductor_id')
            }},
            'vehicle_assignment': {'model_type': QSqlRelationalTableModel, 'relations': {
                1: ('vehicles', 'vehicle_id', 'plate_no'),
                2: ('drivers', 'driver_id', 'driver_id'),
                3: ('conductors', 'conductor_id', 'conductor_id')
            }}
        }

        for table_name, config in table_configs.items():
            model = config['model_type']()
            model.setTable(table_name)
            model.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)
            
            if 'relations' in config:
                for column, relation in config['relations'].items():
                    model.setRelation(column, QSqlRelation(*relation))
            
            model.select()
            self.models[table_name] = model

    def show_table(self, table_name):
        self.current_table = table_name
        model = self.models[table_name]
        
        # Refresh the model data from the database
        model.select()
        print(f"Row count for {table_name}: {model.rowCount()}")
        # Set headers to match relations
        for i in range(model.columnCount()):
            model.setHeaderData(i, Qt.Horizontal, model.headerData(i, Qt.Horizontal))
        
        self.table_view.setModel(model)
        self.table_view.resizeColumnsToContents()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_id_from_relation(self, table, display_column, prompt):
        """Helper to get foreign key ID from user selection"""
        # Get primary key column name dynamically
        pk_column = {
            'vehicles': 'vehicle_id',
            'drivers': 'driver_id',
            'conductors': 'conductor_id'
        }.get(table, 'rowid')
        
        query = f"SELECT {display_column}, {pk_column} FROM {table}"
        data = self.db_manager.execute_query(query)
        
        if not data:
            QMessageBox.warning(self, "Error", f"No {table} available!")
            return None
    
        items = [str(record[0]) for record in data]
        item, ok = QInputDialog.getItem(self, f"Select {prompt}", f"{prompt}:", items, 0, False)
        
        return data[items.index(item)][1] if ok and item else None


    def add_row(self):
        if not self.current_table:
            return
    
        try:
            if self.current_table == "vehicle_assignment":
                # Prompt for vehicle plate, driver license, and conductor license
                vehicle_plate, ok = QInputDialog.getText(
                    self, "Vehicle Assignment", "Enter Vehicle Plate Number:"
                )
                if not ok or not vehicle_plate:
                    return
    
                driver_license, ok = QInputDialog.getText(
                    self, "Vehicle Assignment", "Enter Driver License Number:"
                )
                if not ok or not driver_license:
                    return
    
                conductor_license, ok = QInputDialog.getText(
                    self, "Vehicle Assignment", "Enter Conductor License Number:"
                )
                if not ok or not conductor_license:
                    return
    
                # Lookup IDs
                vehicle_id = self.db_manager.get_vehicle_id_by_plate(vehicle_plate)
                driver_id = self.db_manager.get_driver_id_by_license(driver_license)
                conductor_id = self.db_manager.get_conductor_id_by_license(conductor_license)
    
                # Debug: Print fetched IDs
                print(f"Fetched IDs - Vehicle: {vehicle_id}, Driver: {driver_id}, Conductor: {conductor_id}")
    
                if not all([vehicle_id, driver_id, conductor_id]):
                    QMessageBox.warning(self, "Error", "Invalid license/plate number(s)")
                    return
    
                # Create and insert record
                model = self.models[self.current_table]
                record = model.record()
                record.setValue("vehicle_id", str(vehicle_id))
                record.setValue("driver_id", str(driver_id))
                record.setValue("conductor_id", str(conductor_id))
                record.setValue("assignment_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
                # With this improved version:
                if model.insertRecord(-1, record):
                    if model.submitAll():
                        QMessageBox.information(self, "Success", "Assignment added successfully!")
                        # Force a complete refresh of the table
                        self.show_table("vehicle_assignment")  # Re-show the same table to force refresh
                    else:
                        error = model.lastError().text()
                        print(f"Database Error: {error}")
                        QMessageBox.critical(self, "Error", f"Failed to save: {error}")
                else:
                    QMessageBox.critical(self, "Error", "Failed to insert record into model")
                    
                model = self.models[self.current_table]
                row_count = model.rowCount()
                model.insertRow(row_count)
                index = model.index(row_count, 0)
                self.table_view.setCurrentIndex(index)
                self.table_view.edit(index)
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Operation failed: {str(e)}")

    def create_user(self, username, password, user_type, first_name="", last_name="", email=""):
        """Base method to create a user (no transaction handling)"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users 
            (username, password, user_type, first_name, last_name, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password, user_type, first_name, last_name, email))
        return cursor.lastrowid
        
    def create_driver(self, username, password, license_no, **user_info):
        """Create a driver with proper transaction handling"""
        try:
            self.begin_transaction()
            cursor = self.conn.cursor()
            
            # Insert into users
            user_id = self.create_user(
                username, password, 'Driver',
                user_info.get('first_name', ''),
                user_info.get('last_name', ''),
                user_info.get('email', '')
            )
            
            # Generate driver ID
            driver_id = f"D{user_id}"
            
            # Insert into drivers
            cursor.execute('''
                INSERT INTO drivers 
                (driver_id, user_id, license_no)
                VALUES (?, ?, ?)
            ''', (driver_id, user_id, license_no))
            
            self.commit_transaction()
            return driver_id
        except Exception as e:
            self.rollback_transaction()
            raise ValueError(f"Driver creation failed: {str(e)}")
        
    def create_conductor(self, username, password, license_no, **user_info):
        try:
            self.begin_transaction()
            cursor = self.conn.cursor()
            
            user_id = self.create_user(
                username, password, 'Conductor',
                user_info.get('first_name', ''),
                user_info.get('last_name', ''),
                user_info.get('email', '')
            )
            
            conductor_id = f"C{user_id}"
            cursor.execute('''
                INSERT INTO conductors 
                (conductor_id, user_id, license_no)
                VALUES (?, ?, ?)
            ''', (conductor_id, user_id, license_no))
            
            self.commit_transaction()
            return conductor_id
        except Exception as e:
            self.rollback_transaction()
            raise ValueError(f"Conductor creation failed: {str(e)}")
    
    def create_admin(self, username, password, role, **user_info):
        try:
            self.begin_transaction()
            cursor = self.conn.cursor()
            
            user_id = self.create_user(
                username, password, 'Admin',
                user_info.get('first_name', ''),
                user_info.get('last_name', ''),
                user_info.get('email', '')
            )
            
            admin_id = f"A{user_id}"
            cursor.execute('''
                INSERT INTO admins 
                (admin_id, user_id, role)
                VALUES (?, ?, ?)
            ''', (admin_id, user_id, role))
            
            self.commit_transaction()
            return admin_id
        except Exception as e:
            self.rollback_transaction()
            raise ValueError(f"Admin creation failed: {str(e)}")

    def delete_row(self):
        if not self.current_table:
            return

        try:
            model = self.models[self.current_table]
            current_row = self.table_view.currentIndex().row()
            if current_row >= 0:
                model.removeRow(current_row)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete row: {str(e)}")

    def save_changes(self):
        if not self.current_table:
            return

        model = self.models[self.current_table]
        if model.submitAll():
            model.select()
            QMessageBox.information(self, "Success", "Changes saved successfully")
        else:
            error = model.lastError().text()
            if self.current_table == "vehicle_assignment":
                error += "\nEnsure you selected valid Vehicle, Driver, and Conductor"
            QMessageBox.critical(self, "Error", f"Save failed:\n{error}")
