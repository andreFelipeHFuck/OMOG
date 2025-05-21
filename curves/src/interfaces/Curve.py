from abc import ABC, abstractmethod

import numpy as np

class Curve(ABC):
    @abstractmethod
    def get_control_point(self, i):
        pass
    
    @abstractmethod
    def calcule_curve(self, t):
        pass
    
    @abstractmethod
    def translate_curve(self) -> None:
        pass
    
    @abstractmethod
    def connect_curve_P0(self, PN) -> bool:
        pass 
    
    @abstractmethod
    def connect_curve_PN(self, P0) -> bool:
        pass
    
    @abstractmethod
    def first_derivative_P0(self):
        pass
    
    @abstractmethod
    def first_derivate_PN(self):
        pass
    
    @abstractmethod
    def tan_vec_first_derivate_P0(self) -> np.float64:
        pass 
    
    @abstractmethod
    def tan_vec_first_derivate_PN(self) -> np.float64:
        pass 
    
    @abstractmethod
    def second_derivate_P0(self):
        pass
    
    @abstractmethod
    def second_derivate_PN(self):
        pass
    
    @abstractmethod
    def tan_vec_second_derivate_P0(self) -> np.float64:
        pass 
    
    @abstractmethod
    def tan_vec_second_derivate_PN(self) -> np.float64:
        pass 
    
    @abstractmethod
    def rotate_PN_PN_1(self, angle: np.float64):
        pass