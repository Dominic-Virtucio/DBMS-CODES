import sqlite3

DATABASE_NAME = 'transport_app.db'

def drop_all_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Disable foreign key constraints to prevent errors during drop
    cursor.execute('PRAGMA foreign_keys = OFF;')

    # Drop tables in order: child tables first, then parent tables
    tables = [
        'vehicle_assignment',
        'feedbacks',
        'transactions',
        'fares',
        'routes',
        'vehicles',
        'conductors',
        'drivers',
        'admins',
        'commuters',
        'users'
    ]

    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS {table};')
        print(f'Dropped table {table}')

    # If you have views, drop them as well (example for route_view)
    cursor.execute('DROP VIEW IF EXISTS route_view;')

    # Re-enable foreign key constraints
    cursor.execute('PRAGMA foreign_keys = ON;')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    drop_all_tables()
