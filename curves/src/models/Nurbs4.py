import math

import numpy as np
import numpy.typing as npt


# from interfaces.Curve import Curve

class Nurbs4():
    def __init__(self, points: npt.NDArray[npt.NDArray[np.float64]]):
        self._k: int = 5
        self._n: int = len(points)
        
        self._points: npt.NDArray[npt.NDArray[np.float64]] = points
        
        # np.array([0, 0.111, 0.222, 0.333, 0.444, 0.556, 0.667, 0.778, 0.889, 1.0], dtype=np.float64)
        self._knots: npt.NDArray[np.float64]  = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float64)
        self._w : npt.NDArray[np.float64]  = np.array([[1.] for _ in range(0, len(points))], dtype=np.float64)
                        
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

    def get_control_point(self, i: int) -> npt.NDArray[np.float64]:
        return self._points[i]
    
    def deBoor(self, u: np.float64, i: int, k: int):
        return self.__deBoor(u, i, k)
    
    def __deBoor(self, u: np.float64, i: int, k: int) -> np.float64:
        if k == 0:
             return 1.0 if self._knots[i] <= u < self._knots[i+1] else 0.0

        if self._knots[i+k] == self._knots[i]:
            c1 = 0.0
        else:
            c1 = ((u - self._knots[i])/(self._knots[i+k] - self._knots[i])) * self.__deBoor(u, i, k-1)
         
        if self._knots[i+k+1] == self._knots[i+1]:
            c2 = 0.0
        else:
            c2 = ((self._knots[i+k+1] - u)/(self._knots[i+k+1] - self._knots[i+1])) * self.__deBoor(u, i+1, k-1)

        return c1 + c2
    
    def deBoor_matrix(self, u: np.float64, i: int) -> npt.NDArray[np.float64]:
        matrix = np.zeros((self._n, 1), dtype=np.float64)
        
        cont = 0
        
        for n_i in range(i - 1, i + self._k - 1):
            matrix[cont] = self.__deBoor(u, n_i, self._k - 1)   
            cont += 1 
        
        return matrix
        
    def calcule_points(self, i: int) -> npt.NDArray[npt.NDArray[np.float64]]:
        points = np.zeros((i + self._k - 1, 3))

        cont = 0
                
        for n_i in range(i - 1, i + self._k - 1):
            points[cont] = self._points[n_i]
            cont += 1     
            
        return points
    
    def calcule_curve_i(self, u: np.float64, i: int) -> npt.NDArray[npt.NDArray[np.float64]]:
        deBoor = self.deBoor_matrix(u, i)
        print(self._w * deBoor)
        return (self._w * self.calcule_points(i)).T @ deBoor 
    
    def calcule_curve(self, u: np.float64) -> npt.NDArray[np.float64]:
        return sum(
            self.calcule_curve_i(u, i)
            for i in range(1, self._n + 2 - self._k)
        )
    
    def translate_curve(self) -> None:
        pass
    
    def connect_curve_P0(self, PN) -> bool:
        pass 
    
    def connect_curve_PN(self, P0) -> bool:
        pass
    
    def first_derivative_P0(self):
        pass
    
    def first_derivate_PN(self):
        pass
    
    def tan_vec_first_derivate_P0(self) -> np.float64:
        pass 
    
    def tan_vec_first_derivate_PN(self) -> np.float64:
        pass 
    
    def second_derivate_P0(self):
        pass
    
    def second_derivate_PN(self):
        pass
    
    def tan_vec_second_derivate_P0(self) -> np.float64:
        pass 
    
    def tan_vec_second_derivate_PN(self) -> np.float64:
        pass 
    
    def rotate_PN_PN_1(self, angle: np.float64):
        pass
    


if __name__ == "__main__":
    points = np.array([
        np.array([-4, -4, 0], dtype=np.float64),
        np.array([-2, 4, 0], dtype=np.float64),
        np.array([2, -4, 0], dtype=np.float64),
        np.array([4, 4, 0], dtype=np.float64),
        np.array([-0.647, 1.8, 1.708], dtype=np.float64)
    ])
    
    nurbs: Nurbs4 = Nurbs4(points)
    t = 0.99999
    print(nurbs.deBoor_matrix(t, 1))
    print([nurbs.calcule_curve(i) for i in [t]])
    
