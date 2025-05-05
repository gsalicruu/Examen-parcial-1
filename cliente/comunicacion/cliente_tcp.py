import socket
import threading
import json

class ClienteTCP:
    def __init__(self, host='127.0.0.1', puerto=65432):
        self.host = host
        self.puerto = puerto

    def enviar_datos(self, datos):
        def run():
            try:
                with socket.create_connection((self.host, self.puerto)) as sock:
                    mensaje = json.dumps(datos).encode('utf-8')
                    sock.sendall(mensaje)
                    respuesta = sock.recv(1024).decode('utf-8')
                    print(f"[CLIENTE] Respuesta del servidor: {respuesta}")
            except Exception as e:
                print(f"[CLIENTE] Error al enviar datos: {e}")

        hilo = threading.Thread(target=run)
        hilo.start()
