import numpy as np
import numpy.typing as npt

def translate_matrix(point: npt.NDArray[np.float64]) -> npt.NDArray[npt.NDArray[np.float64]]:
    t_matrix = np.eye(4, dtype=np.float64)
            
    t_matrix[0][3] = point[0]
    t_matrix[1][3] = point[1]
    t_matrix[2][3] = point[2]
        
    return t_matrix

def rotate_matrix(theta: np.float64) -> npt.NDArray[npt.NDArray[np.float64]]:
    r_matrix = np.eye(4, dtype=np.float64)
    
    r_matrix[0][0] = np.cos(theta)
    r_matrix[0][1] = - np.sin(theta)
    r_matrix[1][0] = np.sin(theta)
    r_matrix[1][1] = np.cos(theta)
    
    return r_matrix

def angle_vectores(v1, v2, mod_v1, mod_v2) -> np.float64:
    dot_prod = np.dot(v1, v2)
    
    cos_theta = dot_prod / (mod_v1 * mod_v2)
    
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    
    angle_rad = np.arccos(cos_theta)
    print(360 - np.degrees(angle_rad))
    
    return np.arccos(cos_theta)