import sqlite3
from datetime import datetime

DATABASE_NAME = 'transport_app.db'

def insert_sample_data(conn):
    cursor = conn.cursor()

    users_data = [
        # Admins
        ('admin1', 'Super', 'Admin', 'admin1@ex.com', 'adminpass1', 'Admin'),
        ('admin2', 'Alice', 'Director', 'admin2@ex.com', 'adminpass2', 'Admin'),
        ('admin3', 'Bob', 'Manager', 'admin3@ex.com', 'adminpass3', 'Admin'),
        ('admin4', 'Carla', 'Supervisor', 'admin4@ex.com', 'adminpass4', 'Admin'),
        ('admin5', 'David', 'Coordinator', 'admin5@ex.com', 'adminpass5', 'Admin'),
        
        # Drivers
        ('driver1', 'Juan', 'Dela Cruz', 'driver1@ex.com', 'driverpass1', 'Driver'),
        ('driver2', 'Maria', 'Santos', 'driver2@ex.com', 'driverpass2', 'Driver'),
        ('driver3', 'Pedro', 'Reyes', 'driver3@ex.com', 'driverpass3', 'Driver'),
        ('driver4', 'Ana', 'Gonzales', 'driver4@ex.com', 'driverpass4', 'Driver'),
        ('driver5', 'Lito', 'Mendoza', 'driver5@ex.com', 'driverpass5', 'Driver'),
        
        # Commuters
        ('commuter1', 'John', 'Doe', 'commuter1@ex.com', 'commuterpass1', 'Commuter'),
        ('commuter2', 'Jane', 'Smith', 'commuter2@ex.com', 'commuterpass2', 'Commuter'),
        ('commuter3', 'Alice', 'Tan', 'commuter3@ex.com', 'commuterpass3', 'Commuter'),
        ('commuter4', 'Mark', 'Lim', 'commuter4@ex.com', 'commuterpass4', 'Commuter'),
        ('commuter5', 'Sarah', 'Wong', 'commuter5@ex.com', 'commuterpass5', 'Commuter'),
        
        # Conductors
        ('conductor1', 'Peter', 'Jones', 'conductor1@ex.com', 'condpass1', 'Conductor'),
        ('conductor2', 'Carla', 'Lim', 'conductor2@ex.com', 'condpass2', 'Conductor'),
        ('conductor3', 'Rico', 'Navarro', 'conductor3@ex.com', 'condpass3', 'Conductor'),
        ('conductor4', 'Lorna', 'Dizon', 'conductor4@ex.com', 'condpass4', 'Conductor'),
        ('conductor5', 'Ben', 'Parker', 'conductor5@ex.com', 'condpass5', 'Conductor'),
    ]
    
    cursor.executemany(
        """INSERT INTO users 
        (username, first_name, last_name, email, password, user_type) 
        VALUES (?, ?, ?, ?, ?, ?)""",
        users_data
    )
    conn.commit()
    print("Inserted users")

    user_ids = {}
    for username in [u[0] for u in users_data]:
        user_ids[username] = cursor.execute(
            "SELECT user_id FROM users WHERE username=?", (username,)
        ).fetchone()[0]

    # Insert Admins
    admins_data = [
        ('A001', user_ids['admin1'], 'System Admin'),
        ('A002', user_ids['admin2'], 'Operations Manager'),
        ('A003', user_ids['admin3'], 'HR Supervisor'),
        ('A004', user_ids['admin4'], 'IT Coordinator'),
        ('A005', user_ids['admin5'], 'Finance Head'),
    ]
    cursor.executemany(
        "INSERT INTO admins (admin_id, user_id, role) VALUES (?, ?, ?)",
        admins_data
    )
    print("Inserted admins")

    # Insert Drivers
    drivers_data = [
        ('D001', user_ids['driver1'], 1001),
        ('D002', user_ids['driver2'], 1002),
        ('D003', user_ids['driver3'], 1003),
        ('D004', user_ids['driver4'], 1004),
        ('D005', user_ids['driver5'], 1005),
    ]
    cursor.executemany(
        "INSERT INTO drivers (driver_id, user_id, license_no) VALUES (?, ?, ?)",
        drivers_data
    )
    print("Inserted drivers")

    # Insert Commuters
    commuters_data = [
        ('C001', user_ids['commuter1'], '09171234567', 'Student', 1),
        ('C002', user_ids['commuter2'], '09179876543', 'Senior', 2),
        ('C003', user_ids['commuter3'], '09221234567', 'PWD', 3),
        ('C004', user_ids['commuter4'], '09331234567', 'None', 4),
        ('C005', user_ids['commuter5'], '09441234567', 'Student', 5),
    ]
    cursor.executemany(
        """INSERT INTO commuters 
        (commuter_id, user_id, contact_no, discount_type, preferred_route) 
        VALUES (?, ?, ?, ?, ?)""",
        commuters_data
    )
    print("Inserted commuters")

    # Insert Conductors
    conductors_data = [
        ('K001', user_ids['conductor1'], 2001),
        ('K002', user_ids['conductor2'], 2002),
        ('K003', user_ids['conductor3'], 2003),
        ('K004', user_ids['conductor4'], 2004),
        ('K005', user_ids['conductor5'], 2005),
    ]
    cursor.executemany(
        "INSERT INTO conductors (conductor_id, user_id, license_no) VALUES (?, ?, ?)",
        conductors_data
    )
    print("Inserted conductors")

    # Insert Vehicles
    vehicles_data = [
        ('V001', 'ABC123'),
        ('V002', 'XYZ789'),
        ('V003', 'DEF456'),
        ('V004', 'GHI789'),
        ('V005', 'JKL012'),
    ]
    cursor.executemany(
        "INSERT INTO vehicles (vehicle_id, plate_no) VALUES (?, ?)",
        vehicles_data
    )
    print("Inserted vehicles")

    # Insert Routes (from original code)
    routes_data = [
        ('Antipolo', 'Antipolo', 0), ('Antipolo', 'Cogeo', 6.7), ('Antipolo', 'Penafrancia', 8.7),
        ('Antipolo', 'Masinag', 10.4), ('Antipolo', 'Cainta', 10.6), ('Antipolo', 'Katipunan', 15.2),
        ('Antipolo', 'Anonas', 16.7), ('Antipolo', 'T.I.P.', 17.7),
        ('Cogeo', 'Antipolo', 6.7), ('Cogeo', 'Cogeo', 0), ('Cogeo', 'Penafrancia', 2.7),
        ('Cogeo', 'Masinag', 5.8), ('Cogeo', 'Cainta', 6.6), ('Cogeo', 'Katipunan', 10.6),
        ('Cogeo', 'Anonas', 11.5), ('Cogeo', 'T.I.P.', 13.0),
        ('Penafrancia', 'Antipolo', 8.7), ('Penafrancia', 'Cogeo', 2.7), ('Penafrancia', 'Penafrancia', 0),
        ('Penafrancia', 'Masinag', 3.1), ('Penafrancia', 'Cainta', 5.8), ('Penafrancia', 'Katipunan', 8.2),
        ('Penafrancia', 'Anonas', 8.9), ('Penafrancia', 'T.I.P.', 9.3),
        ('Masinag', 'Antipolo', 10.4), ('Masinag', 'Cogeo', 5.8), ('Masinag', 'Penafrancia', 3.1),
        ('Masinag', 'Masinag', 0), ('Masinag', 'Cainta', 2.1), ('Masinag', 'Katipunan', 6.0),
        ('Masinag', 'Anonas', 7.7), ('Masinag', 'T.I.P.', 8.5),
        ('Cainta', 'Antipolo', 10.6), ('Cainta', 'Cogeo', 6.6), ('Cainta', 'Penafrancia', 5.8),
        ('Cainta', 'Masinag', 2.1), ('Cainta', 'Cainta', 0), ('Cainta', 'Katipunan', 3.9),
        ('Cainta', 'Anonas', 5.6), ('Cainta', 'T.I.P.', 6.6),
        ('Katipunan', 'Antipolo', 15.2), ('Katipunan', 'Cogeo', 10.6), ('Katipunan', 'Penafrancia', 8.2),
        ('Katipunan', 'Masinag', 6.0), ('Katipunan', 'Cainta', 3.9), ('Katipunan', 'Katipunan', 0),
        ('Katipunan', 'Anonas', 1.0), ('Katipunan', 'T.I.P.', 1.3),
        ('Anonas', 'Antipolo', 16.7), ('Anonas', 'Cogeo', 11.5), ('Anonas', 'Penafrancia', 8.9),
        ('Anonas', 'Masinag', 7.7), ('Anonas', 'Cainta', 5.6), ('Anonas', 'Katipunan', 1.0),
        ('Anonas', 'Anonas', 0), ('Anonas', 'T.I.P.', 0.4),
        ('T.I.P.', 'Antipolo', 17.7), ('T.I.P.', 'Cogeo', 13.0), ('T.I.P.', 'Penafrancia', 9.3),
        ('T.I.P.', 'Masinag', 8.5), ('T.I.P.', 'Cainta', 6.6), ('T.I.P.', 'Katipunan', 1.3),
        ('T.I.P.', 'Anonas', 0.4), ('T.I.P.', 'T.I.P.', 0)
    ]
    cursor.executemany(
        "INSERT INTO routes (origin, destination, distance) VALUES (?, ?, ?)",
        routes_data
    )
    print("Inserted routes")

    # Insert Fares (from original code)
    fares_data = [
            (1, 15.00, 12.00), (2, 20.94, 16.75), (3, 25.34, 20.27), (4, 29.08, 23.26),
            (5, 29.52, 23.62), (6, 39.64, 31.71), (7, 42.94, 34.35), (8, 45.14, 36.11),
            (9, 20.94, 16.75), (10, 15.00, 12.00), (11, 15.00, 12.00), (12, 18.96, 15.17),
            (13, 20.72, 16.58), (14, 29.52, 23.62), (15, 31.50, 25.20), (16, 34.80, 27.84),
            (17, 25.34, 20.27), (18, 15.00, 12.00), (19, 15.00, 12.00), (20, 15.00, 12.00),
            (21, 18.96, 15.17), (22, 24.24, 19.39), (23, 25.78, 20.62), (24, 26.66, 21.33),
            (25, 29.08, 23.26), (26, 18.96, 15.17), (27, 15.00, 12.00), (28, 15.00, 12.00),
            (29, 15.00, 12.00), (30, 19.40, 15.52), (31, 23.14, 18.51), (32, 24.90, 19.92),
            (33, 29.52, 23.62), (34, 20.72, 16.58), (35, 18.96, 15.17), (36, 15.00, 12.00),
            (37, 15.00, 12.00), (38, 15.00, 12.00), (39, 18.52, 14.82), (40, 20.72, 16.58),
            (41, 39.64, 31.71), (42, 29.52, 23.62), (43, 24.24, 19.39), (44, 19.40, 15.52),
            (45, 15.00, 12.00), (46, 15.00, 12.00), (47, 15.00, 12.00), (48, 15.00, 12.00),
            (49, 42.94, 34.35), (50, 31.50, 25.20), (51, 25.78, 20.62), (52, 23.14, 18.51),
            (53, 20.72, 16.58), (54, 15.00, 12.00), (55, 15.00, 12.00), (56, 15.00, 12.00),
            (57, 45.14, 36.11), (58, 34.80, 27.84), (59, 26.66, 21.33), (60, 24.90, 19.92),
            (61, 20.72, 16.58), (62, 15.00, 12.00), (63, 15.00, 12.00), (64, 15.00, 12.00)
        ]

    cursor.executemany(
        "INSERT INTO fares (route_id, price_fare, discount_fare) VALUES (?, ?, ?)",
        fares_data
    )
    print("Inserted fares")

    # Insert Transactions
    transactions_data = [
        ('T001', 'C001', 1, 'V001', 'K001', 1, 15.00, '2024-01-01 08:00'),
        ('T002', 'C002',  2, 'V002', 'K002', 2, 20.94, '2024-01-01 08:15'),
        ('T003', 'C003',  3, 'V003', 'K003', 3, 25.34, '2024-01-01 08:30'),
        ('T004', 'C004',  4, 'V004', 'K004', 4, 29.08, '2024-01-01 08:45'),
        ('T005', 'C005',  5, 'V005', 'K005', 5, 29.52, '2024-01-01 09:00'),
    ]
    cursor.executemany(
        """INSERT INTO transactions 
        (transaction_id, commuter_id, route_id, vehicle_id, conductor_id, fare_id, total_fare, transaction_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        transactions_data
    )
    print("Inserted transactions")

    # Insert Feedbacks
    feedbacks_data = [
        ('C001', 'D001', 'K001', 4.5, 'Good service'),
        ('C002', 'D002', 'K002', 5.0, 'Excellent driver'),
        ('C003', 'D003', 'K003', 4.0, 'Comfortable ride'),
        ('C004', 'D004', 'K004', 3.5, 'Slightly late'),
        ('C005', 'D005', 'K005', 4.2, 'Clean vehicle'),
    ]
    cursor.executemany(
        """INSERT INTO feedbacks 
        (commuter_id, driver_id, conductor_id, rating, comment)
        VALUES (?, ?, ?, ?, ?)""",
        feedbacks_data
    )
    print("Inserted feedbacks")

    # Insert Vehicle Assignments
    assignments_data = [
        ('V001', 'D001', 'K001', '2024-01-01 07:00'),
        ('V002', 'D002', 'K002', '2024-01-01 07:15'),
        ('V003', 'D003', 'K003', '2024-01-01 07:30'),
        ('V004', 'D004', 'K004', '2024-01-01 07:45'),
        ('V005', 'D005', 'K005', '2024-01-01 08:00'),
    ]
    cursor.executemany(
        """INSERT INTO vehicle_assignment 
        (vehicle_id, driver_id, conductor_id, assignment_date)
        VALUES (?, ?, ?, ?)""",
        assignments_data
    )
    print("Inserted vehicle assignments")

    conn.commit()
    print("\nAll data inserted successfully!")

if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        insert_sample_data(conn)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()