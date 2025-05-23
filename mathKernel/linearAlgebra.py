"""_summary_
    
Bibliote que contem todas as operações de transformações geometricas
"""
    
import numpy as np
import numpy.typing as npt

from public.variables import *


def points_to_pixels(point: npt.NDArray[np.float64]) -> tuple(int, int):
    return (X_ORIGIN + point[0] * SCALE, Y_ORIGIN - point[1] * SCALE)
            