import numpy as np

import matplotlib.pyplot as plt


from .Curve import Curve
from .Nurbs4 import Nurbs4
from .Bezier4 import Bezier4

from .CurveController import CurveController

class CurvesController:
    def __init__(self):
        self._curves = []
        
    def init_curve(self, curve: CurveController):
        self._curves.append(curve)
        
    def C0(self) -> None:
        for c_i in range(0, len(self._curves)):
            if c_i == 0:
                curve_0 = self._curves[0]
            else:
                curve_1 = self._curves[c_i]
                
                delta = curve_0.get_PN() - curve_1.get_P0()
                
                print(delta)
                
                curve_1.translate(delta)
            
        
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
    
    curves.plot_curve(['b-', 'r-'], 100)
    

    
