import pygame
import sys
import threading
from ..comunicacion.cliente_tcp import ClienteTCP

class Disco:
    def __init__(self, ancho):
        self.ancho = ancho

class Torre:
    def __init__(self):
        self.discos = []

    def agregar(self, disco):
        if not self.discos or disco.ancho < self.discos[-1].ancho:
            self.discos.append(disco)
            return True
        return False

    def quitar(self):
        return self.discos.pop() if self.discos else None

    def esta_ordenada(self, num_discos):
        return len(self.discos) == num_discos and all(
            self.discos[i].ancho > self.discos[i+1].ancho
            for i in range(len(self.discos)-1)
        )

class JuegoHanoi:
    def __init__(self, num_discos):
        self.torres = [Torre() for _ in range(3)]
        for i in range(num_discos, 0, -1):
            self.torres[0].agregar(Disco(i))
        self.num_discos = num_discos
        self.movimientos = 0
        self.origen = None
        self.disco_en_mano = None

    def seleccionar_origen(self, idx):
        if self.torres[idx].discos:
            self.origen = idx
            self.disco_en_mano = self.torres[idx].quitar()
            return True
        return False

    def mover_a(self, destino):
        if self.disco_en_mano:
            if self.torres[destino].agregar(self.disco_en_mano):
                self.movimientos += 1
                self.origen = None
                self.disco_en_mano = None
                return True
            else:
                self.torres[self.origen].agregar(self.disco_en_mano)
                self.disco_en_mano = None
                self.origen = None
        return False

    def resuelto(self):
        return (
            self.torres[1].esta_ordenada(self.num_discos)
            or self.torres[2].esta_ordenada(self.num_discos)
        )

def enviar_resultado(discos, movimientos):
    ClienteTCP().enviar_datos({
        "juego": "hanoi",
        "datos": {
            "discos": discos,
            "movimientos": movimientos,
            "resuelto": True
        }
    })

def main():
    pygame.init()
    num_discos = 4
    juego = JuegoHanoi(num_discos)
    pantalla = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Torres de Hanói")
    fuente = pygame.font.SysFont(None, 36)
    reloj = pygame.time.Clock()
    mensaje = ""
    enviado = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    idx = int(evento.unicode) - 1
                    if juego.disco_en_mano is None:
                        juego.seleccionar_origen(idx)
                    else:
                        juego.mover_a(idx)

        pantalla.fill((250, 250, 250))
        ancho_base = 120
        alto_disco = 20
        for i, torre in enumerate(juego.torres):
            x_base = 100 + i * 200
            pygame.draw.rect(pantalla, (120, 60, 0), (x_base + ancho_base//2 - 5, 100, 10, 200))
            for j, disco in enumerate(reversed(torre.discos)):
                ancho_px = disco.ancho * 20
                y = 300 - j * alto_disco
                pygame.draw.rect(pantalla, (0, 100, 200), (x_base + ancho_base//2 - ancho_px//2, y, ancho_px, alto_disco))

        texto = fuente.render(f"Movimientos: {juego.movimientos}", True, (0, 0, 0))
        pantalla.blit(texto, (10, 10))

        if juego.disco_en_mano:
            ancho_px = juego.disco_en_mano.ancho * 20
            pygame.draw.rect(pantalla, (255, 100, 0), (300 - ancho_px//2, 360, ancho_px, alto_disco))

        if juego.resuelto() and not enviado:
            mensaje = "¡Has ganado!"
            threading.Thread(target=enviar_resultado, args=(num_discos, juego.movimientos)).start()
            enviado = True

        if mensaje:
            pantalla.blit(fuente.render(mensaje, True, (0, 150, 0)), (200, 10))

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    main()
