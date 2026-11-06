import socket
import threading

inventario = {
    1:{"nombre":"camiseta","stock":2},
    2:{"nombre":"pantalon","stock":3}
}

id_contador = 4

lock = threading.Lock()

def manejarCLientes(conexion, direccion):
    print(f"Cliente conectado desde: {direccion}")
    try:

        while True:
            mensaje_bytes = conexion.recv(1024)
            if not mensaje_bytes:
                break
            mensaje = mensaje_bytes.decode().strip()
            print(f"Comando recibido de: {direccion}: {mensaje}")
            if mensaje.lower()=="salir":
                conexion.send("Conexion cerrada.\n".encode())
                break
            partes = mensaje.split(":")
            comando = partes[0].upper()
            respuesta = ""

            if comando == "LISTAR":
                with lock:
                    if not inventario:
                        respuesta = "El inventario esta vacio.\n"
                    else:
                        respuesta = "--- INVENTARIO DISPONIBLE --- \n"
                        for prod_id, datos in inventario.items():
                            respuesta += f"ID: {prod_id} | Nombre: {datos['nombre']} | Stock: {datos['stock']}\n"
            elif comando == "AGREGAR":
                if len(partes)==3:
                    nombre = partes[3]
                    try:
                        stock = int(partes[2])
                        global id_contador
                        with lock:
                            nuevo_id = id_contador
                            inventario[nuevo_id] = {"nombre": nombre, "stock": stock}
                            id_contador += 1
                        respuesta = f"Producto agregado correctamente ID asignado: {nuevo_id}\n"
                    except ValueError:
                        respuesta = "Error: el stock debe ser un numero entero.\n"
                else:
                    respuesta = "Error de formato. Use: AGREGAR:Nombre:Stock\n"
            elif comando == "COMPRAR":
                if len(partes)==3:
                    try:
                        prod_id = int(partes[1])
                        cantidad = int(partes[2])
                        with lock:
                            if prod_id in inventario:
                                if inventario[prod_id]["stock"]>=cantidad:
                                    inventario[prod_id]["stock"] -= cantidad
                                    respuesta = f"Compra exitosa Stock restante de: '{inventario[prod_id]['nombre']}':{inventario[prod_id]['stock']}\n"
                                else:
                                    respuesta = "Error Stock insuficiente" 
        conexion.close()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(("localhost", 5000))

servidor.listen()

print("Servidor TCP esperando conexión ...")


while True:
    conexion, direccion = servidor.accept()
    hilo=threading.Thread(target=manejarCLientes, args= (conexion, direccion))
    hilo.start()