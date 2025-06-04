import pygame

import numpy as np
import numpy.typing as npt

from .ButtonSprit import ButtonSprit
from .variables import *

class MenuSprit(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, w: int, h: int, font):
        super().__init__()
        
        self._buttons = [
            ButtonSprit(0, 0, 60, 30, "C0", font, C0_EVENT),
            ButtonSprit(0, 40, 60, 30, "C1", font, C1_EVENT),
            ButtonSprit(0, 80, 60, 30, "C2", font, C2_EVENT),
            ButtonSprit(0, 120, 120, 30, "Add Point", font, ADD_POINT_EVENT),
            ButtonSprit(0, 160, 120, 30, "Move", font, None)
        ]
        
        self._rect = pygame.Rect(x, y, w, h)
        

        
    def draw(self, screen, pos_mouse, click):
        pygame.draw.rect(screen, COLORS["gray"], self._rect)
        
        for num, button in enumerate(self._buttons):
            button.draw(
                screen=screen,
                pos_mouse=pos_mouse,
                num=num,
                click=click
            )