import pygame

import numpy as np
import numpy.typing as npt

from .ButtonSprit import ButtonSprit
from .InputTextSprit import InputTextSprit
from .variables import *

class MenuSprit(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, w: int, h: int, font):
        super().__init__()
        
        h_button = SCREEN_HEIGHT - 50
        
        self._buttons = [
            ButtonSprit(20, h_button, 60, 30, "C0", font, C0_EVENT),
            ButtonSprit(90, h_button, 60, 30, "C1", font, C1_EVENT),
            ButtonSprit(160, h_button, 60, 30, "C2", font, C2_EVENT),
            ButtonSprit(230, h_button, 120, 30, "Add Point", font, ADD_POINT_EVENT),
            ButtonSprit(360, h_button, 120, 30, "Reset", font, RESET_EVENT)
        ]
        
        
        self._input_text = InputTextSprit(
            x=570,
            y=h_button,
            w=1_500,
            h=30,
            font=font,
            event=None,
            bord=3        
        )
        
        self._font = font
        
        self._rect = pygame.Rect(x, y, w, h)
        
    
    def collidepoint(self, mouse_pos) -> bool:
        return self._input_text.collidepoint(mouse_pos)
    
    def write(self, event) -> None:
        self._input_text.write(event)

    def draw(self, screen, pos_mouse, click, knots):
        pygame.draw.rect(screen, COLORS["gray"], self._rect)
        
        for num, button in enumerate(self._buttons):
            button.draw(
                screen=screen,
                pos_mouse=pos_mouse,
                num=num,
                click=click
            )
            
        label_input = self._font.render("K-nots:", True, COLORS["white"])
        screen.blit(label_input, (490, SCREEN_HEIGHT - 45))
        
        text: str = ""
        for i in knots:
            text += f"{i:.2f}, "
            
        self._input_text.draw(screen=screen, text=text)
