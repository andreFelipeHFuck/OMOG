import numpy as np
import numpy.typing as npt
from scipy import optimize


def translate_matrix(point: npt.NDArray[np.float64]) -> npt.NDArray[npt.NDArray[np.float64]]:
    t_matrix = np.eye(4, dtype=np.float64)
            
    t_matrix[0][3] = point[0]
    t_matrix[1][3] = point[1]
    t_matrix[2][3] = point[2]
        
    return t_matrix

def rotate_matrix(theta: np.float64, point: npt.NDArray[np.float64] = np.array([0, 0, 0, 0], dtype=np.float64)) -> npt.NDArray[npt.NDArray[np.float64]]:
    r_matrix = np.eye(4, dtype=np.float64)
    
    r_matrix[0][0] = np.cos(theta)
    r_matrix[0][1] = - np.sin(theta)
    r_matrix[1][0] = np.sin(theta)
    r_matrix[1][1] = np.cos(theta)
    
    r_matrix[0][3] = point[0]
    r_matrix[1][3] = point[1]
    r_matrix[2][3] = point[2]
    
    return r_matrix

def angle_vectores(v1, v2, mod_v1, mod_v2) -> np.float64:
    dot_prod = np.dot(v1, v2)
    
    cos_theta = dot_prod / (mod_v1 * mod_v2)
    
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    
    angle_rad = np.arccos(cos_theta)
    
    return np.arccos(cos_theta)

def parametric_line(x0, y0, vector_PNx, vector_PNy):
    def f(t):
        return x0 + vector_PNx*t
    
    def g(t):
        return y0 + vector_PNy*t
    
    return f, g

def root_of_f_t(c: np.float64, x0: np.float64, y0: np.float64,  vector_PNx: np.array(np.float32), vector_PNy: np.array(np.float32)) -> np.array(np.array(np.float32)):
    def z(t):
        return c - np.sqrt(16 * vector_PNx * vector_PNx * t * t + 16 * vector_PNy * vector_PNy * t * t)
    
    f, g = parametric_line(x0, y0, vector_PNx, vector_PNy)
    
    t: np.float32 = optimize.fsolve(z, 0.5)
        
    return f(t), g(t)

def root_of_f_x_y(a: np.float64, b: np.float64, vector_PNx: np.array(np.float32), vector_PNy: np.array(np.float32)) -> np.array(np.array(np.float32)):
    
    x: np.float32 = (vector_PNx - b[0]) / a
    y: np.float32 = (vector_PNy - b[1]) / a
        
    return x, y

        
    
    
    
    