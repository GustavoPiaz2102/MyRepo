from classOBJ import *
from time import sleep
import sys
from os import system
sys.setrecursionlimit(100000)  # Limite de recursão pra poder usar labs maiores

#Cara isso tem q melhorar muito kkk
"""
def WalkDeepSearch(w,lab_map,m,n):
    if((w.CordX, w.CordY) != (m-1, n-1)):
        x, y = w.CordX, w.CordY
        #print(f"Posição atual: ({x}, {y})")

        if w.sentido == 0:  # Norte
            if (x-1, y) in lab_map and not lab_map[(x-1, y)].HB and (x-1, y) not in w.PassedCords:
                w.Move(x-1, y)
                w.sentido = 3  # Oeste
            elif (x, y+1) in lab_map and not lab_map[(x, y+1)].HB and (x, y+1) not in w.PassedCords:
                w.Move(x, y+1)
                w.sentido = 0
            elif (x+1, y) in lab_map and not lab_map[(x+1, y)].HB and (x+1, y) not in w.PassedCords:
                w.Move(x+1, y)
                w.sentido = 1
            elif (x, y-1) in lab_map and not lab_map[(x, y-1)].HB and (x, y-1) not in w.PassedCords:
                w.Move(x, y-1)
                w.sentido = 2
            else:
                #Volta sempre pela esquerda novamente
                if (x-1, y) in lab_map and not lab_map[(x-1, y)].HB and (x-1, y) :
                    w.Move(x-1, y)
                    w.sentido = 3
                elif (x, y+1) in lab_map and not lab_map[(x, y+1)].HB and (x, y+1) :
                    w.Move(x, y+1)
                    w.sentido = 0
                elif (x+1, y) in lab_map and not lab_map[(x+1, y)].HB and (x+1, y):
                    w.Move(x+1, y)
                    w.sentido = 1
                elif (x, y-1) in lab_map and not lab_map[(x, y-1)].HB and (x, y-1):
                    w.Move(x, y-1)
                    w.sentido = 2
        elif w.sentido == 1:  # Leste
            if (x, y+1) in lab_map and not lab_map[(x, y+1)].HB and (x, y+1) not in w.PassedCords:
                w.Move(x, y+1)
                w.sentido = 0
            elif (x+1, y) in lab_map and not lab_map[(x+1, y)].HB and (x+1, y) not in w.PassedCords:
                w.Move(x+1, y)
                w.sentido = 1
            elif (x, y-1) in lab_map and not lab_map[(x, y-1)].HB and (x, y-1) not in w.PassedCords:
                w.Move(x, y-1)
                w.sentido = 2
            elif (x-1, y) in lab_map and not lab_map[(x-1, y)].HB and (x-1, y) not in w.PassedCords:
                w.Move(x-1, y)
                w.sentido = 3
            else:
                # Volta sempre pela esquerda
                if (x, y+1) in lab_map and not lab_map[(x, y+1)].HB and (x, y+1):
                    w.Move(x, y+1)
                    w.sentido = 0
                elif (x+1, y) in lab_map and not lab_map[(x+1, y)].HB and (x+1, y):
                    w.Move(x+1, y)
                    w.sentido = 1
                elif (x, y-1) in lab_map and not lab_map[(x, y-1)].HB and (x, y-1):
                    w.Move(x, y-1)
                    w.sentido = 2
                elif (x-1, y) in lab_map and not lab_map[(x-1, y)].HB and (x-1, y):
                    w.Move(x-1, y)
                    w.sentido = 3
        elif w.sentido == 2:  # Sul
            if (x+1, y) in lab_map and not lab_map[(x+1, y)].HB and (x+1, y) not in w.PassedCords:
                w.Move(x+1, y)
                w.sentido = 1
            elif (x, y-1) in lab_map and not lab_map[(x, y-1)].HB and (x, y-1) not in w.PassedCords:
                w.Move(x, y-1)
                w.sentido = 2
            elif (x-1, y) in lab_map and not lab_map[(x-1, y)].HB and (x-1, y) not in w.PassedCords:
                w.Move(x-1, y)
                w.sentido = 3
            elif (x, y+1) in lab_map and not lab_map[(x, y+1)].HB and (x, y+1) not in w.PassedCords:
                w.Move(x, y+1)
                w.sentido = 0
            else:
                # mesma coisa
                if (x+1, y) in lab_map and not lab_map[(x+1, y)].HB and (x+1, y):
                    w.Move(x+1, y)
                    w.sentido = 1
                elif (x, y-1) in lab_map and not lab_map[(x, y-1)].HB and (x, y-1):
                    w.Move(x, y-1)
                    w.sentido = 2
                elif (x-1, y) in lab_map and not lab_map[(x-1, y)].HB and (x-1, y):
                    w.Move(x-1, y)
                    w.sentido = 3
                elif (x, y+1) in lab_map and not lab_map[(x, y+1)].HB and (x, y+1):
                    w.Move(x, y+1)
                    w.sentido = 0
        elif w.sentido == 3:  # Oeste
          if (x, y-1) in lab_map and not lab_map[(x, y-1)].HB and (x, y-1) not in w.PassedCords:
                w.Move(x, y-1)
                w.sentido = 2
          elif (x-1, y) in lab_map and not lab_map[(x-1, y)].HB and (x-1, y) not in w.PassedCords:
                w.Move(x-1, y)
                w.sentido = 3
          elif (x, y+1) in lab_map and not lab_map[(x, y+1)].HB and (x, y+1) not in w.PassedCords:
                w.Move(x, y+1)
                w.sentido = 0
          elif (x+1, y) in lab_map and not lab_map[(x+1, y)].HB and (x+1, y) not in w.PassedCords:
                w.Move(x+1, y)
                w.sentido = 1
          else:
            # EU podia ter feito uma função pra isso
            if (x, y-1) in lab_map and not lab_map[(x, y-1)].HB and (x, y-1):
                w.Move(x, y-1)
                w.sentido = 2
            elif (x-1, y) in lab_map and not lab_map[(x-1, y)].HB and (x-1, y):
                w.Move(x-1, y)
                w.sentido = 3
            elif (x, y+1) in lab_map and not lab_map[(x, y+1)].HB and (x, y+1):
                w.Move(x, y+1)
                w.sentido = 0
            elif (x+1, y) in lab_map and not lab_map[(x+1, y)].HB and (x+1, y):
                w.Move(x+1, y)
                w.sentido = 1
        w.AddCord(w.CordX, w.CordY)
        return
    else:
        return 0

"""
def WalkDeepSearch(w, lab_map, m, n):
    if (w.CordX, w.CordY) == (m-1, n-1):
        return 0

    x, y = w.CordX, w.CordY
    moves = [(-1,0), (0,1), (1,0), (0,-1)]  # N, L, S, O

    # 1) tenta virar à esquerda primeiro e só andar em celulas não visitadas
    for i in range(4):
        dx, dy = moves[(w.sentido + 3 + i) % 4]
        nx, ny = x + dx, y + dy
        if (nx, ny) in lab_map and not lab_map[(nx, ny)].HB and (nx, ny) not in w.PassedCords:
            w.Move(nx, ny)
            w.sentido = (w.sentido + 3 + i) % 4
            w.AddCord(nx, ny)
            return

    # 2) se não tiver novos caminhos, anda em celulas já visitadas
    for i in range(4):
        dx, dy = moves[(w.sentido + 3 + i) % 4]
        nx, ny = x + dx, y + dy
        if (nx, ny) in lab_map and not lab_map[(nx, ny)].HB:
            w.Move(nx, ny)
            w.sentido = (w.sentido + 3 + i) % 4
            w.AddCord(nx, ny)
            return

def VerificarCaminho(x,y,ToVisit,lab_map2,w):
    c = 0
    if (x-1,y) in lab_map2 and not lab_map2[(x-1,y)].HB and (x-1,y) not in w.PassedCords and (x-1,y) not in ToVisit:
        ToVisit.append((x-1,y))
        c+=1
    if (x,y+1) in lab_map2 and not lab_map2[(x,y+1)].HB and (x,y+1) not in w.PassedCords and (x,y+1) not in ToVisit:
        ToVisit.append((x,y+1))
        c+=1
    if (x+1,y) in lab_map2 and not lab_map2[(x+1,y)].HB and (x+1,y) not in w.PassedCords and (x+1,y) not in ToVisit:
        ToVisit.append((x+1,y))
        c+=1
    if (x,y-1) in lab_map2 and not lab_map2[(x,y-1)].HB and (x,y-1) not in w.PassedCords and (x,y-1) not in ToVisit:
        ToVisit.append((x,y-1))
        c+=1
    return c
def WalkBreadthSearch(w2,lab_map2,ToVisit,m,n):
    if ((w2.CordX,w2.CordY) != (m-1,n-1)):
        #print(f"Posição atual: ({w2.CordX}, {w2.CordY})")
        x,y = w2.CordX,w2.CordY
        VerificarCaminho(x,y,ToVisit,lab_map2,w2)
        if len(ToVisit) > 0:
            next_x,next_y = ToVisit.pop(0)
            w2.Move(next_x,next_y)
            w2.AddCord(next_x,next_y)
        else:
            #print("Não há mais caminhos disponíveis. O labirinto não tem solução.")
            return
        return
    else:
        return 0

        
def main():
    screen = pygame.display.set_mode((1920, 1080))
    while True:

        pygame.init()
        tamanho = menu(screen)
        tm = 0.0000000001
        m  = n = tamanho
        x = 0
        y = 0
        w = walker(x, y, True)
        w2 = walker(x, y, True)
        w.Move(0,0)
        w.AddCord(0,0)
        w2.Move(0,0)
        w2.AddCord(0,0)
        ToVisit = []
        objs,lab_map = GenLab(m,n)
        objs2 = objs.copy()
        lab_map2 = lab_map.copy()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            a = WalkDeepSearch(w,lab_map,m,n)
            b = WalkBreadthSearch(w2,lab_map2,ToVisit,m,n)
            if( a == 0 and b == 0):
                sleep(1)
                running = False                
            screen.fill(WHITE)
            PrintLab(objs, w, objs2, w2, screen,a,b)
            pygame.display.flip()
            #sleep(tm)
    
main()
pygame.quit()
