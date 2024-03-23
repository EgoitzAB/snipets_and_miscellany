from flask import Flask, request, jsonify, render_template
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import hashlib

app = Flask(__name__)

# Generate a global key pair to be used throughout
private_key = RSA.generate(2048)
public_key = private_key.publickey()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Generate a new key pair
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()

        # Show the keys to the user
        return render_template('home.html', public_key=public_key.export_key().decode(), private_key=private_key.export_key().decode())
    else:
        # Show the home page
        return render_template('home.html')

@app.route('/generate_keys', methods=['GET'])
def generate_keys():
    # Export the keys and return them as strings
    return jsonify({
        'public_key': public_key.export_key().decode(),
        'private_key': private_key.export_key().decode()
    })

@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    # Get the message from the request
    message = request.json.get('message')

    # Hash the message
    message_hash = hashlib.sha256(message.encode()).hexdigest()

    # Encrypt the message
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message_hash.encode())

    # Return the encrypted message as a base64 encoded string
    return jsonify({
        'encrypted_message': base64.b64encode(encrypted_message).decode()
    })

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    # Get the encrypted message from the request
    encrypted_message = request.json.get('encrypted_message')

    # Decrypt the message
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))

    # Verify the hash
    original_message = request.json.get('original_message')
    original_message_hash = hashlib.sha256(original_message.encode()).hexdigest()
    if original_message_hash != decrypted_message.decode():
        return jsonify({'error': 'Hash verification failed'}), 400

    # Return the decrypted message
    return jsonify({
        'decrypted_message': decrypted_message.decode()
    })

if __name__ == '__main__':
    app.run(debug=True)