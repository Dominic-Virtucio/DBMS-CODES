import sqlite3

DATABASE_NAME = 'transport_app.db'

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, database_name=DATABASE_NAME):
        self.database_name = database_name
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database_name)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.conn.execute("PRAGMA journal_mode = WAL")
            return True
        except sqlite3.Error as e:
            print(f"Connection error: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def ensure_connection(self):
        if not self.conn:
            return self.connect()
        return True

    def execute_query(self, query, params=None):
        if not self.ensure_connection():
            return None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return None

    def execute_insert_update_delete(self, query, params=None, commit=True):
        if not self.ensure_connection():
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            if commit:
                self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database modification error: {e}")
            if commit:
                self.conn.rollback()
            return False

    def begin_transaction(self):
        self.ensure_connection()
        self.conn.execute("BEGIN TRANSACTION")

    def commit_transaction(self):
        try:
            self.conn.commit()
            print("Transaction committed successfully")
        except sqlite3.Error as e:
            print(f"Commit error: {e}")
            raise

    def rollback_transaction(self):
        try:
            self.conn.rollback()
            print("Transaction rolled back")
        except sqlite3.Error as e:
            print(f"Rollback error: {e}")
            raise

    def get_users(self):
        return self.execute_query("SELECT * FROM users")

    def get_user_by_username(self, username):
        return self.execute_query("SELECT * FROM users WHERE username = ?", (username,))

    def get_user_by_id(self, user_id):
        return self.execute_query("SELECT * FROM users WHERE user_id = ?", (user_id,))

    def get_admins(self):
        return self.execute_query("SELECT a.*, u.username, u.email FROM admins a JOIN users u ON a.user_id = u.user_id")

    def get_drivers(self):
        return self.execute_query("SELECT d.*, u.username, u.first_name, u.last_name, u.email FROM drivers d JOIN users u ON d.user_id = u.user_id")

    def get_conductors(self):
        return self.execute_query("SELECT k.*, u.username, u.first_name, u.last_name, u.email FROM conductors k JOIN users u ON k.user_id = u.user_id")

    def get_commuters(self):
        return self.execute_query("SELECT c.*, u.username, u.first_name, u.last_name, u.email FROM commuters c JOIN users u ON c.user_id = u.user_id")

    def get_vehicles(self):
        return self.execute_query("SELECT * FROM vehicles")

    def get_routes(self):
        return self.execute_query("SELECT route_id, origin, destination FROM routes")

    def get_fares(self):
        return self.execute_query("SELECT f.*, r.origin, r.destination FROM fares f JOIN routes r ON f.route_id = r.route_id")

    def get_transactions(self):
        return self.execute_query("""
            SELECT t.*, c.commuter_id, r.origin, r.destination, v.plate_no, k.conductor_id
            FROM transactions t
            LEFT JOIN commuters c ON t.commuter_id = c.commuter_id
            LEFT JOIN routes r ON t.route_id = r.route_id
            LEFT JOIN vehicles v ON t.vehicle_id = v.vehicle_id
            LEFT JOIN conductors k ON t.conductor_id = k.conductor_id
        """)

    def get_feedbacks(self):
        return self.execute_query("""
            SELECT f.*, c.commuter_id, d.driver_id, k.conductor_id
            FROM feedbacks f
            LEFT JOIN commuters c ON f.commuter_id = c.commuter_id
            LEFT JOIN drivers d ON f.driver_id = d.driver_id
            LEFT JOIN conductors k ON f.conductor_id = k.conductor_id
        """)

    def get_commuter_data(self, user_id):
        return self.execute_query("""
            SELECT c.*, u.username, u.first_name, u.last_name, u.email, u.password
            FROM commuters c
            JOIN users u ON c.user_id = u.user_id
            WHERE u.user_id = ?
        """, (user_id,))

    def get_driver_data(self, user_id):
        return self.execute_query("""
            SELECT d.*, u.username, u.first_name, u.last_name, u.email, u.password, va.vehicle_id, v.plate_no
            FROM drivers d
            JOIN users u ON d.user_id = u.user_id
            LEFT JOIN vehicle_assignment va ON d.driver_id = va.driver_id
            LEFT JOIN vehicles v ON va.vehicle_id = v.vehicle_id
            WHERE u.user_id = ?
        """, (user_id,))

    def get_conductor_data(self, user_id):
        return self.execute_query("""
            SELECT k.*, u.username, u.first_name, u.last_name, u.email, u.password, va.vehicle_id, v.plate_no
            FROM conductors k
            JOIN users u ON k.user_id = u.user_id
            LEFT JOIN vehicle_assignment va ON k.conductor_id = va.conductor_id
            LEFT JOIN vehicles v ON va.vehicle_id = v.vehicle_id
            WHERE u.user_id = ?
        """, (user_id,))

    def get_commuter_transactions(self, commuter_id):
        return self.execute_query("""
            SELECT t.*, r.origin, r.destination, v.plate_no, k.conductor_id
            FROM transactions t
            LEFT JOIN routes r ON t.route_id = r.route_id
            LEFT JOIN vehicles v ON t.vehicle_id = v.vehicle_id
            LEFT JOIN conductors k ON t.conductor_id = k.conductor_id
            WHERE t.commuter_id = ?
        """, (commuter_id,))

    def get_driver_feedbacks(self, driver_id):
        return self.execute_query("""
            SELECT f.feedback_id, f.commuter_id, f.rating, f.comment
            FROM feedbacks f
            WHERE f.driver_id = ?
            ORDER BY f.feedback_id
        """, (driver_id,))

    def get_conductor_feedbacks(self, conductor_id):
        return self.execute_query("""
            SELECT f.feedback_id, f.commuter_id, f.rating, f.comment, datetime('now') AS feedback_date
            FROM feedbacks f
            WHERE f.conductor_id = ?
            ORDER BY f.feedback_id
        """, (conductor_id,))

    def get_conductor_transactions(self, conductor_id):
        return self.execute_query("""
            SELECT t.transaction_id, t.commuter_id, t.route_id AS Route, v.plate_no AS "Vehicle Plate", t.total_fare, t.transaction_date AS Date
            FROM transactions t
            LEFT JOIN vehicles v ON t.vehicle_id = v.vehicle_id
            WHERE t.conductor_id = ?
            ORDER BY t.transaction_date DESC
        """, (conductor_id,))

    def get_vehicle_id_by_plate(self, plate_no):
        result = self.execute_query(
            "SELECT vehicle_id FROM vehicles WHERE LOWER(plate_no) = LOWER(?)",
            (plate_no.strip(),)
        )
        return result[0]['vehicle_id'] if result else None

    def get_driver_id_by_license(self, license_no):
        result = self.execute_query(
            "SELECT driver_id FROM drivers WHERE license_no = ?",
            (license_no.strip(),)
        )
        return result[0]['driver_id'] if result else None

    def get_conductor_id_by_license(self, license_no):
        result = self.execute_query(
            "SELECT conductor_id FROM conductors WHERE license_no = ?",
            (license_no.strip(),)
        )
        return result[0]['conductor_id'] if result else None

    def get_all_commuter_ids(self):
        return self.execute_query("SELECT commuter_id FROM commuters")

    def get_all_driver_ids(self):
        return self.execute_query("SELECT driver_id FROM drivers")

    def get_all_conductor_ids(self):
        return self.execute_query("SELECT conductor_id FROM conductors")

    def get_all_vehicle_ids(self):
        return self.execute_query("SELECT vehicle_id FROM vehicles")

    def get_all_route_ids(self):
        return self.execute_query("SELECT route_id, origin || ' to ' || destination AS route_desc FROM routes")

    def get_all_fare_ids(self):
        return self.execute_query("SELECT fare_id FROM fares")

    def get_all_user_ids(self):
        return self.execute_query("SELECT user_id, username FROM users")

    def get_user_id_by_username(self, username):
        result = self.get_user_by_username(username)
        if result:
            return result[0]['user_id']
        return None

    def get_commuter_id_by_user_id(self, user_id):
        result = self.execute_query("SELECT commuter_id FROM commuters WHERE user_id = ?", (user_id,))
        return result[0]['commuter_id'] if result else None

    def get_driver_id_by_user_id(self, user_id):
        result = self.execute_query("SELECT driver_id FROM drivers WHERE user_id = ?", (user_id,))
        return result[0]['driver_id'] if result else None

    def get_conductor_id_by_user_id(self, user_id):
        result = self.execute_query("SELECT conductor_id FROM conductors WHERE user_id = ?", (user_id,))
        return result[0]['conductor_id'] if result else None

    def get_commuter_by_username(self, username):
        if not self.ensure_connection():
            return None
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.*, u.password, 'Commuter' AS user_type
            FROM commuters c
            JOIN users u ON c.user_id = u.user_id
            WHERE u.username = ?
        """, (username,))
        return cursor.fetchone()

    def get_commuter_feedbacks(self, commuter_id):
        return self.execute_query("""
            SELECT f.feedback_id, f.driver_id, f.conductor_id, f.rating, f.comment, datetime('now') AS date
            FROM feedbacks f
            WHERE f.commuter_id = ?
            ORDER BY f.feedback_id DESC
        """, (commuter_id,))

    def get_driver_by_username(self, username):
        if not self.ensure_connection():
            return None
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.*, u.password, 'Driver' AS user_type
            FROM drivers d
            JOIN users u ON d.user_id = u.user_id
            WHERE u.username = ?
        """, (username,))
        return cursor.fetchone()

    def insert_commuter(self, username, password, first_name, last_name, email):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users
                (username, password, first_name, last_name, email, user_type)
                VALUES (?, ?, ?, ?, ?, 'Commuter')
            ''', (username, password, first_name, last_name, email))
            user_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO commuters (user_id)
                VALUES (?)
            ''', (user_id,))
            self.conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")

    def authenticate_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT u.*,
                c.commuter_id, c.contact_no, c.discount_type,
                d.driver_id, d.license_no,
                k.conductor_id,
                a.admin_id
            FROM users u
            LEFT JOIN commuters c ON u.user_id = c.user_id
            LEFT JOIN drivers d ON u.user_id = d.user_id
            LEFT JOIN conductors k ON u.user_id = k.user_id
            LEFT JOIN admins a ON u.user_id = a.user_id
            WHERE u.username = ? AND u.password = ?
        ''', (username, password))
        user = cursor.fetchone()
        return dict(user) if user else None

    def get_fares_with_routes(self):
        return self.execute_query("""
            SELECT
                f.fare_id AS "Fare ID",
                r.route_id AS "Route ID",
                r.origin AS "Origin",
                r.destination AS "Destination",
                r.distance AS "Distance",
                f.price_fare AS "Price",
                f.discount_fare AS "Discount Price"
            FROM fares f
            JOIN routes r ON f.route_id = r.route_id
            ORDER BY f.fare_id
        """)
