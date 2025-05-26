import random

import numpy as np
import numpy.typing as npt

from Curve import Curve

class Nurbs4(Curve):
    def __init__(self, points: npt.NDArray[npt.NDArray[np.float64]]):
        super().__init__()
        
        self._k: int = 5
        self._n: int = len(points)
        
        self._points: npt.NDArray[npt.NDArray[np.float64]] = points
        
        self._knots: npt.NDArray[np.float64] = self.generate_knots()
                
        self._w : npt.NDArray[np.float64]  = np.array([[self._points[i][3]] for i in range(0, len(points))], dtype=np.float64)
                        
        self._P0 = points[0]
        self._PN = points[len(points) - 1]
        
        self._v_tan_P0: npt.NDArray[np.float64]
        self._mod_tan_P0: np.float64
        
        self.v_tan_PN: npt.NDArray[np.float64]
        self._mod_tan_PN: np.float64

        self.v_curv_P0: npt.NDArray[np.float64]
        self._mod_curv_P0: np.float64

        self.v_curv_PN: npt.NDArray[np.float64]
        self._mod_curv_PN: np.float64
        
    def generate_knots(self) -> npt.NDArray[np.float64]:
        num_knots = self._n  + (self._k - 1) + 1
        knots = np.zeros(num_knots)
        
        num = num_knots - 2 * self._k
        
        for i in range(1, self._k + 1):
            knots[len(knots) - i] = 1.0
            
        rand_num = sorted([random.uniform(0, 1) for _ in range(0, num)])
                        
        cont: int = 0
        
        for i in range(self._k, self._k + num):
            knots[i] = rand_num[cont]
            cont += 1
            
        return knots
            
    def get_n(self):
        return self._n
    
    def set_point_P0(self, P0) -> None:
        self._P0 = P0
        
    def set_point_PN(self, PN) -> None:
        self._PN = PN
        
    def get_point_P0(self) -> npt.NDArray[np.float64]:
        return self._P0
    
    def get_point_PN(self) -> npt.NDArray[np.float64]:
        return self._PN

    def get_control_point(self, i: int) -> npt.NDArray[np.float64]:
        return self._points[i]
    
    def deBoor(self, t: np.float64, i: int, k: int):
        return self.__deBoor(t, i, k)
    
    def __deBoor(self, t: np.float64, i: int, k: int) -> np.float64:
        if k == 0:
             return 1.0 if self._knots[i] <= t < self._knots[i+1] else 0.0

        if self._knots[i+k] == self._knots[i]:
            c1 = 0.0
        else:
            c1 = ((t - self._knots[i])/(self._knots[i+k] - self._knots[i])) * self.__deBoor(t, i, k-1)
         
        if self._knots[i+k+1] == self._knots[i+1]:
            c2 = 0.0
        else:
            c2 = ((self._knots[i+k+1] - t)/(self._knots[i+k+1] - self._knots[i+1])) * self.__deBoor(t, i+1, k-1)

        return c1 + c2
    
    def deBoor_matrix(self, t: np.float64, derivative: int = 0) -> npt.NDArray[np.float64]:
        n = self._n - derivative
        matrix = np.zeros((n, 1), dtype=np.float64)
        
        cont = 0
        
        for n_i in range(0, n):
            matrix[cont] = self.__deBoor(t, n_i, self._k - 1)   
            cont += 1 
        
        return matrix
    
    def calcule_Q_i(self, i: int, p1: npt.NDArray[np.float64], p2: npt.NDArray[np.float64], derivative: int) ->  npt.NDArray[np.float64]:
        k = self._k - 1 - derivative
            
        if self._knots[i+k+1] == self._knots[i+1]:
            return np.zeros(4)
        
        return (k / (self._knots[i+k+1] - self._knots[i+1])) * (p2 - p1)
        
    
    def calcule_points(self, derivative: int = 0) -> npt.NDArray[np.float64]:
        if derivative > 0:
            return np.array([self.calcule_Q_i(i, self._points[i], self._points[i - 1], derivative) for i in range(1, self._n)])
            
        return self._points
    
    def calcule_curve(self, t: np.float64, derivative: int = 0) -> npt.NDArray[np.float64]: 
        if t == 0.0:
            return np.array([self._points[0]])
        elif t == 1.0:
            return np.array([self._points[len(self._points) - 1]])
        else:
            n = self._n - derivative
              
            deBoor_matrix = self.deBoor_matrix(t, derivative) 
            points = self.calcule_points(derivative)
        
            w = self._w[0:n]
            sum_d_w = sum(w[i][0] * deBoor_matrix[i] for i in range(0, n))
               
            return ((w * deBoor_matrix).T @ points) / sum_d_w
    
    
    
    def first_derivative_P0(self):
        self._v_tan_P0 = self.calcule_curve(0.0, 1)
        self._mod_tan_P0 = np.linalg.norm(self._v_tan_P0)
    
    def first_derivate_PN(self):
        self._v_tan_PN = self.calcule_curve(1.0, 1)
        self._mod_tan_P0 = np.linalg.norm(self._v_tan_PN)
        
    def tan_vec_first_derivate_P0(self) -> np.float64:
        return self._v_tan_P0
    
    def tan_vec_first_derivate_PN(self) -> np.float64:
        return self._v_tan_PN
    
    def second_derivate_P0(self):
        pass
    
    def second_derivate_PN(self):
        pass
    
    def k_curvature_derivate_P0(self) -> np.float64:
        pass 
    
    def k_curvature_derivate_PN(self) -> np.float64:
        pass 
    
if __name__ == "__main__":
    points = np.array([
        np.array([-4, -4, 0, 1], dtype=np.float64),
        np.array([-2, 4, 0, 1], dtype=np.float64),
        np.array([2, -4, 0, 1], dtype=np.float64),
        np.array([4, 4, 0, 1], dtype=np.float64),
        np.array([-2.707, 4.071, 0.0, 1], dtype=np.float64),
        np.array([-3.687, 3.97, 0.0, 1.0], dtype=np.float64),
        np.array([4.283, 1.285, 0.0, 1.0], dtype=np.float64)
    ])
    
    nurbs: Nurbs4 = Nurbs4(points)
    t = 0.999
    print(nurbs.calcule_curve(t))
    
    print(nurbs.calcule_curve(1.0))
    
    
    
