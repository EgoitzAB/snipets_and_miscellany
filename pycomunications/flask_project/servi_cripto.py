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

# Configuración del servidor
host = '127.0.0.1'
port = 12345

# Generar par de claves
clave_publica, clave_privada = generar_par_claves()

# Establecer conexión
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    print('Esperando conexiones en {}:{}'.format(host, port))
    conn, addr = s.accept()
    with conn:
        print('Conexión establecida desde:', addr)

        # Enviar clave pública al cliente
        enviar_clave_publica(conn, clave_publica)

        # Recibir clave pública del cliente
        clave_publica_cliente = conn.recv(1024)

        while True:
            # Recibir el mensaje cifrado del cliente
            ciphertext_recibido = conn.recv(1024)

            # Descifrar el mensaje cifrado
            cipher = PKCS1_OAEP.new(RSA.import_key(clave_privada))
            mensaje_descifrado = cipher.decrypt(ciphertext_recibido)

            # Calcular el hash del mensaje descifrado
            hash_mensaje_descifrado = hash_mensaje(mensaje_descifrado)

            # Recibir el hash del cliente
            hash_recibido = conn.recv(32)

            if not ciphertext_recibido:
                break

            # Comparar el hash recibido con el hash calculado localmente
            if hash_mensaje_descifrado == hash_recibido:
                print('Mensaje recibido del cliente:', mensaje_descifrado.decode())
            else:
                print('Error: El mensaje fue alterado durante la transmisión.')
