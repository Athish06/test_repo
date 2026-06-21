from flask import Flask, request, jsonify
import requests
import hashlib
import re
from lxml import etree

app = Flask(__name__)

class User:
    def __init__(self):
        self.is_admin = False
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@app.route('/api/webhook', methods=['POST'])
def trigger_webhook():
    data = request.json
    target_url = data.get('url')
    # [Medium 1] SSRF (Server-Side Request Forgery)
    response = requests.get(target_url)
    return response.text

@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    data = request.json
    user = User()
    # [Medium 2] Mass Assignment
    # Attacker can send {"is_admin": True} and elevate privileges
    user.update(**data)
    return "Profile updated"

@app.route('/api/users/<int:user_id>/documents')
def get_user_documents(user_id):
    current_user_id = 42 # Mock authenticated user
    # [Medium 3] IDOR / Broken Access Control
    # Fetches documents for user_id without verifying if current_user_id == user_id
    documents = {"1": "Tax Return", "2": "Medical Records"}
    return jsonify({"docs": documents})

@app.route('/api/generate_token')
def generate_token():
    user_seed = request.args.get('seed', 'default')
    # [Medium 4] Weak Cryptography
    token = hashlib.md5(user_seed.encode()).hexdigest()
    return token

@app.route('/api/validate_email', methods=['POST'])
def validate():
    email = request.json.get('email', '')
    # [Medium 5] ReDoS (Catastrophic Backtracking)
    # The regex ^([a-zA-Z0-9]+\s?)*$ is vulnerable to catastrophic backtracking
    if re.match(r"^([a-zA-Z0-9]+\s?)*$", email):
        return "Valid"
    return "Invalid"

@app.route('/api/upload_xml', methods=['POST'])
def upload_xml():
    xml_data = request.data
    # [Medium 6] XML External Entity (XXE)
    parser = etree.XMLParser(resolve_entities=True)
    tree = etree.fromstring(xml_data, parser)
    return "XML Parsed"
