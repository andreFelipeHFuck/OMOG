import numpy as np
import numpy.typing as npt

from .Curve import Curve

class Nurbs4(Curve):
    def __init__(self, points: npt.NDArray[npt.NDArray[np.float64]]):
        self._k: int = 5
        self._n: int = len(points)
        
        self._points: npt.NDArray[npt.NDArray[np.float64]] = points
        
        # np.array([0, 0.111, 0.222, 0.333, 0.444, 0.556, 0.667, 0.778, 0.889, 1.0], dtype=np.float64)
        self._knots: npt.NDArray[np.float64]  = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0], dtype=np.float64)
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
    
    def deBoor_matrix(self, u: np.float64, derivative: int = 0) -> npt.NDArray[np.float64]:
        n = self._n - derivative
        matrix = np.zeros((n, 1), dtype=np.float64)
        
        cont = 0
        
        for n_i in range(0, n):
            matrix[cont] = self.__deBoor(u, n_i, self._k - 1)   
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
    
    def calcule_curve(self, u: np.float64, derivative: int = 0) -> npt.NDArray[np.float64]: 
        n = self._n - derivative
              
        deBoor_matrix = self.deBoor_matrix(u, derivative) 
        points = self.calcule_points(derivative)
        
        w = self._w[0:n]
        sum_d_w = sum(w[i][0] * deBoor_matrix[i] for i in range(0, n))
               
        return ((deBoor_matrix * w).T @ points) / sum_d_w
    
    def translate_matrix(self, point: npt.NDArray[np.float64]) ->  npt.NDArray[npt.NDArray[np.float64]]:
        t_matrix = np.eye(4, dtype=np.float64)
        
        t_matrix[0][3] = point[0]
        t_matrix[1][3] = point[1]
        t_matrix[2][3] = point[2]
        
        return t_matrix
    
    def translate_curve(self, point: npt.NDArray[np.float64]) -> None:
       t_matrix = self.translate_matrix(point)
                
       for i in range(0, len(self._points)):
            self._points[i] = t_matrix @ self._points[i]
                        
    def connect_curve_P0(self, PN) -> bool:
        pass 
    
    def connect_curve_PN(self, P0) -> bool:
        pass
    
    def first_derivative_P0(self):
        self._v_tan_P0 = self.calcule_curve(0.0, 1)
    
    def first_derivate_PN(self):
        self._v_tan_PN = self.calcule_curve(1.0, 1)
    
    def tan_vec_first_derivate_P0(self) -> np.float64:
        return self._v_tan_P0
    
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
        np.array([-4, -4, 0, 1], dtype=np.float64),
        np.array([-2, 4, 0, 1], dtype=np.float64),
        np.array([2, -4, 0, 1], dtype=np.float64),
        np.array([4, 4, 0, 1], dtype=np.float64),
        np.array([-2.707, 4.071, 0.274, 1], dtype=np.float64),
        # np.array([-3.687, 3.97, 3.315], dtype=np.float64)
    ])
    
    nurbs: Nurbs4 = Nurbs4(points)
    t = 0.0
    print(nurbs.calcule_curve(t))
    print(nurbs.calcule_curve(t, 1))
    
    
    
