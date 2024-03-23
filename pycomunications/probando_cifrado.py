from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket

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

def descifrar_mensaje(clave_privada, ciphertext):
    # Crear un objeto cipher utilizando la clave privada
    cipher = PKCS1_OAEP.new(RSA.import_key(clave_privada))
    # Descifrar el mensaje
    mensaje = cipher.decrypt(ciphertext)
    return mensaje

# Configuración del servidor
host = '127.0.0.1'
port = 12345

# Generar par de claves
clave_publica, clave_privada = generar_par_claves()

# Establecer conexión
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Conexión establecida desde:', addr)

        # Enviar clave pública al cliente
        enviar_clave_publica(conn, clave_publica)

        # Recibir clave pública del cliente
        clave_publica_cliente = conn.recv(1024)

        # Cifrar y enviar mensaje
        mensaje = b'Hola, mundo!'
        ciphertext = cifrar_mensaje(clave_publica_cliente, mensaje)
        conn.sendall(ciphertext)

        # Recibir y descifrar mensaje
        ciphertext_recibido = conn.recv(1024)
        mensaje_descifrado = descifrar_mensaje(clave_privada, ciphertext_recibido)
        print('Mensaje recibido:', mensaje_descifrado.decode())
