class obj:
    def __init__(self,x,y,hb):
        self.CordX=x
        self.CordY=y
        self.HB=hb #Hit Box (só pra ver se é atravessavel)
    def Move(self, x, y):
        self.CordX = x
        self.CordY = y

class walker(obj):
    def __init__(self, x, y, hb):
        super().__init__(x, y, hb)
        self.PassedCords = []  # Lista de coordenadas passadas
        # sentidos norte = 0, leste = 1, sul = 2, oeste = 3
        self.sentido = 0
    def AddCord(self, x, y):
        self.PassedCords.append((x, y))


RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
import random

def GenLab(m, n):
    # força dimensões ímpares
    if m % 2 == 0: m -= 1
    if n % 2 == 0: n -= 1

    # cria grid inicial cheio de paredes
    grid = [[obj(x, y, True) for y in range(n)] for x in range(m)]

    direcoes = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    def dentro(x, y):
        return 0 <= x < m and 0 <= y < n

    # DFS para escavar caminhos
    def dfs(x, y):
        grid[x][y].HB = False
        random.shuffle(direcoes)
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if dentro(nx, ny) and grid[nx][ny].HB:
                grid[x + dx // 2][y + dy // 2].HB = False
                dfs(nx, ny)

    dfs(0, 0)

    # entrada e saída livres
    grid[0][0].HB = False
    grid[m-1][n-1].HB = False

    # adiciona as bordas como objetos
    objs = []

    # parede de cima e baixo
    for x in range(-1, m+1):
        objs.append(obj(x, -1, True))  # topo
        objs.append(obj(x, n, True))   # fundo

    # parede lateral
    for y in range(n):
        objs.append(obj(-1, y, True))  # esquerda
        objs.append(obj(m, y, True))   # direita

    # adiciona o grid interno
    for x in range(m):
        for y in range(n):
            objs.append(grid[x][y])

    lab_map = {(o.CordX, o.CordY): o for o in objs}
    return objs,lab_map

import pygame

# cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE  = (0, 0, 200)
GRAY  = (100, 100, 100)
clock = pygame.time.Clock()
CELL_SIZE = 20  # tamanho de cada célula (em pixels)


def PrintLab(objs1, w1, objs2, w2, screen):
    def draw_lab(objs, w, offset_x):
        wx, wy = w.CordX, w.CordY
        max_x = max(o.CordX for o in objs)
        min_x = min(o.CordX for o in objs)
        max_y = max(o.CordY for o in objs)
        min_y = min(o.CordY for o in objs)

        mapa = {(o.CordX, o.CordY): o for o in objs}

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                rect = pygame.Rect(
                    offset_x + (x - min_x) * CELL_SIZE,
                    (y - min_y) * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                if (x, y) in mapa:
                    o = mapa[(x, y)]
                    if x == wx and y == wy:
                        pygame.draw.rect(screen, BLUE, rect)   # posição atual
                    elif (x, y) in w.PassedCords:
                        pygame.draw.rect(screen, GRAY, rect)   # caminho percorrido
                    elif x == 0 and y == 0:
                        pygame.draw.rect(screen, GREEN, rect)  # start
                    elif x == max_x - 1 and y == max_y - 1:
                        pygame.draw.rect(screen, RED, rect)    # end
                    elif o.HB:
                        pygame.draw.rect(screen, BLACK, rect)  # parede
                    else:
                        pygame.draw.rect(screen, WHITE, rect)  # espaço livre
                else:
                    pygame.draw.rect(screen, BLACK, rect)      # fora do grid = parede

    # --- Desenha os dois lado a lado ---
    draw_lab(objs1, w1, offset_x=0)
    largura1 = (max(o.CordX for o in objs1) + 1) * CELL_SIZE
    draw_lab(objs2, w2, offset_x=largura1 + 50)  # 50px de margem

    pygame.display.flip()
    clock.tick(120)




'''# exemplo de uso
if __name__ == "__main__":
    objs = gerar_labirinto_objs(21, 21)
    # print simples para conferir
    for o in objs:
        tipo = "Parede" if o.HB else "Caminho"
        print(f"({o.CordX}, {o.CordY}) -> {tipo}")
    print_labirinto_from_objs(objs)'''
def menu(screen):
    tamanho = 41
    font = pygame.font.SysFont(None, 80)
    largura_tela, altura_tela = screen.get_size()
    margem = 50  # espaço entre os labirintos

    while True:
        screen.fill((30, 30, 30))
        txt = font.render(f"Tamanho: {tamanho}x{tamanho}", True, WHITE)
        screen.blit(txt, (600, 300))

        # Botões lado a lado
        btn_minus = pygame.Rect(700, 400, 100, 100)
        btn_start = pygame.Rect(820, 400, 200, 100)
        btn_plus = pygame.Rect(1040, 400, 100, 100)

        pygame.draw.rect(screen, GREEN, btn_plus)
        pygame.draw.rect(screen, RED, btn_minus)
        pygame.draw.rect(screen, (0, 100, 200), btn_start)

        screen.blit(font.render("-", True, WHITE), (735, 435))
        screen.blit(font.render("Start", True, WHITE), (865, 435))
        screen.blit(font.render("+", True, WHITE), (1075, 435))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_plus.collidepoint(e.pos):
                    tamanho += 10
                if btn_minus.collidepoint(e.pos) and tamanho > 11:
                    tamanho -= 10
                if btn_start.collidepoint(e.pos):
                    # Ajusta o CELL_SIZE considerando dois labirintos lado a lado
                    global CELL_SIZE
                    CELL_SIZE = min((largura_tela - margem) // (2 * tamanho), altura_tela // tamanho, 20)
                    return tamanho
