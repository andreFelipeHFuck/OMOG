import pygame

import numpy as np
import numpy.typing as npt

class InputTextSprit(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, w: int, h: int):
        super().__init__()
        self._active_input = None
        
        self._text: str = ""
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
        pass
        
        
        
        
        
    