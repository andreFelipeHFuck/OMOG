import numpy as np
import numpy.typing as npt

from .Curve import Curve

class Bezier4(Curve):
    def __init__(self, points: npt.NDArray[npt.NDArray[np.float64]]):
        super().__init__()
        
        self._n = 5
        
        self._points: npt.NDArray[npt.NDArray[np.float64]] = points
        
        self._Mb = np.array([
            np.array([1, -4, 6, -4, 1], dtype=np.float64),
            np.array([-4, 12, -12, 4, 0], dtype=np.float64),
            np.array([6, -12, 6, 0, 0], dtype=np.float64),
            np.array([-4, 4, 0, 0, 0], dtype=np.float64),
            np.array([1, 0, 0, 0, 0], dtype=np.float64),
        ])
        
        self._P0 = points[0]
        self._PN = points[len(points) - 1]
        
        self._v_tan_P0: npt.NDArray[np.float64]
        self._mod_tan_P0: np.float64
        
        self._v_tan_PN: npt.NDArray[np.float64]
        self._mod_tan_PN: np.float64

        self._v_tan_d2_P0: npt.NDArray[np.float64]
        self._curv_P0: np.float64

        self._v_tan_d2_PN: npt.NDArray[np.float64]
        self._curv_PN: np.float64
        
    def get_n(self):
        return self._n
    
    def get_control_point(self, p_i):
        return self._points[p_i]
    
    def get_all_control_point(self):
        return self._points
         
    def get_control_point(self, i: int):
        return self._points[i]
    
    def set_control_point(self, p_i: int, point):
        self._points[p_i] = point
    
    def set_all_control_point(self, points):
        self._points = points
    
    def set_point_P0(self, P0) -> None:
        self._P0 = P0
        
    def set_point_PN(self, PN) -> None:
        self._PN = PN
        
    def get_point_P0(self) -> npt.NDArray[np.float64]:
        return self._P0
    
    def get_point_PN(self) -> npt.NDArray[np.float64]:
        return self._PN
    
    def calcule_T(self, t) -> npt.NDArray[np.float64]:
        return np.array([[t ** i for i in range(self._n -1, -1, -1)]], dtype=np.float64)
    
    def calcule_curve(self, t: np.float64, derivative: int = 0) -> npt.NDArray[np.float64]:     
        T = self.calcule_T(t)
      
        return T @ self._Mb @ self._points
            
    def first_derivative_P0(self):
        print(4, self._points[1], self._points[0], (self._n - 1) * (self._points[1] - self._points[0]))
        self._v_tan_P0 = np.array([(self._n - 1) * (self._points[1] - self._points[0])])
        self._mod_tan_P0 = np.linalg.norm(self._v_tan_P0)
    
    def first_derivative_PN(self):
        self._v_tan_PN = np.array([(self._n - 1)* (self._points[len(self._points) - 1] - self._points[len(self._points) - 2])])
        self._mod_tan_PN = np.linalg.norm(self._v_tan_PN)

    def tan_vec_first_derivate_P0(self) -> np.float64:
        return self._v_tan_P0
    
    def tan_vec_first_derivate_PN(self) -> np.float64:
        return self._v_tan_PN
    
    def mod_tan_first_derivate_P0(self) -> np.float64:
        return self._mod_tan_P0
    
    def mod_tan_first_derivate_PN(self) -> np.float64:
        return self._mod_tan_PN
    
    def second_derivative_P0(self):
        self._v_tan_d2_P0 = np.array([(self._n - 1) * (self._n - 2) * (self._points[0] - 2 * self._points[1] + self._points[2])])
        self._curv_P0 = np.linalg.norm(np.cross(self._v_tan_P0[0][0:3], self._v_tan_d2_P0[0][0:3])) / np.pow(self._mod_tan_P0, 3)
    
    def second_derivative_PN(self):
        self._v_tan_d2_P0 =  np.array([(self._n - 1) * (self._n - 2) * (self._points[len(self._points) - 1] - 2 * self._points[len(self._points) - 2] + self._points[len(self._points) - 3])])
        self._curv_PN = np.linalg.norm(np.cross(self._v_tan_PN[0][0:3], self._v_tan_d2_PN[0][0:3])) / np.pow(self._mod_tan_PN, 3)
    
    def tan_vec_second_derivate_P0(self) -> np.float64:
        return self._v_tan_d2_P0 
    
    def tan_vec_second_derivate_PN(self) -> np.float64:
        return self._v_tan_d2_PN
    
    def curvature_P0(self) -> np.float64:
        return self._curv_P0
    
    def curvature_PN(self) -> np.float64:
        return self._curv_PN
    
if __name__ == "__main__":
    points = np.array([
        np.array([-4, -4, 0, 1], dtype=np.float64),
        np.array([-2, 4, 0, 1], dtype=np.float64),
        np.array([2, -4, 0, 1], dtype=np.float64),
        np.array([4, 4, 0, 1], dtype=np.float64),
        np.array([3, 3, 0, 1], dtype=np.float64),
    ])
    
    bezier4: Bezier4 = Bezier4(points)
    t = 1.0   
    
    print(bezier4.calcule_curve(t, 0))
    bezier4.first_derivative_P0()
    print(bezier4.tan_vec_first_derivate_P0())
    
    