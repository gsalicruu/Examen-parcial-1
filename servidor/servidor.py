import socket
import threading
import json
from .modelos import Session, Resultado

def manejar_cliente(conn, addr):
    print(f"[SERVIDOR] Conexión desde {addr}")
    try:
        datos = conn.recv(1024).decode('utf-8')
        datos_json = json.loads(datos)
        print(f"[SERVIDOR] Datos recibidos: {datos_json}")

        session = Session()
        resultado = Resultado(juego=datos_json['juego'], datos=json.dumps(datos_json['datos']))
        session.add(resultado)
        session.commit()
        session.close()

        conn.sendall(b"Resultado guardado correctamente.")
    except Exception as e:
        print(f"[SERVIDOR] Error: {e}")
        conn.sendall(b"Error al procesar los datos.")
    finally:
        conn.close()

def main():
    host = '127.0.0.1'
    puerto = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, puerto))
        s.listen()
        print(f"[SERVIDOR] Escuchando en {host}:{puerto}")
        while True:
            conn, addr = s.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo.start()

if __name__ == "__main__":
    main()
