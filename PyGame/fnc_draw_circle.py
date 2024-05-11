import pygame
import pygame.gfxdraw
import math

pygame.init()

def mapp(value, min, max, n_min, n_max):
    p_a = (value-min) * 100 / (max-min)
    perc = p_a / 100
    out = int(perc * (n_max-abs(n_min)))
    return out


width, height = 1000, 1000

scr = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fnc draw')

color = pygame.Color(50, 50, 50)
#color = (100, 200, 50)
zoom = 50

old_x_1, old_x_2 = 0, 0
old_y_1, old_y_2 = 0, 0
        

run = True
while run:
    pygame.time.delay(50)
    
    scr.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    
    beg = int(height/2 % zoom)
    
    for y in range(0, height, zoom):
        pygame.gfxdraw.hline(scr, 0, width, y + beg, (30,30,30))
    else:
        pygame.gfxdraw.hline(scr, 0, width, int(height/2), (60,60,60))
        
    for x in range(0, height, zoom):
        pygame.gfxdraw.vline(scr, x + beg, 0, height, (30,30,30))
    else:
        pygame.gfxdraw.vline(scr, int(width/2), 0, height, (60,60,60))
    
    circle_r = 1
    w = 5
    z = 5
    a = 0
    b = 0
#     ((x+a)^2)/w + ((y+b)^2)/z = circle_r
    
    minx =-(math.sqrt(circle_r*w**2)+a)*zoom
    maxx = (math.sqrt(circle_r*w**2)-a)*zoom
    
    w2 = int(width/2)
    for x in range(w2*-1, w2):
        if x <= minx or x >= maxx:
            continue
        
        x /= zoom

        y = -(x+a)**2/w**2 + circle_r
        
        try:
            y = math.sqrt((y)*z**2)
        except:
            pass
        
        
        y = int(y*zoom*-1)
        x = int(x*zoom)
        if y+w2 > height or y+w2 < 0:
            continue
        
        
        x_1 = x+w2
        y_1 = y+w2+int(b*zoom)
        x_2 = x_1
        y_2 = -y+w2+int(b*zoom)
        
        if not old_x_1 and not old_x_2 and not old_y_1 and not old_y_2:
            old_x_1, old_x_2 = x_1, x_2
            old_y_1, old_y_2 = y_1, y_2
        elif x in [minx+1]:
            old_x_1, old_x_2 = x_1, x_2
            old_y_1, old_y_2 = y_1, y_2
        
        if x in [minx+1, maxx-1]:
            pygame.draw.line(scr, (255,150,150), (x_1, y_1), (x_2, y_2), 1)
            
        
        pygame.gfxdraw.pixel(scr, x_1, y_1, (255,150,150))
        pygame.draw.line(scr, (255,150,150), (old_x_1, old_y_1), (x_1, y_1), 1)
        
        pygame.gfxdraw.pixel(scr, x_2, y_2, (255,150,150))
        pygame.draw.line(scr, (255,150,150), (old_x_2, old_y_2), (x_2, y_2), 1)
        
        
        
        old_x_1, old_x_2 = x_1, x_2
        old_y_1, old_y_2 = y_1, y_2
        
    
    
    
    
    pygame.display.update()
    
    
    
