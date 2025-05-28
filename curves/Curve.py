from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt

from helper import translate_matrix, rotate_matrix

class Curve(ABC):
    @abstractmethod
    def get_n(self):
        pass
    
    @abstractmethod
    def get_all_control_point(self):
        pass
    
    @abstractmethod
    def get_control_point(self, points):
        pass
    
    @abstractmethod
    def set_control_point(self, points):
        pass
    
    @abstractmethod
    def calcule_curve(self, t):
        pass
    
    def translate_curve(self, point: npt.NDArray[np.float64]) -> None:
       t_matrix = translate_matrix(point)
                
       for i in range(0, len(self._points)):
            self._points[i] = t_matrix @ self._points[i]
            
    def rotate_point(self, p_i: int, theta: np.float64) -> None:
        r_matrix = rotate_matrix(theta)
        
        self._points[p_i] = r_matrix @ self._points[p_i]
    
    @abstractmethod
    def first_derivative_P0(self):
        pass
    
    @abstractmethod
    def first_derivative_PN(self):
        pass
    
    @abstractmethod
    def tan_vec_first_derivate_P0(self) -> np.float64:
        pass 
    
    @abstractmethod
    def mod_tan_first_derivate_P0(self) -> np.float64:
        pass
    
    @abstractmethod
    def tan_vec_first_derivate_PN(self) -> np.float64:
        pass 
    
    @abstractmethod
    def mod_tan_first_derivate_PN(self) -> np.float64:
        pass
    
    @abstractmethod
    def second_derivate_P0(self):
        pass
    
    @abstractmethod
    def second_derivate_PN(self):
        pass
    
    @abstractmethod
    def k_curvature_derivate_P0(self) -> np.float64:
        pass 
    
    @abstractmethod
    def k_curvature_derivate_PN(self) -> np.float64:
        pass 
    
