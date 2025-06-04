import pygame 

from public.variables import *
from mathKernel.linearAlgebra import pixels_to_points


def click_mouse(event) -> tuple[int, int]:
    mouse_position = event.pos
    
    if mouse_position[0] > MENU_WIDTH:
        return pixels_to_points(mouse_position)
    
    return None

def write_point(event, curves):
    pass

def chang_point(event, curves):
    pass

def update_point(event, curves):
    pass