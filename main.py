import pygame 
import pygame_textinput

from public.variables import *
from public.geometricObjects import draw_axes, draw_menu
from public.events import click_mouse

from public.PointSprit import PointSprit
from public.CurveSprit import CurvesSprit

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Curves")

font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

user_text = ''
input_rect = pygame.Rect(200, 200, 140, 32)

menu: dict = {}

point = PointSprit(0.0, 0.0)
curver = CurvesSprit()

activate = False
       
while CARRY_ON:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           CARRY_ON = False   
           
        if event.type == pygame.KEYDOWN:
            if activate == True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
           
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                activate = True
            print(click_mouse(event))
            
            if event.button == 1:
                if point.collidepoint(event.pos):
                    print("O ponto foi clicado", point.get_active_point())
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                point.set_active_point(False)
            
        elif event.type == pygame.MOUSEMOTION:
            if point.get_active_point():
                print("O ponto foi ARRASTADO", point.get_active_point())
                point.move_ip(event.pos)
                
        elif event.type == RENDER_EVENT:
            curver.draw(screen)           
            
            
    screen.fill(COLORS["background"])
    draw_axes(screen)
    
    pygame.draw.rect(screen, COLORS["curve_1"], input_rect, 2)
    
    text_surface = font.render(user_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    
    input_rect.w = max(100, text_surface.get_width() + 10)
    
    # draw_menu(screen, font)
    
    point.draw(screen)
    
   
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()


