from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import os
import secrets



app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = secrets.token_hex(16)
    os.environ['FLASK_SECRET_KEY'] = SECRET_KEY

app.secret_key = SECRET_KEY

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    return User(username) if db.users.find_one({'username': username}) else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    db.users.insert_one({'username': username, 'public_key': public_key.export_key().decode(), 'password': generate_password_hash(password)})
    return jsonify({'private_key': private_key.export_key().decode()})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        login_user(User(username))
        return 'Logged in'
    else:
        return 'Invalid username or password', 401

@app.route('/public_key', methods=['GET'])
def public_key():
    username = request.args.get('username')
    user = db.users.find_one({'username': username})
    if user:
        return jsonify({'public_key': user['public_key']})
    else:
        return 'User not found', 404

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    recipient = request.form['recipient']
    message = request.form['message']
    db.messages.insert_one({'sender': current_user.id, 'recipient': recipient, 'message': message})
    return 'Message sent'

@app.route('/receive_messages', methods=['GET'])
@login_required
def receive_messages():
    messages = db.messages.find({'recipient': current_user.id})
    return jsonify([{'sender': message['sender'], 'message': message['message']} for message in messages])

if __name__ == '__main__':
    app.run(debug=True)