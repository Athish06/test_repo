from flask import Flask, request
import sqlite3
import hmac
import subprocess
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["testdb"]

@app.route('/api/profile/save', methods=['POST'])
def save_profile():
    # Phase 1 of Second-Order SQLi (Safe Insert)
    bio = request.json.get('bio')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profiles (bio) VALUES (?)", (bio,))
    conn.commit()
    return "Saved"

@app.route('/api/profile/view')
def view_profile():
    # [Hard 1] Second-Order SQL Injection
    # The 'bio' was safely inserted, but is retrieved and concatenated unsafely here.
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT bio FROM profiles ORDER BY id DESC LIMIT 1")
    bio = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM users WHERE description = '" + bio + "'")
    return str(cursor.fetchall())

@app.route('/api/settings/update', methods=['POST'])
def update_settings():
    current_user_id = 42
    data = request.json
    # [Hard 2] Sneaky IDOR
    # Attacker passes {"target_user_id": 1} in the body to override the authenticated user.
    target_id = data.get('target_user_id', current_user_id)
    conn = sqlite3.connect('database.db')
    conn.execute("UPDATE settings SET theme = ? WHERE user_id = ?", (data.get('theme'), target_id))
    return "Updated"

@app.route('/api/system/reset', methods=['PUT'])
def reset_system():
    # [Hard 3] HTTP Verb Bias Trap (Destructive action via PUT instead of DELETE)
    # The AI must catch this logic flaw despite it not being a DELETE request.
    target_table = request.json.get('table_name')
    conn = sqlite3.connect('database.db')
    # SQLi in a PUT request
    conn.execute(f"DROP TABLE {target_table}")
    return "System reset"

@app.route('/api/verify_webhook', methods=['POST'])
def verify():
    signature = request.headers.get('X-Signature')
    expected_signature = hmac.new(b"secret", request.data, "sha256").hexdigest()
    # [Hard 4] Timing Attack
    # Using == instead of hmac.compare_digest allows timing attacks to guess the signature
    if signature == expected_signature:
        return "Verified"
    return "Denied"

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    # [Hard 5] Logic Bypass
    # If the attacker simply omits the 'payment_token' field, the validation is completely bypassed.
    if 'payment_token' in data:
        if not validate_payment(data['payment_token']):
            return "Payment failed", 400
    
    # Process order...
    return "Order complete"

def validate_payment(token):
    return token == "valid"

class AppConfig:
    def __init__(self):
        self.maintenance_mode = False

@app.route('/api/config/set', methods=['POST'])
def set_config():
    config = AppConfig()
    data = request.json
    # [Hard 6] Server-Side Attribute Override
    # Attacker can send {"__class__": ...} or override maintenance_mode dynamically
    for key, value in data.items():
        setattr(config, key, value)
    return "Config applied"

@app.route('/api/search_users', methods=['POST'])
def search_users():
    # [Hard 7] NoSQL Injection
    # Attacker sends {"username": {"$gt": ""}} to dump all users
    query = request.json
    users = list(db.users.find(query))
    return str(users)

@app.route('/api/background_process', methods=['POST'])
def process_data():
    filename = request.json.get('filename')
    # [Hard 8] Blind Command Injection
    # Interpolated string passed to shell=True, but output is never returned to the user.
    subprocess.Popen(f"process_tool.sh {filename}", shell=True)
    return "Processing started in background"
