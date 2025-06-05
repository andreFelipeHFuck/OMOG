import pygame 

from public.variables import *
from public.geometricObjects import draw_axes
from public.events import click_mouse

from public.PointSprit import PointSprit
from public.CurveSprit import CurvesSprit
from public.MenuSprit import MenuSprit
from public.InputTextSprit import InputTextSprit

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Curves")


# Variables
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

user_text = ''
input_rect = pygame.Rect(200, 200, 140, 32)

activate_point = None
activate = False

menu = MenuSprit(0, SCREEN_HEIGHT - MENU_HEIGHT, SCREEN_WIDTH, MENU_HEIGHT, font)

point = None
input = InputTextSprit(400, 400, 40, 80, font, None)

curves = CurvesSprit()

curves.set_point(CurveEnum.C1, PointSprit(-10, 0), True)
curves.set_point(CurveEnum.C1, PointSprit(-9, 4), True)
curves.set_point(CurveEnum.C1, PointSprit(-8, 0), True)
curves.set_point(CurveEnum.C1, PointSprit(-7, 4), True)
curves.set_point(CurveEnum.C1, PointSprit(-6, 0), True)
curves.set_point(CurveEnum.C1, PointSprit(-5, 4), True)
curves.set_point(CurveEnum.C1, PointSprit(-4, 2), True)


curves.set_point(CurveEnum.C2, PointSprit(1.147, 1.078), True)
curves.set_point(CurveEnum.C2, PointSprit(2.0, -1.341), True)
curves.set_point(CurveEnum.C2, PointSprit(4.739, 1.888), True)
curves.set_point(CurveEnum.C2, PointSprit(6.962, -1.398), True)
curves.set_point(CurveEnum.C2, PointSprit(8.327, 1.029), True)

is_init: bool = True

# Camera Offset
offset_x = 0
offset_y = 0

speed: int = 5
       
while CARRY_ON:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           CARRY_ON = False   
           
        if event.type == pygame.KEYDOWN:
            input.write(event)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            input.collidepoint(event.pos)
            if ADD_POINT:
                x, y = click_mouse(event)[0]
                curves.set_point(CurveEnum.C1, PointSprit(x, y), True)
                curves.check_status_curves()
            
            if event.button == 1:
                activate_point = curves.click_point(event.pos)
                
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                activate_point = curves.unclick(activate_point[0], activate_point[1])
               
                                
        elif event.type == pygame.MOUSEMOTION:
            if activate_point != None:
                curves.move_ip(activate_point[0], activate_point[1], event.pos)
                curves.check_status_curves()
                
            if point != None:
                point.move_ip(event.pos)
                
        elif event.type == RENDER_EVENT:
            if ADD_POINT:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                curves.calcule_points(CurveEnum.C1) 
                point = None
                ADD_POINT = False

            elif C0_ACTIVE:
                curves.calcule_points(CurveEnum.ALL)  
            else:
                if activate_point != None:
                    curves.calcule_points(activate_point[0])  
                    
        elif event.type == C0_EVENT:
            curves.C0()
            
        elif event.type == C1_EVENT:
            curves.C1()
            
        elif event.type == C2_EVENT:
            curves.C2()
            
        elif event.type == ADD_POINT_EVENT:
            point = PointSprit(0, 0)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            ADD_POINT = True
                   
    screen.fill(COLORS["background"])
    draw_axes(
        screen=screen,
        offset_x=offset_x,
        offset_y=offset_y
    )
    
    # pygame.draw.rect(screen, COLORS["curve_1"], input_rect, 2)
    
    # text_surface = font.render(user_text, True, (0, 0, 0))
    # screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    
    # input_rect.w = max(100, text_surface.get_width() + 10)
    
    
    if point != None:
        point.draw(
            screen=screen,
            color=CurveEnum.C1
        )
    
    if is_init:
        curves.check_status_curves()
        curves.calcule_points(CurveEnum.ALL)
        is_init = False
    
    curves.draw(screen)  
    
    menu.draw(
        screen=screen,
        pos_mouse=pygame.mouse.get_pos(),
        click=pygame.mouse.get_pressed()
    )
   
    # input.draw(screen)
   
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()


