import socket
import pickle
import random

def cifrar(mensaje, p, g, y):
    valores_ascii = [ord(char) for char in mensaje]
    k = random.randint(2, p - 2)
    a = pow(g, k, p)
    b = [(pow(y, k, p) * valor) % p for valor in valores_ascii]
    return a, b

# Parámetros del sistema
p = 7919

# Crear socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Recibir clave pública del servidor
clave_publica = pickle.loads(client_socket.recv(1024))
print("Clave pública recibida del servidor: (p={}, g={}, y={})".format(*clave_publica))

# Leer mensaje del archivo de texto
with open("mensajeentrada.txt", "r") as archivo:
    mensaje_original = archivo.read()
print("Mensaje original:", mensaje_original)

# Cifrar mensaje y enviar al servidor
mensaje_cifrado = cifrar(mensaje_original, *clave_publica)
print("Mensaje cifrado enviado al servidor:", mensaje_cifrado)
client_socket.send(pickle.dumps(mensaje_cifrado))

# Cerrar conexión
client_socket.close()
