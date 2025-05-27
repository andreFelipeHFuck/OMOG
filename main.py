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

activate_point = None
activate = False

curves = CurvesSprit()

curves.set_point(CurveEnum.C1, PointSprit(-2.147, -4.078))
curves.set_point(CurveEnum.C1, PointSprit(-7.837, 5.341))
curves.set_point(CurveEnum.C1, PointSprit(1.739, 1.888))
curves.set_point(CurveEnum.C1, PointSprit(8.962, 5.398))
curves.set_point(CurveEnum.C1, PointSprit(9.327, -2.029))

curves.calcule_points()   
curves.check_status_curves()
       
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
                activate_point = curves.click_point(event.pos)
                # if point.collidepoint(event.pos, 1):
                #     print("O ponto foi clicado", point.get_active_point())
                
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                activate_point = curves.unclick(activate_point[0], activate_point[1])
                
            
        elif event.type == pygame.MOUSEMOTION:
            if activate_point != None:
                curves.move_ip(activate_point[0], activate_point[1], event.pos)
                
        elif event.type == RENDER_EVENT:
            curves.calcule_points()         
            
            
    screen.fill(COLORS["background"])
    draw_axes(screen)
    
    pygame.draw.rect(screen, COLORS["curve_1"], input_rect, 2)
    
    text_surface = font.render(user_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    
    input_rect.w = max(100, text_surface.get_width() + 10)
    
    # draw_menu(screen, font)
    
    curves.draw(screen)  
   
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()


