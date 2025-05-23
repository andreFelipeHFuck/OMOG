import pygame 

from public.variables import *
from public.geometricObjects import draw_axes

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Curves")

clock = pygame.time.Clock()
       
while CARRY_ON:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           CARRY_ON = False      
    
    screen.fill(COLORS["background"])
    draw_axes(screen)
    
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()


