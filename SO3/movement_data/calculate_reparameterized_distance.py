from dataclasses import dataclass
import numpy as np
from typing import Tuple

from SO3.utils.multiple_curves_utils import move_several_rotations_origins_to_identity, create_parameterization_several_rotations, SRVT_multiple_rotations, skew_matrix_to_vector_several_rotations
from SO3.utils.reparameterization_utils import find_optimal_diffeomorphism, reparameterize_multiple_rotations, L2_metric
from my_help_functions import tictoc

@dataclass
class reparameterized_distance:
    movement_1: np.ndarray
    movement_2: np.ndarray
    depth: int = 2

    def __post_init__(self) -> None:
        # Preprocess the movements
        self.moved_movement_1, self.I1, self.vector_1 = self.process_movement(self.movement_1)
        self.moved_movement_2, self.I2, self.vector_2 = self.process_movement(self.movement_2)

        # Reparameterize the second movement
        self.I_new = self.find_optimal_diffeomorphism(self.vector_1, self.vector_2, self.I1, self.I2, self.depth)
        self.movement_2_new = self.reparameterize(self.I_new, self.I2, self.movement_2)
        self.moved_movement_2_new, self.I_reg, self.vector_2_new = self.process_movement(self.movement_2_new)

        # Compute the distance
        self.distance = self.L2_metric(self.vector_1, self.vector_2_new, self.I1, self.I_reg)

    def process_movement(self, movement: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        moved_movement = self.move_several_rotations_origins_to_identity(movement)
        I = self.create_parameterization_several_rotations(moved_movement)
        SRVT = self.SRVT_multiple_rotations(I, moved_movement)
        vector = self.skew_matrix_to_vector_several_rotations(SRVT)
        return moved_movement, I, vector

    
    def skew_matrix_to_vector_several_rotations(self, movement: np.ndarray) -> np.ndarray:
        return skew_matrix_to_vector_several_rotations(movement)
    
    def create_parameterization_several_rotations(self, movement: np.ndarray) -> np.ndarray:
        return create_parameterization_several_rotations(movement) 

    def move_several_rotations_origins_to_identity(self, rotation: np.ndarray) -> np.ndarray:
        return move_several_rotations_origins_to_identity(rotation)

    def SRVT_multiple_rotations(self, I: np.ndarray, movement: np.ndarray) -> np.ndarray:
        return SRVT_multiple_rotations(I, movement)

    def find_optimal_diffeomorphism(self, q0: np.ndarray, q1: np.ndarray, I0: np.ndarray, I1: np.ndarray, depth: int) -> np.ndarray:
        return find_optimal_diffeomorphism(q0, q1, I0, I1, depth)

    def reparameterize(self, I_new: np.ndarray, I: np.ndarray, c: np.ndarray) -> np.ndarray:
        return reparameterize_multiple_rotations(I_new, I, c)
    
    def L2_metric(self, q0: np.ndarray, q1: np.ndarray, I0: np.ndarray, I1: np.ndarray) -> float:
        return L2_metric(q0, q1, I0, I1)


