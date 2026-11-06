import socket
import threading

def manejarCLientes(conexion, direccion):
    while True:
        print("Cliente conectado desde:", direccion)
        mensaje = conexion.recv(1024)
        print("Mensaje recibido:", mensaje.decode())
        if mensaje.decode().lower()=="salir":
            break
        respuesta = "Hola cliente, mensaje recibido correctamente"
        conexion.send(respuesta.encode())
    conexion.close()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(("localhost", 5000))

servidor.listen()

print("Servidor TCP esperando conexión ...")


while True:
    conexion, direccion = servidor.accept()
    hilo=threading.Thread(target=manejarCLientes, args= (conexion, direccion))
    hilo.start()