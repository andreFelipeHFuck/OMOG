import numpy as np

import matplotlib.pyplot as plt


from Curve import Curve
from Nurbs4 import Nurbs4
from Bezier4 import Bezier4

from CurveController import CurveController

from helper import angle_vectores

class CurvesController:
    def __init__(self):
        self._curves = []
        
    def get_control_point(self, i: int):
        return self._curves[i].get_all_control_point()
        
    def set_control_point(self, i: int, points):
        self._curves[i].set_control_point(points)
        
    def init_curve(self, curve: CurveController) -> int:
        self._curves.append(curve)
                
        return len(self._curves) - 1
        
    def C0(self) -> None:
        for c_i in range(0, len(self._curves)):
            if c_i == 0:
                curve_0 = self._curves[0]
            else:
                curve_1 = self._curves[c_i]
                
                delta = curve_0.get_PN() - curve_1.get_P0()
                                
                curve_1.translate(delta)
                
    def G1(self) -> None:
        for c_i in range(0, len(self._curves)):
            if c_i == 0:
                curve_0 = self._curves[0]
            else:
                curve_1 = self._curves[c_i]
                
                V_0 = curve_1.get_first_derivate_P0()
                V_1 = curve_1.get_first_derivate_PN()
                
                theta = angle_vectores(V_0[1][0], V_1[1][0], V_0[2], V_1[2])
                print(theta)
                
                curve_1.rotate(1, theta)
                
                V_0 = curve_1.get_first_derivate_P0()
                V_1 = curve_1.get_first_derivate_PN()
                
                theta = angle_vectores(V_0[1][0], V_1[1][0], V_0[2], V_1[2])
                print(theta)
                
        
    def render_curves(self, step: float):
        return [c.calcule_points(step) for c in self._curves]
    
    def plot_curve(self, colors: list[str], step) -> None:
        fig, ax = plt.subplots()
        
        for curve, color in zip(self._curves, colors):
            x_list = []
            y_list = []
            
            for i in curve.calcule_points(step):
                x_list.append(i[0][0])
                y_list.append(i[0][1])
                
            P0, vector_P0, _ = curve.get_first_derivate_P0()
            PN, vector_PN, _ = curve.get_first_derivate_PN()
                        
            plt.quiver([P0[0]], [P0[1]], [vector_P0[0][0]], [vector_P0[0][1]], color='g', units='xy', scale=0.5)
            plt.quiver([PN[0]], [PN[1]], [vector_PN[0][0]], [vector_PN[0][1]], color='k', units='xy', scale=0.5)
            
            ax.plot(x_list, y_list, color, lw=3, label=curve.get_name()) 


    
        ax.grid(True)
        ax.legend(loc='best')
        plt.show()       

                    
if __name__ == "__main__":
    
    points_1 = np.array([
        np.array([-4, -4, 0, 1], dtype=np.float64),
        np.array([-2, 4, 0, 1], dtype=np.float64),
        np.array([2, -4, 0, 1], dtype=np.float64),
        np.array([4, 4, 0, 1], dtype=np.float64),
        np.array([-3.271, -0.827, 0.0, 1], dtype=np.float64),
        np.array([3.663, 2.207, 0.0, 1.0], dtype=np.float64),
        np.array([4.283, 1.285, 0.0, 1.0], dtype=np.float64)
    ])
    
    points_2 = np.array([
        np.array([-2.147, -4.078, 0, 1], dtype=np.float64),
        np.array([-7.837, 5.341, 0, 1], dtype=np.float64),
        np.array([1.739, 1.888, 0, 1], dtype=np.float64),
        np.array([8.962, 5.398, 0, 1], dtype=np.float64),
        np.array([9.327, -2.029, 1.461, 1], dtype=np.float64)
    ])
    
    curves: CurvesController = CurvesController()
    
    c1: Nurbs4 = Nurbs4(points_1)
    c2: Bezier4 = Bezier4(points_2)
    
    c1_controller: CurveController = CurveController(c1, "Nurbs")
    c2_controller: CurveController = CurveController(c2, "Bezier")
    
    curves.init_curve(c1_controller)
    curves.init_curve(c2_controller)
    
    curves.C0()
    
    curves.G1()
    
    curves.plot_curve(['b-', 'r-'], 100)
    

    
