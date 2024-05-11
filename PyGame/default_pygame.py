import pygame
import pygame.gfxdraw

pygame.init()

def mapp(value, min, max, n_min, n_max):
    p_a = (value-min) * 100 / (max-min)
    perc = p_a / 100
    out = int(perc * (n_max-abs(n_min)))
    return out


width, height = 400, 400

scr = pygame.display.set_mode((width, height))
pygame.display.set_caption('Set')

color = pygame.Color(50, 50, 50)
#color = (100, 200, 50)

run = True
while run:
    pygame.time.delay(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for x in range(width):
        for  y in range(height):
            pygame.gfxdraw.pixel(scr, x, y, (mapp(x, 0, width, 0, 255), mapp(y, 0, height, 0, 255), z))
            #pygame.draw.circle(scr, (x, y, y), (x, y), 1, 1)   #(screen, color, coords, radius, width)
    
    pygame.display.update()
    
    
    

