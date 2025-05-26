import numpy as np

from .CurveController import NurbsController
from .Curve import Curve

class CurvesController:
    def __init__(self):
        self._curves: list[Curve] = []
        
    def init_curve(self, curve: NurbsController):
        self._curves.append(curve)
         
    def init_bezier(self, points):
        self._bezier
        
    def render_curves(self, step: float):
        return [c.calcule_points(step) for c in self._curves]
        
if __name__ == "__main__":
    points = np.array([
        np.array([-2.147, -4.078, 0, 1], dtype=np.float64),
        np.array([-7.837, 5.341, 0, 1], dtype=np.float64),
        np.array([1.739, 1.888, 0, 1], dtype=np.float64),
        np.array([8.962, 5.398, 0, 1], dtype=np.float64),
        np.array([9.327, -2.029, 1.461, 1], dtype=np.float64)
    ])
    
    
    curves = CurvesController()
    
    nurbsController = NurbsController(points)
    curves.init_curve(nurbsController)
    
    for p in curves.render_curves(100):
        for c1 in p:
            print(c1)
