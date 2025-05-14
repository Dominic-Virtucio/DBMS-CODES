import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QButtonGroup, QRadioButton, QLabel, QComboBox, QPushButton

class FareCalculatorApp(QtWidgets.QWidget):
    def __init__(self, db_manager=None):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Transport Fare Calculator")
        self.setGeometry(100, 100, 500, 600)
        self.setFixedSize(500, 600)
        self.setStyleSheet("background-color: #E3F2FD;")
        layout = QtWidgets.QVBoxLayout()

        origin_label = QLabel("Select Origin:")
        origin_label.setStyleSheet("font: bold 10pt 'Segoe UI'; color: #1976D2;")
        layout.addWidget(origin_label)
        self.origin_combo = QComboBox()
        self.origin_combo.setStyleSheet("font: 10pt 'Segoe UI'; background-color: #BBDEFB; color: #1976D2;")
        self.origin_combo.addItems(self.fetch_origins())
        layout.addWidget(self.origin_combo)

        destination_label = QLabel("Select Destination:")
        destination_label.setStyleSheet("font: bold 10pt 'Segoe UI'; color: #1976D2;")
        layout.addWidget(destination_label)
        self.destination_combo = QComboBox()
        self.destination_combo.setStyleSheet("font: 10pt 'Segoe UI'; background-color: #BBDEFB; color: #1976D2;")
        self.destination_combo.addItems(self.fetch_destinations())
        layout.addWidget(self.destination_combo)

        passenger_label = QLabel("Passenger Type:")
        passenger_label.setStyleSheet("font: bold 10pt 'Segoe UI'; color: #1976D2;")
        layout.addWidget(passenger_label)
        self.passenger_type_group = QButtonGroup(self)
        self.regular_rb = QRadioButton("Regular")
        self.student_rb = QRadioButton("Student")
        self.senior_rb = QRadioButton("Senior")
        self.pwd_rb = QRadioButton("PWD")
        for rb in [self.regular_rb, self.student_rb, self.senior_rb, self.pwd_rb]:
            rb.setStyleSheet("font: 10pt 'Segoe UI'; color: #1976D2;")
            layout.addWidget(rb)
            self.passenger_type_group.addButton(rb)
        self.regular_rb.setChecked(True)

        calc_button = QPushButton("Calculate Fare")
        calc_button.setStyleSheet("background-color: #2196F3; color: white; font: bold 12pt 'Segoe UI'; border-radius: 5px; padding: 6px 0;")
        calc_button.clicked.connect(self.calculate_fare)
        layout.addWidget(calc_button)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font: 12pt 'Arial'; color: #1976D2;")
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def fetch_origins(self):
        if self.db_manager:
            origins = self.db_manager.execute_query("SELECT DISTINCT origin FROM routes ORDER BY origin")
            return [row['origin'] for row in origins] if origins else []
        else:
            conn = sqlite3.connect('transport_app.db')
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT origin FROM routes ORDER BY origin")
            result = [row[0] for row in cursor.fetchall()]
            conn.close()
            return result

    def fetch_destinations(self):
        if self.db_manager:
            destinations = self.db_manager.execute_query("SELECT DISTINCT destination FROM routes ORDER BY destination")
            return [row['destination'] for row in destinations] if destinations else []
        else:
            conn = sqlite3.connect('transport_app.db')
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT destination FROM routes ORDER BY destination")
            result = [row[0] for row in cursor.fetchall()]
            conn.close()
            return result

    def calculate_fare(self):
        origin = self.origin_combo.currentText()
        destination = self.destination_combo.currentText()
        if self.regular_rb.isChecked():
            passenger_type = "Regular"
        elif self.student_rb.isChecked():
            passenger_type = "Student"
        elif self.senior_rb.isChecked():
            passenger_type = "Senior"
        elif self.pwd_rb.isChecked():
            passenger_type = "PWD"
        else:
            passenger_type = "Regular"
        if not origin or not destination:
            self.show_message("Input Error", "Please select both origin and destination.")
            return
        if origin == destination:
            base_fare = 15.00 if passenger_type == 'Regular' else 12.00
            self.result_label.setText(
                f"Origin: {origin}\nDestination: {destination}\nTotal KM: 0\nTotal Fare: {base_fare:.2f} PHP ({passenger_type})"
            )
            return
        if self.db_manager:
            query = '''
SELECT r.route_id, r.distance, f.price_fare, f.discount_fare
FROM routes r
JOIN fares f ON r.route_id = f.route_id
WHERE r.origin = ? AND r.destination = ?
'''
            res = self.db_manager.execute_query(query, (origin, destination))
            if not res:
                self.show_message("Error", "Route not found.")
                return
            res = res[0]
            distance = res['distance']
            price_fare = res['price_fare']
            discount_fare = res['discount_fare']
        else:
            conn = sqlite3.connect('transport_app.db')
            cursor = conn.cursor()
            cursor.execute('''
SELECT r.route_id, r.distance, f.price_fare, f.discount_fare
FROM routes r
JOIN fares f ON r.route_id = f.route_id
WHERE r.origin = ? AND r.destination = ?
''', (origin, destination))
            res = cursor.fetchone()
            conn.close()
            if not res:
                self.show_message("Error", "Route not found.")
                return
            _, distance, price_fare, discount_fare = res
        fare = price_fare if passenger_type == 'Regular' else discount_fare
        self.result_label.setText(
            f"Origin: {origin}\nDestination: {destination}\nTotal KM: {distance}\nTotal Fare: {fare:.2f} PHP ({passenger_type})"
        )

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.exec_()
