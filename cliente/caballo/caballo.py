import pygame
import sys
import threading
from ..comunicacion.cliente_tcp import ClienteTCP

class TableroCaballo:
    def __init__(self, n):
        self.n = n
        self.tablero = [[0]*n for _ in range(n)]
        self.movimientos = 0
        self.x = 0
        self.y = 0
        self.tablero[self.y][self.x] = 1
        self.orden = [(self.x, self.y)]
        self.mov_caballo = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

    def mover(self, nx, ny):
        if 0 <= nx < self.n and 0 <= ny < self.n and self.tablero[ny][nx] == 0:
            if (abs(self.x - nx), abs(self.y - ny)) in [(abs(a), abs(b)) for a, b in self.mov_caballo]:
                self.x, self.y = nx, ny
                self.tablero[ny][nx] = 1
                self.orden.append((nx, ny))
                self.movimientos += 1
                return True
        return False

    def completado(self):
        return all(all(cell == 1 for cell in row) for row in self.tablero)

    def sin_movimientos_validos(self):
        for dx, dy in self.mov_caballo:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < self.n and 0 <= ny < self.n and self.tablero[ny][nx] == 0:
                return False
        return True

def enviar_resultado(pos_inicial, movimientos, completado):
    ClienteTCP().enviar_datos({
        "juego": "caballo",
        "datos": {
            "inicio": pos_inicial,
            "movimientos": movimientos,
            "completado": completado
        }
    })

def main():
    pygame.init()
    N = 8
    tamaño = 600
    celda = tamaño // N
    pantalla = pygame.display.set_mode((tamaño, tamaño))
    pygame.display.set_caption("Recorrido del Caballo")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 36)

    juego = TableroCaballo(N)
    enviado = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // celda
                fila = y // celda
                juego.mover(col, fila)

        pantalla.fill((255, 255, 255))
        for i in range(N):
            for j in range(N):
                rect = pygame.Rect(j*celda, i*celda, celda, celda)
                color = (230, 230, 230) if (i+j)%2==0 else (80, 80, 80)
                pygame.draw.rect(pantalla, color, rect)
                if juego.tablero[i][j]:
                    pygame.draw.circle(pantalla, (0, 0, 255), rect.center, celda//4)

        pygame.draw.circle(pantalla, (255, 0, 0), ((juego.x+0.5)*celda, (juego.y+0.5)*celda), celda//3)

        if juego.completado() and not enviado:
            pantalla.blit(fuente.render("¡Recorrido completo!", True, (0, 200, 0)), (10, 10))
            threading.Thread(target=enviar_resultado, args=(f"{juego.orden[0]}", juego.movimientos, True)).start()
            enviado = True
        elif juego.sin_movimientos_validos() and not enviado:
            pantalla.blit(fuente.render("¡Sin movimientos válidos!", True, (200, 0, 0)), (10, 10))
            threading.Thread(target=enviar_resultado, args=(f"{juego.orden[0]}", juego.movimientos, False)).start()
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    main()
