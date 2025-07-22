from sqlalchemy import create_engine, Table, Column, String, MetaData, select

# Connect to the SQLite DB
engine = create_engine('sqlite:///auth.db', echo=True)
metadata = MetaData()

# Define the AuthTable
auth_table = Table('AuthTable', metadata,
                   Column('UserName', String, primary_key=True),
                   Column('UserPassword', String))

# List of users to add
new_users = [
    {"UserName": "admin", "UserPassword": "admin123"},
    {"UserName": "test", "UserPassword": "testpass"},
    {"UserName": "newuser1", "UserPassword": "newpass1"},
    {"UserName": "newuser2", "UserPassword": "newpass2"}
]

# Insert only if user doesn't exist
with engine.connect() as conn:
    for user in new_users:
        stmt = select(auth_table).where(auth_table.c.UserName == user["UserName"])
        result = conn.execute(stmt).fetchone()
        if result:
            print(f"User '{user['UserName']}' already exists. Skipping.")
        else:
            conn.execute(auth_table.insert().values(user))
            print(f"Inserted user '{user['UserName']}'.")

print("Done seeding users.")
