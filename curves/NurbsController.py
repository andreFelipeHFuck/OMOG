import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt

from .Nurbs4 import Nurbs4

class NurbsController:
    def __init__(self, points: npt.NDArray[npt.NDArray[np.float64]]):
         self._nurbs = Nurbs4(points=points)
         
    def calcule_points(self, step: float) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        for u_i in np.linspace(0.0, 0.999, step):
            if u_i == 0.0:
                aux = self._nurbs.calcule_curve(u_i)
                self._nurbs.set_point_P0(aux)
                yield aux
            elif u_i == 0.999:
                aux = self._nurbs.calcule_curve(u_i)
                self._nurbs.set_point_PN(aux)
                yield aux
            else:
                yield self._nurbs.calcule_curve(u_i)
                
    def translate(self, point: npt.NDArray[np.float64]) -> None:
        self._nurbs.translate_curve(point)
        
    def get_first_derivate(self) -> npt.NDArray[np.float64]:
        return self._nurbs.get_point_P0(), self._nurbs.get_point_P0() @ self._nurbs.translate_matrix(self._nurbs.get_point_P0()[0])
    
    def plot_curve(self) -> None:
        points = [self._nurbs.get_control_point(i) for i in range(0, 5)]
        
        x_convex_hull = list(map(lambda x: x[0], points))
        y_convex_hull = list(map(lambda y: y[1], points))
        
        x_list = []
        y_list = []
        
        for i in self.calcule_points(100):
            x_list.append(i[0][0])
            y_list.append(i[0][1])
    
        self._nurbs.first_derivative_P0()
        vector_P0 = self._nurbs.tan_vec_first_derivate_P0()
                
        P0 = self._nurbs.get_point_P0()
        
        fig, ax = plt.subplots()
        ax.plot(x_convex_hull, y_convex_hull, 'b-', lw=3, label='Convex Hull')
        ax.plot(x_list, y_list, 'r-', lw=3, label='NURBS')        
                
        # plt.quiver(*origin, [1], [1], color=['g'], scale=2)
        plt.quiver([P0[0][0]], [P0[0][1]], [vector_P0[0][0]], [vector_P0[0][1]], color='b', units='xy', scale=1)
        
        ax.grid(True)
        ax.legend(loc='best')
        plt.show()
    
    
if __name__ == "__main__":
    points = np.array([
        np.array([-2.147, -4.078, 0, 1], dtype=np.float64),
        np.array([-7.837, 5.341, 0, 1], dtype=np.float64),
        np.array([1.739, 1.888, 0, 1], dtype=np.float64),
        np.array([8.962, 5.398, 0, 1], dtype=np.float64),
        np.array([9.327, -2.029, 1.461, 1], dtype=np.float64)
    ])
    
    nurbs_controller: NurbsController = NurbsController(points)
    nurbs_controller.plot_curve()
    
    
        
    
        
    
    