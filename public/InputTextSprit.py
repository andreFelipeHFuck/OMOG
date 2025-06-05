import re

import pygame

from public.variables import *

import numpy as np
import numpy.typing as npt

regex = r"[,]?[+-]?\d+\.?\d*"

class InputTextSprit(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, w: int, h: int, font, event: int | None):
        super().__init__()
        self._active_input = None
        
        self._text: str = ""
        self._font = font
        self._event = event
        
        self._active_input: bool = False
        
        
        self._rect = pygame.Rect(x, y, w, h)
        
    def get_active_input(self) -> int | None:
        return self._active_input
    
    def set_active_input(self, active: int | None) -> None:
        self._active_input = active
        
    def get_text(self) -> str:
        return self._text
    
    def set_text(self, text: str) -> str:
        return self._text
    
    def write_letter(self, letter: str) -> None:
        self._text += letter
    
    def backspace(self) -> None:
        self._text = self._text[:-1]
        
    def render(self, font) -> None:
        font.render(self._text, True, (0, 0, 0))
        
    def collidepoint(self, mouse_pos) -> bool:
        res = self._rect.collidepoint(mouse_pos)
        
        if res:
            self._active_input = True
            
        return res
    
    def draw(self, screen):
        pygame.draw.rect(screen, COLORS["white"], self._rect)
        
        text_surface = self._font.render(self._text, True, COLORS["black"])
        text_rect = text_surface.get_rect(center=self._rect.center)
        self._rect.w = max(100,  text_surface.get_width() + 10)
        screen.blit(text_surface, text_rect)
        

    def write(self, event):
        if self._active_input:
            if event.key == pygame.K_BACKSPACE:
                self._text = self._text[:-1]
            else:
                self._text += event.unicode if re.search(regex, self._text + event.unicode) else ""
            
            
        
        
        
        
        
    