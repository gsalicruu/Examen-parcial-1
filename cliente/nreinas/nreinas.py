import pygame
import sys
import threading
from ..comunicacion.cliente_tcp import ClienteTCP

class TableroReinas:
    def __init__(self, n):
        self.n = n
        self.tablero = [[0] * n for _ in range(n)]
        self.intentos = 0

    def es_seguro(self, fila, col):
        for i in range(self.n):
            if self.tablero[fila][i] == 1 or self.tablero[i][col] == 1:
                return False
        for i in range(-self.n, self.n):
            if 0 <= fila+i < self.n and 0 <= col+i < self.n and self.tablero[fila+i][col+i] == 1:
                return False
            if 0 <= fila+i < self.n and 0 <= col-i < self.n and self.tablero[fila+i][col-i] == 1:
                return False
        return True

    def colocar_reina(self, fila, col):
        if self.tablero[fila][col] == 0 and self.es_seguro(fila, col):
            self.tablero[fila][col] = 1
            self.intentos += 1
            return True
        return False

    def quitar_reina(self, fila, col):
        if self.tablero[fila][col] == 1:
            self.tablero[fila][col] = 0
            return True
        return False

    def solucion_valida(self):
        return sum(sum(fila) for fila in self.tablero) == self.n

def enviar_resultado(n, intentos):
    ClienteTCP().enviar_datos({
        "juego": "nreinas",
        "datos": {
            "tamano": n,
            "resuelto": True,
            "intentos": intentos
        }
    })

def main():
    pygame.init()
    N = 8
    tamaño = 600
    celda = tamaño // N
    pantalla = pygame.display.set_mode((tamaño, tamaño))
    pygame.display.set_caption("N Reinas")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 36)

    juego = TableroReinas(N)
    enviado = False
    mensaje = ""

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                fila = y // celda
                col = x // celda
                if juego.tablero[fila][col] == 1:
                    juego.quitar_reina(fila, col)
                else:
                    if juego.colocar_reina(fila, col):
                        mensaje = ""
                    else:
                        mensaje = "Movimiento inválido"

        pantalla.fill((255, 255, 255))
        for i in range(N):
            for j in range(N):
                rect = pygame.Rect(j*celda, i*celda, celda, celda)
                color = (240, 240, 240) if (i+j)%2==0 else (100, 100, 100)
                pygame.draw.rect(pantalla, color, rect)
                if juego.tablero[i][j] == 1:
                    pygame.draw.circle(pantalla, (255, 0, 0), rect.center, celda//3)

        if juego.solucion_valida() and not enviado:
            mensaje = "¡Has ganado!"
            threading.Thread(target=enviar_resultado, args=(N, juego.intentos)).start()
            enviado = True

        if mensaje:
            texto = fuente.render(mensaje, True, (0, 150, 0) if "ganado" in mensaje else (200, 0, 0))
            pantalla.blit(texto, (10, 10))

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    main()
