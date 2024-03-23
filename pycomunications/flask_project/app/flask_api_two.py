from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, UserMixin, current_user
from flask_socketio import SocketIO, emit
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os
import jwt

app = Flask(__name__)
socketio = SocketIO(app)

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_secret_key')

# Dummy user database
users = {}

class User(UserMixin):
    def __init__(self, username, public_key):
        self.id = username
        self.public_key = public_key

@login_manager.user_loader
def load_user(username):
    return users.get(username)

@app.route('/')
def home():
    return render_template('index_one.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    # Save user to the database
    users[username] = User(username, public_key)

    # Generate JWT token
    token_data = {
        'username': username,
        'private_key': private_key.export_key().decode(),
        'public_key': public_key.export_key().decode()
    }
    token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token.decode()})

@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        username = decoded_token['username']
        if username in users:
            # Authenticate user
            users[username].authenticated = True
            print('User connected: ' + username)
        else:
            print('Invalid token')
            return False  # Reject connection if token is invalid
    except jwt.ExpiredSignatureError:
        print('Token expired')
        return False  # Reject connection if token is expired

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        current_user.authenticated = False
        print('User disconnected: ' + current_user.id)

@socketio.on('send_message')
def send_message(data):
    recipient_username = data['recipient']
    recipient_public_key = users[recipient_username].public_key
    message = data['message']
    cipher_rsa = PKCS1_OAEP.new(recipient_public_key)
    encrypted_message = cipher_rsa.encrypt(message.encode())
    recipient_socket_id = users[recipient_username].socket_id
    if recipient_socket_id:
        emit('receive_message', {'sender': current_user.id, 'message': base64.b64encode(encrypted_message).decode()}, room=recipient_socket_id)
    else:
        print('Recipient socket ID not found for user: ' + recipient_username)

if __name__ == '__main__':
    socketio.run(app, debug=True)
