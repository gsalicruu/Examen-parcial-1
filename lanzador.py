import pygame
import subprocess
import sys

def lanzar_juego(modulo):
    cmd = [sys.executable, "-m", modulo]
    subprocess.Popen(cmd)

def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Máquina Arcade")
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    botones = [
        {"texto": "N Reinas", "rect": pygame.Rect(180, 50, 150, 50), "modulo": "cliente.nreinas.nreinas"},
        {"texto": "Recorrido del Caballo", "rect": pygame.Rect(100, 120, 320, 50), "modulo": "cliente.caballo.caballo"},
        {"texto": "Torres de Hanói", "rect": pygame.Rect(145, 190, 230, 50), "modulo": "cliente.hanoi.hanoi"},
    ]

    while True:
        screen.fill((30, 30, 30))
        for boton in botones:
            pygame.draw.rect(screen, (255, 200, 100), boton["rect"])
            texto = font.render(boton["texto"], True, (0, 0, 0))  
            texto_rect = texto.get_rect(center=boton["rect"].center)
            screen.blit(texto, texto_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton["rect"].collidepoint(event.pos):
                        lanzar_juego(boton["modulo"])

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
