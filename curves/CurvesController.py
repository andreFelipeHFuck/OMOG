from enum import Enum

import numpy as np

import matplotlib.pyplot as plt

from .Curve import Curve
from .Nurbs4 import Nurbs4
from .Bezier4 import Bezier4

from .CurveController import CurveController

from .helper import parametric_line, root_of_f_t, root_of_f_x_y

class CurveEnum(Enum):
    C1 = 0
    C2 = 1
    ALL = 2

class CurvesController:
    def __init__(self):
        self._curves = []
        
    def get_knots(self):
        return self._curves[0].get_knots()
    
    def set_knots(self, knots):
        return self._curves[0].set_knots(knots)
        
    def get_control_point(self, i: int):
        return self._curves[i].get_all_control_point()
    
    def set_all_control_points(self, i:int, points):
        self._curves[i].set_all_control_point(points)
        
    def set_control_point(self, i: int, point):
        self._curves[i].set_control_point(point)
        
    def init_curve(self, curve: CurveController) -> int:
        self._curves.append(curve)
                
        return len(self._curves) - 1
        
    def C0(self) -> np.float64:
        for c_i in range(0, len(self._curves)):
            if c_i == 0:
                curve_0 = self._curves[0]
            else:
                curve_1 = self._curves[c_i]
                                
                delta = curve_0.get_PN() - curve_1.get_P0()
                                
                curve_1.translate(delta)
                
    def G1(self) -> np.float64:
        for c_i in range(0, len(self._curves)):
            if c_i == 0:
                curve_0 = self._curves[0]
            else:
                curve_1 = self._curves[c_i]
                
                PN, vector_PN, mod_PN = curve_0.get_first_derivate_PN()
                P0, vector_P0, mod_P0  = curve_1.get_first_derivate_P0()
                
                f, g = parametric_line(PN[0], PN[1], vector_PN[0][0],  vector_PN[0][1])
                                
                P1 = np.array([f(1.0), g(1.0), 0.0, 1.0])
                curve_1.set_control_point(1, P1)
                
                curve_1.get_first_derivate_P0()
                                
    def C1(self) -> np.float64:
        for c_i in range(0, len(self._curves)):
            if c_i == 0:
                curve_0 = self._curves[0]
            else:
                curve_1 = self._curves[c_i]
                
                PN, vector_PN, mod_PN = curve_0.get_first_derivate_PN()
                P0, _, _  = curve_1.get_first_derivate_P0()
                
                x, y = root_of_f_t(
                   x0=PN[0],
                   y0=PN[1],
                   c=mod_PN,
                   vector_PNx=vector_PN[0][0],
                   vector_PNy=vector_PN[0][1]
               )
                
                P1 = np.array([x[0], y[0], 0.0, 1.0])
                curve_1.set_control_point(1, P1)
                
                _, _, mod_P0 = curve_1.get_first_derivate_P0()
                
                return mod_PN - mod_P0
                
    def C2(self) -> np.float64:
        for c_i in range(0, len(self._curves)):
            if c_i == 0:
                  curve_0 = self._curves[0]
            else:
                curve_1 = self._curves[c_i]
                
                _ , vector_PN, curve_PN = curve_0.get_second_derivate_PN()
                P0, _, curve_P0  = curve_1.get_second_derivate_P0()
                
                P1 = curve_1.get_control_point(1)
                n = curve_1.get_n()
                                
                a = n * n - n
                b = (n * n) * (P0 - 2*P1) + n * (-P0 + 2*P1)
                    
                x, y = root_of_f_x_y(
                    a=a,
                    b=b,
                    vector_PNx=vector_PN[0][0],
                    vector_PNy=vector_PN[0][1]
                )
                
                P2 = np.array([x, y, 0.0, 1.0])
                
                curve_1.set_control_point(2, P2)
                
                P0, _, curve_P0  = curve_1.get_second_derivate_P0()
                
                return curve_PN - curve_P0
                
                
    def render_curves(self, step: float, type_curve: CurveEnum): 
        if type_curve.value - 1 == CurveEnum.C1.value:
            return [self._curves[CurveEnum.C1.value].calcule_points(step)]
        elif type_curve.value - 1 == CurveEnum.C2.value:
            return [self._curves[CurveEnum.C2.value].calcule_points(step)]
        elif type_curve.value - 1 == CurveEnum.ALL.value:
            return [c.calcule_points(step) for c in self._curves]
    
    def plot_curve(self, colors: list[str], step) -> None:
        fig, ax = plt.subplots()
        
        for curve, color in zip(self._curves, colors):
            x_list = []
            y_list = []
            
            points = [p for p in curve.get_all_control_point()]
        
            x_convex_hull = list(map(lambda x: x[0], points))
            y_convex_hull = list(map(lambda y: y[1], points))
            
            for i in curve.calcule_points(step):
                x_list.append(i[0][0])
                y_list.append(i[0][1])
                
            P0, vector_P0, _ = curve.get_first_derivate_P0()
            PN, vector_PN, _ = curve.get_first_derivate_PN()
            
            _, vector_d2_P0, _ = curve.get_second_derivate_P0()
            _, vector_d2_PN, _ = curve.get_second_derivate_PN()
            
            f, g = parametric_line(PN[0], PN[1], vector_PN[0][0],  vector_PN[0][1])  
            
            # plt.quiver([P0[0]], [P0[1]], [vector_P0[0][0]], [vector_P0[0][1]], color='g', angles='xy', scale_units='xy', scale=1)
            # plt.quiver([PN[0]], [PN[1]], [vector_PN[0][0]], [vector_PN[0][1]], color='k', angles='xy', scale_units='xy', scale=1)
            
            plt.quiver([P0[0]], [P0[1]], [vector_d2_P0[0][0]], [vector_d2_P0[0][1]], color='g', angles='xy', scale_units='xy', scale=1)
            plt.quiver([PN[0]], [PN[1]], [vector_d2_PN[0][0]], [vector_d2_PN[0][1]], color='k', angles='xy', scale_units='xy', scale=1)
            
            ax.plot(x_convex_hull, y_convex_hull, 'y-', lw=3, label='Convex Hull')
            # ax.plot(x_list, y_list, color, lw=3, label=curve.get_name()) 
            
            list_f = [f(t) for t in [0.0, 0.25, 0.5, 1.0]]
            list_g = [g(t) for t in [0.0, 0.25, 0.5, 1.0]]
            
        ax.grid(True)
        ax.legend(loc='best')
        plt.show()       

                    
if __name__ == "__main__":
    
    points_1 = np.array([
        np.array([-10, -4, 0, 3.2], dtype=np.float64),
        np.array([-9, 4, 0, 1], dtype=np.float64),
        np.array([-8, -4, 0, 1], dtype=np.float64),
        np.array([-7, 4, 0, 1], dtype=np.float64),
        np.array([-6, -4, 0.0, 1], dtype=np.float64),
        np.array([-5, 4, 0.0, 1], dtype=np.float64),
        np.array([-4, -4, 0.0, 0.1], dtype=np.float64),
    ])
    
    points_2 = np.array([
        np.array([1.147, 1.078, 0, 1], dtype=np.float64),
        np.array([2.0, -1.341, 0, 1], dtype=np.float64),
        np.array([4.739, 1.888, 0, 1], dtype=np.float64),
        np.array([6.962, -1.398, 0, 1], dtype=np.float64),
        np.array([8.327, 1.029, 0, 1], dtype=np.float64)
    ])
    
    curves: CurvesController = CurvesController()
    
    c1: Nurbs4 = Nurbs4(points_1)
    c2: Bezier4 = Bezier4(points_2)
    
    c1_controller: CurveController = CurveController(c1, "Nurbs")
    c2_controller: CurveController = CurveController(c2, "Bezier")
    
    curves.init_curve(c1_controller)
    curves.init_curve(c2_controller)
    
    step = 1_000
    
    # curves.plot_curve(['b-', 'r-'], step)
    
    curves.C0()
    
    curves.plot_curve(['b-', 'r-'], step)
    
    curves.C1()
    
    # curves.plot_curve(['b-', 'r-'], step)
    
    curves.C2()
    
    curves.plot_curve(['b-', 'r-'], step)

    
