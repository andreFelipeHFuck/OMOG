import pygame

import numpy as np
import numpy.typing as npt

from mathKernel.linearAlgebra import points_to_pixels, pixels_to_points
from .PointUpdateFormSprit import PointUpdateFormSprit

from .variables import *

class PointSprit(pygame.sprite.Sprite):
    def __init__(self, x, y, font):
        super().__init__()
        self._active_point = None
        
        self._x: np.float64 = x
        self._y: np.float64 = y
        self._z: np.float64 = 0.0
        self._w: np.float64 = 1.0
        
        self._rect = pygame.Rect((0, 0, 10, 10))
        
        self._form: PointUpdateFormSprit = PointUpdateFormSprit(  
            x=31,
            y=200,
            h=200,
            button_h=30,
            w=150,
            button_w=100,
            font=font
        )
        
    def get_x_y(self):
        return self._x, self._y
    
    def get_active_point(self) -> bool:
        return self._active_point
    
    def set_active_point(self, active: int | None):
        self._active_point = active
       
    def set_x(self, x: int):
        self._x = x
        
    def set_x(self, y: int):
        self._y = y
        
    def set_w(self, w: int):
        self._w = w
        
    def to_array(self) -> npt.NDArray[np.float64]:
        return np.array([self._x, self._y, self._z, self._w], dtype=np.float64)
    
    def draw_form(self, screen, pos_mouse, click):
        point_dict = {
            "x": str(self._x),
            "y": str(self._y),
            "z": str(self._z),
            "w": str(self._w)
        }
        
        self._form.draw(
            screen=screen,
            point_dict=point_dict,
            pos_mouse=pos_mouse,
            click=click
        )
        
    def draw(self, screen, color: CurveEnum, pos_mouse, click):
        if color == CurveEnum.C1:
            c = COLORS["point_1"]
        elif color == CurveEnum.C2:
            c = COLORS["point_2"]
               
        x, y = points_to_pixels(np.array([self._x, self._y], dtype=np.float64))
        self._rect.center = (x, y)
        
        pygame.draw.rect(screen, c, self._rect)
        
    def collidepoint_form(self, pos_mouse) -> bool:
        return self._form.collidepoint_rect(pos_mouse)
        
    def collidepoint(self, pos_mouse, num):
        res = self._rect.collidepoint(pos_mouse)
        
        if res:
            self._active_point = num
        return res
    
    def move_ip(self, pos):
        if pos[0] >= MENU_WIDTH  and pos[0] <= SCREEN_WIDTH and pos[1] >= 0 and pos[1] <= SCREEN_HEIGHT - MENU_HEIGHT:
            points = pixels_to_points(pos)
            self._x = points[0][0]
            self._y = points[0][1]
            
    def write(self, event, pos_mouse):
        key: str = self._form.collidepoint(
            pos_mouse=pos_mouse
        )
        
        print("KEY: ", key)
        
        self._form.write(
            event=event,
            key=key
        )
                
    def __str__(self):
        return f"[{self._x} {self._y} {self._z} {self._w} ]"
