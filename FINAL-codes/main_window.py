import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from login_window import LoginWindow
from admin_panel import AdminPanel
from commuter_panel import CommuterPanel
from driver_panel import DriverPanel
from conductor_panel import ConductorPanel
from database_manager import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transport App")
        self.setGeometry(100, 100, 600, 600)
        self.db_manager = DatabaseManager()
        if not self.db_manager.connect():
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            sys.exit(1)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.login_window = LoginWindow(self.db_manager)
        self.login_window.login_successful.connect(self.show_user_panel)
        self.stacked_widget.addWidget(self.login_window)
        self.admin_panel = None
        self.commuter_panel = None
        self.driver_panel = None
        self.conductor_panel = None
        self.show_login()

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_window)
        self.setWindowTitle("Login")
        self.login_window.clear_fields()
        if self.admin_panel:
            self.stacked_widget.removeWidget(self.admin_panel)
            self.admin_panel.deleteLater()
            self.admin_panel = None
        if self.commuter_panel:
            self.stacked_widget.removeWidget(self.commuter_panel)
            self.commuter_panel.deleteLater()
            self.commuter_panel = None
        if self.driver_panel:
            self.stacked_widget.removeWidget(self.driver_panel)
            self.driver_panel.deleteLater()
            self.driver_panel = None
        if self.conductor_panel:
            self.stacked_widget.removeWidget(self.conductor_panel)
            self.conductor_panel.deleteLater()
            self.conductor_panel = None

    def show_user_panel(self, user_type, user_data):
        if user_type == 'Admin':
            self.admin_panel = AdminPanel(self.db_manager, user_data)
            self.admin_panel.logout_requested.connect(self.show_login)
            self.stacked_widget.addWidget(self.admin_panel)
            self.stacked_widget.setCurrentWidget(self.admin_panel)
            self.setWindowTitle("Admin Panel")
        elif user_type == 'Commuter':
            self.commuter_panel = CommuterPanel(self.db_manager, user_data)
            self.commuter_panel.logout_requested.connect(self.show_login)
            self.stacked_widget.addWidget(self.commuter_panel)
            self.stacked_widget.setCurrentWidget(self.commuter_panel)
            self.setWindowTitle("Commuter Panel")
        elif user_type == 'Driver':
            self.driver_panel = DriverPanel(self.db_manager, user_data)
            self.driver_panel.logout_requested.connect(self.show_login)
            self.stacked_widget.addWidget(self.driver_panel)
            self.stacked_widget.setCurrentWidget(self.driver_panel)
            self.setWindowTitle("Driver Panel")
        elif user_type == 'Conductor':
            self.conductor_panel = ConductorPanel(self.db_manager, user_data)
            self.conductor_panel.logout_requested.connect(self.show_login)
            self.stacked_widget.addWidget(self.conductor_panel)
            self.stacked_widget.setCurrentWidget(self.conductor_panel)
            self.setWindowTitle("Conductor Panel")
        else:
            QMessageBox.critical(self, "Login Error", f"Unknown user type: {user_type}")
            self.show_login()

    def closeEvent(self, event):
        self.db_manager.close()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
