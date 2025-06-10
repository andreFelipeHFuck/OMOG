from random import random

import pygame

import numpy as np
import numpy.typing as npt

from curves.Nurbs4 import Nurbs4
from curves.Bezier4 import Bezier4

from curves.CurveController import CurveController
from curves.CurvesController import CurvesController

from .PointSprit import PointSprit

from .geometricObjects import draw_line
from .variables import *

def is_float(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False

class CurvesSprit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._curves = CurvesController()
        
        self._C1: bool = False
        self._C1_i = None
        self._points_C1: list[PointSprit] = []
        self._lines_C1 = [(0, 0, CurveEnum.C1)] * (STEP - 1)
        
        self._C2: bool = False
        self._C2_i = None
        self._points_C2: list[PointSprit] = []
        self._lines_C2 = [(0, 0, CurveEnum.C2)] * (STEP - 1)
        
    def get_knots(self):
        if self.create_C1() and self.create_C2():
            return self._curves.get_knots()
        
    def filter_kntos_text(self, knots: str) -> str:
        knots_list_text = knots.split(",")
        knots_list_text = knots_list_text[0:len(knots_list_text) - 2]
        
        new_knots_list = []
        
        knots = self.get_knots()
        
        valid_knots: bool = True
        text : str = ""
        
        if len(knots_list_text) == len(knots):        
            for i in knots_list_text:
                if is_float(i):
                    text += i
                    new_knots_list.append(float(i))
                else:
                    valid_knots = False
                    break
        else:
            valid_knots = False
            
        
        if not valid_knots:  
            text = ""
            for i in self.get_knots():
                text += f"{i:.2f}, "
        return text
        
    def set_knots(self, knots):
        if len(knots) != 0:
            self._curves.set_knots(knots)
     
    def set_point(self, curve: CurveEnum, point: PointSprit, render: bool = False) -> None:
        if curve == CurveEnum.C1:
            self._points_C1.append(point)
            
            if not render:
                self.check_status_curves()

        elif curve == CurveEnum.C2:
            self._points_C2.append(point)
            
            if not render:
                self.check_status_curves()
            
    def create_C1(self) -> bool:
        if len(self._points_C1) >= 5:
            points = np.array([p.to_array() for p in self._points_C1])
            if not self._C1:
                self._C1_i = self._curves.init_curve(
                    CurveController(
                        Nurbs4(points),
                        "Nurbs Degree 4"
                    )
                )
                self._C1 = True
            else:
                self._curves.set_all_control_points(self._C1_i, points)
            return True
        
        return False
        
    
    def create_C2(self):
        if len(self._points_C2) == 5:
            points = np.array([p.to_array() for p in self._points_C2])
            if not self._C2:
                self._C2_i = self._curves.init_curve(
                    CurveController(
                        Bezier4(points),
                        "Bezier Degree 4"
                    )
                )
                self._C2 = True   
            else:
                self._curves.set_all_control_points(self._C2_i, points)
            return True
        
        return False
            
    def check_status_curves(self) -> None:
        if self.create_C1() and self.create_C2():
            pygame.event.post(pygame.event.Event(RENDER_EVENT))  
            
    def click_point(self, pos_mouse, curve: CurveEnum = CurveEnum.NONE, num: int | None = 0) -> tuple[CurveEnum, int]:
        for num, p_1 in enumerate(self._points_C1):
            if p_1.collidepoint(pos_mouse, num):
                pygame.event.post(pygame.event.Event(FORM_POINT_EVENT))
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return (CurveEnum.C1, num)
            
        for num, p_2 in enumerate(self._points_C2):
            if p_2.collidepoint(pos_mouse, num):
                pygame.event.post(pygame.event.Event(FORM_POINT_EVENT))
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return (CurveEnum.C2, num)
        
        if curve != CurveEnum.NONE:
            return (curve, num)
            
        return (CurveEnum.NONE, 0)
            
    def unclick(self, curve: CurveEnum, num: int):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if curve == CurveEnum.C1:
            self._points_C1[num].set_active_point(None)
            self.check_status_curves()
        elif curve == CurveEnum.C2:
            self._points_C2[num].set_active_point(None)
            self.check_status_curves()

        return (CurveEnum.NONE, 0)
        
    def move_ip(self, curve: CurveEnum, num: int, pos) -> None:
        if curve == CurveEnum.C1:
            if self._points_C1[num].get_active_point() != None:
                self._points_C1[num].move_ip(pos)
        elif curve == CurveEnum.C2:
            if self._points_C2[num].get_active_point() != None:
                self._points_C2[num].move_ip(pos)
                
    def draw_form(self, screen, curve: CurveEnum, num: int, pos_mouse, click) -> None:
        if curve == CurveEnum.C1:
            point = self._points_C1[num]
            
            point.draw_form(
                screen=screen,
                pos_mouse=pos_mouse,
                click=click
            )
            
        elif curve == CurveEnum.C2:
            point = self._points_C2[num]
            
            point.draw_form(
                screen=screen,
                pos_mouse=pos_mouse,
                click=click
            )
            
    def collidepoint_form(self, curve: CurveEnum, num: int, pos_mouse) -> bool:
        if curve == CurveEnum.C1:
            point = self._points_C1[num]
            
            return point.collidepoint_form(pos_mouse)
            
        elif curve == CurveEnum.C2:
            point = self._points_C2[num]
            
            return point.collidepoint_form(pos_mouse)
        
        return False
        
    def write_form(self, curve: CurveEnum, num: int, pos_mouse, event) -> None:
        if curve == CurveEnum.C1:
            point = self._points_C1[num]
            
            point.write(
                event=event,
                pos_mouse=pos_mouse
            )
            
        elif curve == CurveEnum.C2:
            point = self._points_C2[num]
            
            point.write(
                event=event,
                pos_mouse=pos_mouse
            )
        
    def move_point(self, font):
        self._points_C1 = [PointSprit(float(p[0]), float(p[1]), font) for p in self._curves.get_control_point(self._C1_i)]
        self._points_C2 = [PointSprit(float(p[0]), float(p[1]), font) for p in self._curves.get_control_point(self._C2_i)]

        self.calcule_points(CurveEnum.ALL)
        
    def C0(self, font):    
        self._curves.C0()
            
        self.move_point(font)
        
    def C1(self, font) -> np.float64:
        self._curves.C0()
        diff = self._curves.C1()
        
        self.move_point(font)
                
        return diff
        
    def C2(self, font) -> np.float64:
        self._curves.C0()
        self._curves.C1()
        diff =self._curves.C2()
        
        self.move_point(font)
        
        return diff
                
    def calcule_points(self, type_curve: CurveEnum):                            
        cont_line: int = 0
        
        if type_curve != CurveEnum.NONE:
            for curve in self._curves.render_curves(STEP, type_curve):
                c_P0: bool = True
                        
                for num, c_i in enumerate(curve): 
                    if c_P0:
                        P0 = (c_i[0][0], c_i[0][1])
                        c_P0 = False
                    else:
                        P1 = (c_i[0][0], c_i[0][1])  
                        
                        if type_curve == CurveEnum.C1:
                            # self._lines_C1.append((P0, P1, True)) 
                            self._lines_C1[num - 1] = (P0, P1, CurveEnum.C1)
                        elif type_curve == CurveEnum.C2:
                            # self._lines_C2.append((P0, P1, False)) 
                            self._lines_C2[num - 1] = (P0, P1, CurveEnum.C2)
                        elif type_curve == CurveEnum.ALL:
                            if cont_line == 0:
                                # self._lines_C1.append((P0, P1, True)) 
                                self._lines_C1[num - 1] = (P0, P1, CurveEnum.C1)
                            elif cont_line >= 0:
                                # self._lines_C2.append((P0, P1, False)) 
                                self._lines_C2[num - 1] = (P0, P1, CurveEnum.C2)
                            
                        P0 = P1    
                  
                cont_line += 1  
                            
                                                          
    def draw_hux(self, screen, points, curve: CurveEnum, hux: CurveEnum,  pos_mouse, click):
        c_P0: bool = True
        
        for p in points:
             if c_P0:
                c_P0 = False
                P0 = p
             else:
                 P1 = p
                 x0, y0 = P0.get_x_y()
                 x1, y1 = P1.get_x_y()
                 
                 draw_line(
                     screen=screen,
                     point_P0=(x0, y0),
                     point_P1=(x1, y1),
                     color=hux,
                     thickness=1
                 )            
                 P0 = P1
                 
             p.draw(screen, curve,  pos_mouse, click) 
    
                        
    def draw_points(self, screen, curve: CurveEnum,  pos_mouse, click) -> None:
        if curve == CurveEnum.C1:
            self.draw_hux(
                screen=screen,
                points=self._points_C1,
                curve=CurveEnum.C1,
                hux=CurveEnum.HUX_C1,
                pos_mouse=pos_mouse,
                click=click
            )
        elif curve == CurveEnum.C2:
         self.draw_hux(
                screen=screen,
                points=self._points_C2,
                curve=CurveEnum.C2,
                hux=CurveEnum.HUX_C2,
                pos_mouse=pos_mouse,
                click=click 
            )  
        
    def draw(self, screen, pos_mouse, click):
        self.draw_points(screen, CurveEnum.C1, pos_mouse, click)
        self.draw_points(screen, CurveEnum.C2, pos_mouse, click)
        
        for l in self._lines_C1:
            draw_line(screen, l[0], l[1], l[2])
            
        for l in self._lines_C2:
            draw_line(screen, l[0], l[1], l[2])
        
        