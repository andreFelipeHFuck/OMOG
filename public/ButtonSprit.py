import pygame

import numpy as np
import numpy.typing as npt

from .variables import *


class ButtonSprit(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, w: int, h: int, text: str, font, event: int | None):
        super().__init__()
        self._active_button = None
        
        self._text: str = text
        self._font = font
        self._event = event
        
        self._rect = pygame.Rect(x, y, w, h)
        
    def get_active_button(self) -> bool:
        return self._active_button
    
    def set_active_button(self, active: int | None):
        self._active_button = active
        
    def draw(self, screen, pos_mouse, num, click):   
        if self.collidepoint(pos_mouse):
            pygame.draw.rect(screen, COLORS["active"], self._rect)
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
            if click[0] == 1:
                pygame.event.post(pygame.event.Event(self._event))
        else:
            pygame.draw.rect(screen, COLORS["disabled"], self._rect)
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
         
            
        text_surface = self._font.render(self._text, True, COLORS["black"])
        text_rect = text_surface.get_rect(center=self._rect.center)
        screen.blit(text_surface, text_rect)
                
    
    def collidepoint(self, pos_mouse):
        return self._rect.collidepoint(pos_mouse)    
    
    def __str__(self):
        return f"[{self._x} {self._y} {self._z} {self._w}], text: {self._text}"