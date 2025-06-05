import pygame

from InputTextSprit import InputTextSprit

class PointUpdateFormSprit(pygame.sprite.Sprite):
    def __init__(self, 
                 x: int, 
                 y: int, 
                 button_w: int, 
                 button_h: int,
                 step: int,
                 w: int,
                 h: int,
                 font, 
                 event: int | None):
        
        super().__init__()
        
        self._buttons: list[InputTextSprit] = []
        
        step = 10
        for i in range(0, 4):
            self._buttons.append(
                InputTextSprit(
                    x=x,
                    y=y + step,
                    w=w,
                    h=h,
                    font=font,
                    event=event
                )
            )
        
        assert(4 * step + 4 * button_w <= w)
        
        self._rect = pygame.Rect(x, y, button_w, button_h)