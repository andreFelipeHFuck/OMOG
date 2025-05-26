import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt

from Curve import Curve

from Nurbs4 import Nurbs4
from Bezier4 import Bezier4

class CurveController:
    def __init__(self, curve: Curve, name: str):
         self._curve = curve
         self._name: str = name
    
    def get_P0(self) -> npt.NDArray[np.float64]:
        return self._curve.get_point_P0()
    
    def get_PN(self) -> npt.NDArray[np.float64]:
        return self._curve.get_point_PN()
    
    def get_name(self) -> str:
        return self._name
         
    def calcule_points(self, step: float) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        for u_i in np.linspace(0.0, 1.0, step):
            if u_i == 0.0:
                aux = self._curve.calcule_curve(u_i)
                self._curve.set_point_P0(aux)
                yield aux
            elif u_i == 1.0:
                aux = self._curve.calcule_curve(u_i)
                self._curve.set_point_PN(aux)
                yield aux
            else:
                yield self._curve.calcule_curve(u_i)
                
    def translate(self, point: npt.NDArray[np.float64]) -> None:
        self._curve.translate_curve(point)
        
    def get_first_derivate(self) -> npt.NDArray[np.float64]:
        return self._curve.get_point_P0(), self._curve.get_point_P0() @ self._curve.translate_matrix(self._curve.get_point_P0()[0])
    
    def plot_curve(self) -> None:
        points = [self._curve.get_control_point(i) for i in range(0, self._curve.get_n())]
        
        x_convex_hull = list(map(lambda x: x[0], points))
        y_convex_hull = list(map(lambda y: y[1], points))
        
        x_list = []
        y_list = []
        
        for i in self.calcule_points(100):
            x_list.append(i[0][0])
            y_list.append(i[0][1])
    
        self._curve.first_derivative_P0()
        vector_P0 = self._curve.tan_vec_first_derivate_P0()
        
        self._curve.first_derivate_PN()
        vector_PN = self._curve.tan_vec_first_derivate_PN()
                
        P0 = self._curve.get_point_P0()
        PN = self._curve.get_point_PN()
              
        fig, ax = plt.subplots()
        ax.plot(x_convex_hull, y_convex_hull, 'b-', lw=3, label='Convex Hull')
        ax.plot(x_list, y_list, 'r-', lw=3, label=self._name)        
                
        # plt.quiver(*origin, [1], [1], color=['g'], scale=2)
        plt.quiver([P0[0][0]], [P0[0][1]], [vector_P0[0][0]], [vector_P0[0][1]], color='g', units='xy', scale=0.5)
        plt.quiver([PN[0][0]], [PN[0][1]], [vector_PN[0][0]], [vector_PN[0][1]], color='g', units='xy', scale=0.5)
        
        ax.grid(True)
        ax.legend(loc='best')
        plt.show()
    
    
if __name__ == "__main__":
    points = np.array([
        np.array([-4, -4, 0, 1], dtype=np.float64),
        np.array([-2, 4, 0, 1], dtype=np.float64),
        np.array([2, -4, 0, 1], dtype=np.float64),
        np.array([4, 4, 0, 1], dtype=np.float64),
        np.array([-3.271, -0.827, 0.0, 1], dtype=np.float64),
        np.array([3.663, 2.207, 0.0, 1.0], dtype=np.float64),
        np.array([4.283, 1.285, 0.0, 1.0], dtype=np.float64)
    ])
    
    c1: Nurbs4 = Nurbs4(points)
    c2: Bezier4 = Bezier4(points)
    
    c1_controller: CurveController = CurveController(c1, "Bezier")
    
    c1_controller.plot_curve()
    
    
        
    
        
    
    