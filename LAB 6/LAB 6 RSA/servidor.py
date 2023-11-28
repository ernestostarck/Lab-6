import socket
import rsa

# Ruta del archivo de entrada 
archivo_entrada = 'mensajeentrada.txt'

# Configurar el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen(1)
print("Esperando una conexión...")

# Aceptar la conexión
client, addr = server.accept()
print("Conexión establecida desde", addr)

# Recibir la clave pública del cliente
data = client.recv(1024)
cliente_pub = rsa.PublicKey.load_pkcs1(data)

print("Llave Recibida de :", addr)

# Abrir mensaje
with open(archivo_entrada, 'rb') as f:
    mensaje = f.read()
    
print("Mensaje Leido")

# Encriptar el mensaje
mensaje_encriptado = rsa.encrypt(mensaje, cliente_pub)

print("Mensaje cifrado : \n", mensaje_encriptado)

# Enviar mensaje cifrado al cliente
client.send(mensaje_encriptado)

print("Mensaje cifrado enviado")
# Cerrar conexiones
client.close()
server.close()
