import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(("localhost", 5000))

while True:
    mensaje = input("Ingrese un mensaje: ")
    cliente.send(mensaje.encode())
    if mensaje.lower() == "salir":
        break
    respuesta = cliente.recv(1024).decode()

    print("Respuesta del servidor:", respuesta)

cliente.close()
