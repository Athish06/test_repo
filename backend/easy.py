from flask import Flask, request
import sqlite3
import os
import pickle

app = Flask(__name__)

# [Easy 1] Hardcoded Secret
JWT_SECRET = "super_secret_jwt_key_123_production"

@app.route('/api/users')
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # [Easy 2] SQL Injection (String Concatenation)
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return str(cursor.fetchall())

@app.route('/api/ping')
def ping_server():
    ip_address = request.args.get('ip')
    # [Easy 3] Command Injection
    result = os.system("ping -c 4 " + ip_address)
    return str(result)

@app.route('/api/logs')
def read_log():
    filename = request.args.get('file')
    # [Easy 4] Path Traversal
    with open("/var/logs/" + filename, "r") as f:
        return f.read()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db_password = "password123" # Mock DB fetch
    # [Easy 5] Plaintext Password Comparison
    if data.get('password') == db_password:
        return "Logged in!"
    return "Failed"

# [Easy 6] Missing Authentication (Admin route lacking @require_auth)
@app.route('/api/admin/delete_all_users', methods=['POST'])
def delete_all_users():
    # Destructive action without checking if user is an admin
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM users")
    return "All users deleted."

@app.route('/api/import', methods=['POST'])
def import_data():
    data = request.data
    # [Easy 7] Insecure Deserialization
    obj = pickle.loads(data)
    return "Imported successfully."

if __name__ == "__main__":
    # [Easy 8] Debug Mode Enabled
    app.run(host="0.0.0.0", port=8080, debug=True)
