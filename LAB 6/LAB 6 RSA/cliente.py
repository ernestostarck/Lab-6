import socket
import rsa

# Ruta del archivo de entrada 
archivo_salida = 'mensajerecibido.txt'

# Configurar el cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

# Crear las claves pública y privada
(cliente_pub, cliente_priv) = rsa.newkeys(512)

# Enviar la clave pública al servidor
client.send(cliente_pub.save_pkcs1())

# Recibir mensaje encriptado
mensaje_encriptado = client.recv(1024)

# Desencripta el mensaje 
mensaje = rsa.decrypt(mensaje_encriptado, cliente_priv)
print(mensaje.decode('utf8'))

# Guarda el mensaje desencriptado
with open(archivo_salida, 'wb') as f:
    f.write(mensaje)
    
print("Mensaje guardado")
# Cerrar la conexión
client.close()
