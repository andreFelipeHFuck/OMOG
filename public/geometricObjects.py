"""
Desenha primitivas geometricas na tela
"""

import pygame

from public.variables import *
from mathKernel.linearAlgebra import points_to_pixels


def draw_axes(screen, offset_x, offset_y, auxiliary: bool = True)->None:
    
    x_origin = X_ORIGIN - offset_x
    y_origin = Y_ORIGIN - offset_y
    
    # Axes X
    pygame.draw.line(screen, COLORS["black"], (0, y_origin), (SCREEN_WIDTH, y_origin), 2)
    
    # Axes Y
    pygame.draw.line(screen, COLORS["black"], (x_origin, 0), (x_origin, SCREEN_HEIGHT), 2)
    
    # Auxiliary Line
    if auxiliary: 
        for x in range(-1_000, 1_000, SCALE):
            screen_x = X_ORIGIN + x
            pygame.draw.line(screen, COLORS["gray"], (screen_x, 0), (screen_x, SCREEN_HEIGHT))
            
        for y in range(-1_000, 1_000, SCALE):
            screen_y = Y_ORIGIN + y
            pygame.draw.line(screen, COLORS["gray"], (0, screen_y), (SCREEN_WIDTH, screen_y))
            
        
    
def draw_line(screen, point_P0, point_P1, color: CurveEnum, thickness: int = 2) -> None:
    if color == CurveEnum.C1:
        c = COLORS["curve_1"]
    elif color == CurveEnum.C2:
        c = COLORS["curve_2"]
    elif color == CurveEnum.HUX_C1:
        c = COLORS["hux_curve_1"]
    elif color == CurveEnum.HUX_C2:
        c = COLORS["hux_curve_2"]
         
    pygame.draw.aaline(screen, c, points_to_pixels(point_P0), points_to_pixels(point_P1), thickness)
            
