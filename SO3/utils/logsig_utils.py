import iisignature
import numpy as np
from typing import List, Tuple

from SO3.utils.multiple_curves_utils import move_several_rotations_origins_to_identity, create_parameterization_several_rotations, right_log_several_rotations, skew_matrix_to_vector_several_rotations

def initialize_logsig(level: int):
    dimensions = 69
    preprocessed_data = iisignature.prepare(dimensions, level)
    return preprocessed_data

def calculate_logsig(movement: np.ndarray, preprocessed_data) -> np.ndarray:
    movement_moved = move_several_rotations_origins_to_identity(movement)
    I = create_parameterization_several_rotations(movement_moved)
    right_log_movement = right_log_several_rotations(I, movement_moved)
    vector = skew_matrix_to_vector_several_rotations(right_log_movement)
    return iisignature.logsig(vector, preprocessed_data)

def calculate_distances(log_signature_dict: dict) -> List[Tuple[str, str, float]]:  
    distances = []
    for key_1, value_1 in log_signature_dict.items():
        for key_2, value_2 in log_signature_dict.items():
            if key_1 <= key_2:
                distance = np.linalg.norm(value_1 / np.linalg.norm(value_1) - value_2 / np.linalg.norm(value_2))
                distances.append((key_1, key_2, distance))

    return distances