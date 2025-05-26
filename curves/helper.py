import numpy as np
import numpy.typing as npt

def translate_matrix(point: npt.NDArray[np.float64]) -> npt.NDArray[npt.NDArray[np.float64]]:
    t_matrix = np.eye(4, dtype=np.float64)
        
    t_matrix[0][3] = point[0]
    t_matrix[1][3] = point[1]
    t_matrix[2][3] = point[2]
        
    return t_matrix

def rotate_matrix(oint: npt.NDArray[np.float64]) -> npt.NDArray[npt.NDArray[np.float64]]:
    pass