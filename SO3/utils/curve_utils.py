import numpy as np
from my_help_functions import tictoc


def exp_map(omega_hat):
    theta = np.linalg.norm([omega_hat[2, 1], omega_hat[0, 2], omega_hat[1, 0]])
    if theta < 1e-10:
        return np.eye(3)
    
    A = omega_hat / theta
    return np.eye(3) + np.sin(theta) * A + (1 - np.cos(theta)) * np.dot(A, A)

def log_map(R):
    theta = np.arccos((np.trace(R) - 1) / 2.0)
    if theta < 1e-10:
        return np.zeros((3, 3))
    
    return (theta / (2 * np.sin(theta))) * (R - R.T)

def create_parameterization_rotation(rotation: np.ndarray) -> np.ndarray:
    return np.linspace(0, 1, rotation.shape[0])

def move_rotation_origin_to_identity(rotation: np.ndarray) -> np.ndarray:
    return np.array([np.dot(rotation_step, rotation[0].T) for rotation_step in rotation])

def SRVT_single_rotation(I: np.ndarray, rotation: np.ndarray) -> np.ndarray:
    TOL = 1e-6

    right_log_derivatives = right_log_single_rotation(I, rotation)

    norms = np.linalg.norm(right_log_derivatives, axis=(1, 2))
    sqrt_norms = np.sqrt(norms)

    scale_factors = np.where(sqrt_norms < TOL, 1, sqrt_norms)
    SRVT = right_log_derivatives / scale_factors[:, np.newaxis, np.newaxis]

    return SRVT

def right_log_derivative(I: np.ndarray, rotation: np.ndarray, index: float) -> np.ndarray:
    return log_map(np.dot(rotation[index + 1], rotation[index].T)) / (I[index + 1] - I[index])

def right_log_single_rotation(I: np.ndarray, rotation: np.ndarray) -> np.ndarray:
    return np.array([right_log_derivative(I, rotation, j) 
                     for j in range(I.shape[0] - 1)]).reshape(rotation.shape[0] - 1, 3, 3)

def skew_matrix_to_vector_single_rotation(rotation: np.ndarray) -> np.ndarray:
    return np.array([[-matrix[1,2], matrix[0,2], -matrix[0,1]] for matrix in rotation])

def vector_to_skew_matrix_single_rotation(vector: np.ndarray) -> np.ndarray:
    return np.array([[0, -vector[2], vector[1]], [vector[2], 0, -vector[0]], [-vector[1], vector[0], 0]])

def interpolate(R0: np.ndarray, R1: np.ndarray, s: float) -> np.ndarray:
    return np.dot(exp_map(s * log_map(np.dot(R1, R0.T))), R0)

def right_log_derivative_vectorized(I: np.ndarray, rotation: np.ndarray) -> np.ndarray:
    indexes = np.arange(I.shape[0] - 1)
    rotation_next = rotation[indexes + 1]
    rotation_current = rotation[indexes]
    product_rotations = np.einsum('ijk,ikl->ijl', rotation_next, np.transpose(rotation_current, (0, 2, 1)))
    delta_I = I[indexes + 1] - I[indexes]
    logm_rotations = np.array([log_map(prod) for prod in product_rotations])
    derivatives = logm_rotations / delta_I[:, None, None]

    return derivatives


