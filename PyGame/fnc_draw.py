import pygame
import pygame.gfxdraw
import math

pygame.init()

def mapp(value, min, max, n_min, n_max):
    p_a = (value-min) * 100 / (max-min)
    perc = p_a / 100
    out = int(perc * (n_max-abs(n_min)))
    return out


width, height = 600, 400

#making display
scr = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fnc draw')               #giving header(like with html<title>)

#variable for storing color
color = pygame.Color(50, 50, 50)
#color = (100, 200, 50)

#zoom value
zoom = 80

run = True
while run:
    #for nice curve(so that you don't see dots)
    old_x = 0
    old_y = 0
    
    pygame.time.delay(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #start of the grid lines
    h_beg = int(height/2 % zoom)
    w_beg = int(width/2 % zoom)
    
    #drawing the grid
    #horizontal lines
    for y in range(0, height, zoom):
        pygame.gfxdraw.hline(scr, 0, width, y + h_beg, (30,30,30))
    else:
        pygame.gfxdraw.hline(scr, 0, width, int(height/2), (50,50,50))
    #vertical lines
    for x in range(0, width, zoom):
        pygame.gfxdraw.vline(scr, x + w_beg, 0, height, (30,30,30))
    else:
        pygame.gfxdraw.vline(scr, int(width/2), 0, height, (50,50,50))
    
    #area for drawing pixels
    h2 = int(height/2)
    w2 = int(width/2)
    for x in range(w2*-1, w2):
        
        x /= zoom
        
        y = (math.tan(x))% 0.5
        
#         if 0 != x:
#             y = 1/x
#         else:
#             y = None
#         
        if y != None:
            y = int(y*zoom*-1)
            x = int(x*zoom)
            if y+h2 > height or y+h2 < 0:
                continue
            
            pygame.gfxdraw.pixel(scr, x+w2, y+h2, (255,150,150))
            
            if old_x != 0 and old_y != 0:
                pygame.draw.line(scr, (255, 150, 150), (x+w2, y+h2), (old_x+w2, old_y+h2), 1)
            
            old_x, old_y = x, y
        else:
            old_x, old_y = 0, 0
    
    pygame.display.update()
    
    
    
