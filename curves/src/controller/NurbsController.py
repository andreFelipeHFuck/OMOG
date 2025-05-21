import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt

from Nurbs4 import Nurbs4 

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
        
if __name__ == "__main__":
    points = np.array([
        np.array([-4, -4, 0, 1], dtype=np.float64),
        np.array([-2, 4, 0, 1], dtype=np.float64),
        np.array([2, -4, 0, 1], dtype=np.float64),
        np.array([4, 4, 0, 1], dtype=np.float64),
        np.array([-3.435, 1.068, 1.461, 1], dtype=np.float64)
    ])
    
    x_convex_hull = list(map(lambda x: x[0], points))
    y_convex_hull = list(map(lambda y: y[1], points))
        
    
    nurbs_controller = NurbsController(points=points)
    
    x_list = []
    y_list = []
    
    for i in nurbs_controller.calcule_points(100):
        x_list.append(i[0][0])
        y_list.append(i[0][1])
    
            
    fig, ax = plt.subplots()
    ax.plot(x_convex_hull, y_convex_hull, 'b-', lw=3, label='Convex Hull')
    ax.plot(x_list, y_list, 'r-', lw=3, label='NURBS')
    ax.grid(True)
    ax.legend(loc='best')
    plt.show()
        
    
        
    
    