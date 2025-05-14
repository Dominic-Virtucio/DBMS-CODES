import sqlite3

DATABASE_NAME = 'transport_app.db'

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR UNIQUE NOT NULL,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        email VARCHAR UNIQUE,
        password VARCHAR NOT NULL,
        user_type VARCHAR NOT NULL CHECK(user_type IN ('Admin', 'Commuter', 'Driver', 'Conductor'))
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        admin_id VARCHAR PRIMARY KEY,
        user_id INTEGER UNIQUE,
        role VARCHAR,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id VARCHAR PRIMARY KEY,
        user_id INTEGER UNIQUE NOT NULL,
        license_no INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS commuters (
        commuter_id VARCHAR PRIMARY KEY,
        user_id INTEGER NOT NULL,
        contact_no TEXT,
        discount_type TEXT DEFAULT 'None',
        preferred_route INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(preferred_route) REFERENCES routes(route_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conductors (
        conductor_id VARCHAR PRIMARY KEY,
        user_id INTEGER UNIQUE NOT NULL,
        license_no INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id VARCHAR PRIMARY KEY,
        plate_no VARCHAR UNIQUE NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS routes (
        route_id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin VARCHAR NOT NULL,
        destination VARCHAR NOT NULL,
        distance REAL NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fares (
        fare_id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER,
        price_fare REAL NOT NULL,
        discount_fare REAL,
        FOREIGN KEY (route_id) REFERENCES routes(route_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR PRIMARY KEY,
        commuter_id VARCHAR,
        route_id INTEGER,
        vehicle_id VARCHAR,
        conductor_id VARCHAR,
        fare_id INTEGER,
        total_fare REAL NOT NULL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (commuter_id) REFERENCES commuters(commuter_id),
        FOREIGN KEY (route_id) REFERENCES routes(route_id),
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
        FOREIGN KEY (conductor_id) REFERENCES conductors(conductor_id),
        FOREIGN KEY (fare_id) REFERENCES fares(fare_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedbacks (
        feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
        commuter_id VARCHAR,
        driver_id VARCHAR,
        conductor_id VARCHAR,
        rating REAL CHECK(rating BETWEEN 0.0 AND 5.0),
        comment TEXT,
        FOREIGN KEY (commuter_id) REFERENCES commuters(commuter_id),
        FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
        FOREIGN KEY (conductor_id) REFERENCES conductors(conductor_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE vehicle_assignment (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id VARCHAR NOT NULL,
        driver_id VARCHAR NOT NULL,
        conductor_id VARCHAR NOT NULL,
        assignment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id),
        FOREIGN KEY(driver_id) REFERENCES drivers(driver_id),
        FOREIGN KEY(conductor_id) REFERENCES conductors(conductor_id)
    )
    ''')
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS route_view AS
    SELECT
        route_id,
        origin || ' to ' || destination AS origin_to_destination
    FROM routes
    ''')

def create_route_view(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS route_view AS
    SELECT route_id, origin || ' to ' || destination AS route_name
    FROM routes
    ''')
    conn.commit()

def setup_database():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        create_tables(conn)
        print(f"Database '{DATABASE_NAME}' tables created successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    setup_database()
