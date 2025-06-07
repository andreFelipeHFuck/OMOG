import pygame 

from mathKernel.linearAlgebra import pixels_to_points

from public.variables import *
from public.geometricObjects import draw_axes
from public.events import click_mouse

from public.PointSprit import PointSprit
from public.CurveSprit import CurvesSprit
from public.MenuSprit import MenuSprit
from public.InputTextSprit import InputTextSprit

pygame.init()

font = pygame.font.Font(None, 32)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Curves")

def init_curves(render: bool = True, knots=[]) -> CurvesSprit:
    curves = CurvesSprit()

    curves.set_point(CurveEnum.C1, PointSprit(-10, 0, font), render)
    curves.set_point(CurveEnum.C1, PointSprit(-9, 4, font), render)
    curves.set_point(CurveEnum.C1, PointSprit(-8, 0, font), render)
    curves.set_point(CurveEnum.C1, PointSprit(-7, 4, font), render)
    curves.set_point(CurveEnum.C1, PointSprit(-6, 0, font), render)
    curves.set_point(CurveEnum.C1, PointSprit(-5, 4, font), render)
    curves.set_point(CurveEnum.C1, PointSprit(-4, 2, font), render)

    curves.set_knots(knots)

    curves.set_point(CurveEnum.C2, PointSprit(1.147, 1.078, font), render)
    curves.set_point(CurveEnum.C2, PointSprit(2.0, -1.341, font), render)
    curves.set_point(CurveEnum.C2, PointSprit(4.739, 1.888, font), render)
    curves.set_point(CurveEnum.C2, PointSprit(6.962, -1.398, font), render)
    curves.set_point(CurveEnum.C2, PointSprit(8.327, 1.029, font), render)
    
    return curves


# Variables

clock = pygame.time.Clock()

user_text = ''
input_rect = pygame.Rect(200, 200, 140, 32)

activate_point = (CurveEnum.NONE, 0)

form_curve_aux = activate_point[0]
form_num_aux = activate_point[1]

activate = False

curves = init_curves()
knots = curves.get_knots()

menu = MenuSprit(0, SCREEN_HEIGHT - MENU_HEIGHT, SCREEN_WIDTH, MENU_HEIGHT, font)

is_init: bool = True



# Camera Offset
offset_x = 0
offset_y = 0

point_x = InputTextSprit(
    x=SCREEN_WIDTH - 180,
    y=SCREEN_HEIGHT - 105,
    w=100,
    h=30,
    font=font,
    event=None
)

point_y = InputTextSprit(
    x=SCREEN_WIDTH - 100,
    y=SCREEN_HEIGHT - 105,
    w=100,
    h=30,
    font=font,
    event=None
)

speed: int = 5

cont = 0
       
while CARRY_ON:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           CARRY_ON = False   
           
        if event.type == pygame.KEYDOWN:
            menu.write(event)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            menu.collidepoint(event.pos)
            
            if ADD_POINT == ActivatePointEnum.LOCK:
                x, y = click_mouse(event)[0]
                curves.set_point(CurveEnum.C1, PointSprit(x, y, font), True)
                curves.check_status_curves()
                ADD_POINT = ActivatePointEnum.DISABLED
            
            elif event.button == 1:
                activate_point = curves.click_point(
                        pos_mouse=event.pos,
                        curve=form_curve_aux,
                        num=form_num_aux)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if activate_point[0] != CurveEnum.NONE:
                    activate_point = curves.unclick(activate_point[0], activate_point[1])
                                
        elif event.type == pygame.MOUSEMOTION:
            if activate_point[0] != CurveEnum.NONE:
                curves.move_ip(activate_point[0], activate_point[1], event.pos)
                curves.check_status_curves()
                                
            if POINT != None:
                POINT.move_ip(event.pos)
                                
        elif event.type == RENDER_EVENT:
            if C0_ACTIVE:
                curves.calcule_points(CurveEnum.ALL)  
            elif ADD_POINT == ActivatePointEnum.DISABLED:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                curves.calcule_points(CurveEnum.C1) 
                POINT = None
                ADD_POINT = ActivatePointEnum.ACTIVE
                print("RENDER_EVENT 2", ADD_POINT)
            else:
                if activate_point[0] != CurveEnum.NONE:
                    curves.calcule_points(activate_point[0])  
                    
        elif event.type == C0_EVENT:
            curves.C0(font)
            
        elif event.type == C1_EVENT:
            curves.C1(font)
            
        elif event.type == C2_EVENT:
            curves.C2(font)
            
        elif event.type == ADD_POINT_EVENT:
            POINT = PointSprit(0, 0, font)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            ADD_POINT = ActivatePointEnum.LOCK
            print("RENDER_EVENT 1", ADD_POINT)
            
        elif event.type == RESET_EVENT:
            curves = init_curves(
                render=False,
                knots=knots
            )
            is_init = True
            
        elif event.type == FORM_POINT_EVENT:
           print("FORM_POINT_EVENT")
           IS_FORM = ActivatePointEnum.ACTIVE
                   
    screen.fill(COLORS["background"])
    draw_axes(
        screen=screen,
        offset_x=offset_x,
        offset_y=offset_y
    )
    
    # print(ADD_POINT)
    if POINT != None:
        POINT.draw(
            screen=screen,
            color=CurveEnum.C1,
            pos_mouse=pygame.mouse.get_pos(),
            click=pygame.mouse.get_pressed()
        )
    
    if is_init:
        curves.check_status_curves()
        curves.calcule_points(CurveEnum.ALL)
        is_init = False
    
    curves.draw(
        screen=screen,
        pos_mouse=pygame.mouse.get_pos(),
        click=pygame.mouse.get_pressed()
    )  
    
    pos_pixels = pygame.mouse.get_pos()
    pos_mouse = pixels_to_points(pos_pixels)
    
    point_x.draw(
        screen=screen,
        text= f"( {pos_mouse[0][0]:.2f} " if pos_pixels[1]  <= SCREEN_HEIGHT - MENU_HEIGHT else "",
        color=COLORS["transparent"]
    )
    
    point_y.draw(
        screen=screen,
        text=f" {pos_mouse[0][1]:.2f} )" if pos_pixels[1]  <= SCREEN_HEIGHT - MENU_HEIGHT else "",
        color=COLORS["transparent"]
    )
    
    # print("Activate Point:", activate_point)
    if IS_FORM == ActivatePointEnum.ACTIVE:
        if activate_point[0] != CurveEnum.NONE:
            form_curve_aux = activate_point[0]
            form_num_aux = activate_point[1]
            
        curves.draw_form(
                screen=screen,
                curve=form_curve_aux,
                num=form_num_aux,
                pos_mouse=pygame.mouse.get_pos(),
                click=pygame.mouse.get_pressed()
            ) 
        
        IS_FORM = ActivatePointEnum.LOCK
        
    elif IS_FORM == ActivatePointEnum.LOCK:
        curves.draw_form(
                screen=screen,
                curve=form_curve_aux,
                num=form_num_aux,
                pos_mouse=pygame.mouse.get_pos(),
                click=pygame.mouse.get_pressed()
            ) 
    
    menu.draw(
        screen=screen,
        pos_mouse=pygame.mouse.get_pos(),
        click=pygame.mouse.get_pressed(),
        knots=curves.get_knots()
    )
      
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()


