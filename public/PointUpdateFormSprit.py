import pygame

from .InputTextSprit import InputTextSprit
from .variables import *

class PointUpdateFormSprit(pygame.sprite.Sprite):
    def __init__(self, 
                 x: int, 
                 y: int, 
                 button_w: int, 
                 button_h: int,
                 w: int,
                 h: int,
                 font, 
                 event: int | None = None):
        
        super().__init__()
        
        self._dict_inputs = {}
        self._font = font
        
        step = 0
        
        for k in ["x", "y", "z", "w"]:
            self._dict_inputs[k] = InputTextSprit(
                    x=x + 40,
                    y=y + 30 + step,
                    w=button_w,
                    h=button_h,
                    font=font,
                    event=event,
                    bord=2
            )
            
            step += 40
                    
        self._rect = pygame.Rect(x, y, w, h)
            
    def collidepoint(self, mouse_pos) -> str:
        for key, i in self._dict_inputs.items():
            if i.collidepoint(mouse_pos):
                return key
            
    def write(self, event, key: str) -> None:
        self._dict_inputs[key].write(event)
        
    def draw(self, screen, point_dict, pos_mouse, click) -> None:
        pygame.draw.rect(screen, COLORS["gray"], self._rect)
        
        for key, i in self._dict_inputs.items():
            label_input = self._font.render(f"{key}: ", True, COLORS["white"])
            screen.blit(label_input, (i.get_x() - 30, i.get_y()))
            
            text: str = f"{float(point_dict[key]):.2f}"
            
            i.draw(screen=screen, text=text)
            
        
    
            
    
