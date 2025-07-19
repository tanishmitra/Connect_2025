from sqlalchemy import create_engine, MetaData, Table

# Connect to the SQLite database
engine = create_engine('sqlite:///auth.db')
metadata = MetaData()

# Reflect the existing AuthTable
auth_table = Table('AuthTable', metadata, autoload_with=engine)

# Insert sample users
with engine.connect() as conn:
    conn.execute(auth_table.insert(), [
        {"UserName": "admin", "UserPassword": "admin123"},
        {"UserName": "test", "UserPassword": "testpass"}
    ])
    conn.commit()  # Ensure the changes are saved
    print(" Sample users inserted.")

