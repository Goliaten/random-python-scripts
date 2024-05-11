import pygame
import pygame.gfxdraw

pygame.init()

def mapp(value, min, max, n_min, n_max):
    p_a = (value-min) * 100 / (max-min)
    perc = p_a / 100
    out = int(perc * (n_max-abs(n_min)))
    return out


width, height = 64, 64

scr = pygame.display.set_mode((width, height))
pygame.display.set_caption('Set')

color = pygame.Color(50, 50, 50)
#color = (100, 200, 50)
z_opt = 0
z = 0

run = True
while run:
    pygame.time.delay(100)
    
    if z == 256 - 4:
        z_opt = 1
    elif z == 0:
        z_opt = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('window closed')
            run = False
    
    for x in range(width):
        for  y in range(height):
            pygame.gfxdraw.pixel(scr, x, y, (mapp(x, 0, width, 0, 255), mapp(y, 0, height, 0, 255), z))
            #pygame.draw.circle(scr, (x, y, y), (x, y), 1, 1)   #(screen, color, coords, radius, width)
    
    if z_opt == 0:
        z += 4
    elif z_opt == 1:
        z -= 4
    
    pygame.display.update()
    