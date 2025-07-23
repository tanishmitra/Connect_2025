from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Table, Column, String, MetaData, select

app = Flask(__name__)
CORS(app)

# SQLite DB connection
engine = create_engine('sqlite:///auth.db', echo=True)
metadata = MetaData()

# Define AuthTable schema
auth_table = Table('AuthTable', metadata,
                   Column('UserName', String, primary_key=True),
                   Column('UserPassword', String))

# Create the table if it doesn't exist
metadata.create_all(engine)

# POST /login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('UserName')
    password = data.get('UserPassword')

    with engine.connect() as conn:
        stmt = select(auth_table).where(
            auth_table.c.UserName == username,
            auth_table.c.UserPassword == password
        )
        result = conn.execute(stmt).fetchone()

        if result:
            return jsonify({"Message": "SuccessLogin"})
        else:
            return jsonify({"Message": "FailureLogin"})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('UserName')
    password = data.get('UserPassword')

    with engine.begin() as conn:
        stmt = select(auth_table).where(auth_table.c.UserName == username)
        existing_user = conn.execute(stmt).fetchone()

        if existing_user:
            return jsonify({"Message": "UserAlreadyExists"}), 409

        conn.execute(auth_table.insert().values(UserName=username, UserPassword=password))
        return jsonify({"Message": "SuccessSignup"}), 201


# Run the app
if __name__ == '__main__':
    app.run(port=8787)
