import socket
import pickle

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generar_claves(p):
    g = 2
    x = 3
    y = pow(g, x, p)
    return g, x, y

def descifrar(a, b, x, p):
    s = pow(a, x, p)
    s_inv = modinv(s, p)
    valores_descifrados = [(valor * s_inv) % p for valor in b]
    mensaje = ''.join([chr(valor) for valor in valores_descifrados])
    return mensaje

# Parámetros del sistema
p = 7919

# Crear socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print("Esperando conexión del cliente...")

# Aceptar conexión del cliente
client_socket, client_address = server_socket.accept()
print("Conexión establecida con:", client_address)

# Generar claves y enviar clave pública al cliente
g, x, y = generar_claves(p)
print("Clave pública enviada al cliente: (p={}, g={}, y={})".format(p, g, y))
client_socket.send(pickle.dumps((p, g, y)))

# Recibir mensaje cifrado del cliente
mensaje_cifrado = pickle.loads(client_socket.recv(1024))
print("Mensaje cifrado recibido:", mensaje_cifrado)

# Descifrar mensaje
mensaje_descifrado = descifrar(mensaje_cifrado[0], mensaje_cifrado[1], x, p)
print("Mensaje descifrado:", mensaje_descifrado)

# Guardar mensaje descifrado en un archivo de texto
with open("mensajerecibido.txt", "w") as archivo:
    archivo.write(mensaje_descifrado)

# Cerrar conexiones
client_socket.close()
server_socket.close()
