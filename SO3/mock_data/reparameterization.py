from SO3.mock_data.curve import Curve
from dataclasses import dataclass
import numpy as np
import time

from SO3.utils.reparameterization_utils import find_optimal_diffeomorphism, reparameterize_rotation, L2_metric
from SO3.utils.curve_utils import skew_matrix_to_vector_single_rotation, SRVT_single_rotation, right_log_derivative, interpolate

@dataclass
class ShapeDistance:

    def __post_init__(self):
        pass

    def L2_metric(self, q0, q1, I0, I1):
        return L2_metric(q0, q1, I0, I1)

    def find_optimal_diffeomorphism(self, q0, q1, I0, I1, depth):
        return find_optimal_diffeomorphism(q0, q1, I0, I1, depth)

    def reparameterize(self, I_new, I, c):
        return reparameterize_rotation(I_new, I, c)

    def interpolate(self, R0, R1, s) -> np.ndarray:
        return interpolate(R0, R1, s)
    
    def right_log_derivative(self, c, I, i) -> np.ndarray:
        return right_log_derivative(I, c, i)

    def SRVT(self, I, c) -> np.ndarray:
        return SRVT_single_rotation(I, c)

    def skew_matrix_to_vector(self, matrices) -> np.ndarray:
        return skew_matrix_to_vector_single_rotation(matrices)
    
def main():
    
    f = lambda x: x**2
    for n_steps in [4, 8, 16]:
        # depth = 20

        start = time.time()
        curve1 = Curve(n_steps, f = f)
        curve2 = Curve(n_steps)
        sd = ShapeDistance()
        _, c0 = curve1.get_parameterization(), curve1.get_rotations()
        _, c1 = curve2.get_parameterization(), curve2.get_rotations()
        I = np.linspace(0, 1, n_steps)
        # print(f"Time to create curves: {time.time() - start} seconds")

        start = time.time()
        q0 = sd.skew_matrix_to_vector(sd.SRVT(I, c0))
        q1 = sd.skew_matrix_to_vector(sd.SRVT(I, c1))
        # print(f"Time to create SRVT: {time.time() - start} seconds")

        start = time.time()
        I1_new = sd.find_optimal_diffeomorphism(q0, q1, I, I, depth = n_steps)
        # print(f"Time to find optimal diffeomorphism: {time.time() - start} seconds")

        start = time.time()
        c1_new = sd.reparameterize(I1_new, I, c1)
        # print(f"Time to reparameterize: {time.time() - start} seconds")

        start = time.time()
        q0 = sd.skew_matrix_to_vector(sd.SRVT(I, c0))
        q1 = sd.skew_matrix_to_vector(sd.SRVT(I, c1_new))
        # print(f"Time to create SRVT: {time.time() - start} seconds")


        print(f"Steps = {n_steps} : {sd.L2_metric(q0, q1, I, I)}")


if __name__ == "__main__":
    main()


