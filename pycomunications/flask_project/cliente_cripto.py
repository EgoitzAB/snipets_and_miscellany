from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket
import hashlib

def generar_par_claves():
    # Generar par de claves RSA de 2048 bits
    key = RSA.generate(2048)
    # Exportar clave pública y privada
    public_key = key.publickey().export_key()
    private_key = key.export_key()
    return public_key, private_key

def enviar_clave_publica(socket, clave_publica):
    # Enviar la clave pública al otro extremo
    socket.sendall(clave_publica)

def cifrar_mensaje(clave_publica, mensaje):
    # Crear un objeto cipher utilizando la clave pública
    cipher = PKCS1_OAEP.new(RSA.import_key(clave_publica))
    # Cifrar el mensaje
    ciphertext = cipher.encrypt(mensaje)
    return ciphertext

def hash_mensaje(mensaje):
    # Crea un hash SHA-256 del mensaje
    hash_obj = hashlib.sha256()
    hash_obj.update(mensaje)
    return hash_obj.digest()

# Configuración del cliente
host = '127.0.0.1'
port = 12345

# Generar par de claves
clave_publica, clave_privada = generar_par_claves()

# Establecer conexión
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    # Recibir clave pública del servidor
    clave_publica_servidor = s.recv(1024)

    # Enviar clave pública al servidor
    enviar_clave_publica(s, clave_publica)

    while True:
        mensaje = input("Mensaje del cliente: ")
        if mensaje.lower() == 'exit':
            s.sendall(mensaje.encode())
            break

        # Calcular el hash del mensaje
        hash_mensaje_enviado = hash_mensaje(mensaje.encode())

        # Cifrar el mensaje
        ciphertext = cifrar_mensaje(clave_publica_servidor, mensaje.encode())

        # Enviar el mensaje cifrado al servidor
        s.sendall(ciphertext)

        # Enviar el hash del mensaje al servidor
        s.sendall(hash_mensaje_enviado)

        if not mensaje:
            break
