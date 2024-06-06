import numpy as np

from SO3.utils.curve_utils import move_rotation_origin_to_identity, SRVT_single_rotation, skew_matrix_to_vector_single_rotation, right_log_single_rotation

def skew_matrix_to_vector_several_rotations(movement: np.ndarray) -> np.ndarray:
    """
    Transforms a (joints, time, 3, 3) -> (time, 3 * joints)
    """
    vector = np.zeros((movement.shape[1], 3 * movement.shape[0]))
    for i in range(movement.shape[1]):
        vector[i] =  skew_matrix_to_vector_single_rotation(movement[:, i]).flatten()
    return vector

def create_parameterization_several_rotations(movement: np.ndarray) -> np.ndarray:
    return np.linspace(0, 1, movement.shape[1])    

def move_several_rotations_origins_to_identity(rotation: np.ndarray) -> np.ndarray:
    new_rotation = np.zeros(rotation.shape)
    for i, joint in enumerate(rotation):
        new_rotation[i] = move_rotation_origin_to_identity(joint)
    return new_rotation

def SRVT_multiple_rotations(I: np.ndarray, movement: np.ndarray) -> np.ndarray:
    SRVT = np.zeros((movement.shape[0], movement.shape[1] - 1, 3, 3))
    for i, rotation in enumerate(movement):
        SRVT[i] = SRVT_single_rotation(I, rotation)
    return SRVT

def right_log_several_rotations(I: np.ndarray, movement: np.ndarray): 
    right_log = np.zeros((movement.shape[0], movement.shape[1] - 1, 3, 3))
    for i, rotation in enumerate(movement):
        right_log[i] = right_log_single_rotation(I, rotation)
    return right_log