import unittest
import numpy as np
from SO3.utils.multiple_curves_utils import skew_matrix_to_vector_several_rotations

class TestMultipleCurvesUtils(unittest.TestCase):
    def test_skew_matrix_to_vector_several_rotations(self):
        # Define a test case
        rotation_1 = np.array([
            [[0, -3, 2], [3, 0, -1], [-2, 1, 0]],
            [[0, -4, 5], [4, 0, -6], [-5, 6, 0]],
            [[0, -7, 8], [7, 0, -9], [-8, 9, 0]]
        ])

        rotation_2 = np.array([
            [[0, -3.5, 2.5], [3.5, 0, -1.5], [-2.5, 1.5, 0]],
            [[0, -4.5, 5.5], [4.5, 0, -6.5], [-5.5, 6.5, 0]],
            [[0, -7.5, 8.5], [7.5, 0, -9.5], [-8.5, 9.5, 0]]
        ])

        rotation_3 = np.array([
            [[0, -30, 20], [30, 0, -10], [-20, 10, 0]],
            [[0, -40, 50], [40, 0, -60], [-50, 60, 0]],
            [[0, -70, 80], [70, 0, -90], [-80, 90, 0]]
        ])

        movement = np.array([rotation_1, rotation_2, rotation_3])

        # Call the function with the test case
        result = skew_matrix_to_vector_several_rotations(movement)

        # Define the expected result
        expected_result = np.array([
            [1, 2, 3, 1.5, 2.5, 3.5, 10, 20, 30], 
            [6, 5, 4, 6.5, 5.5, 4.5, 60, 50, 40], 
            [9, 8, 7, 9.5, 8.5, 7.5, 90, 80, 70] 
        ])

        # Assert that the result is as expected
        np.testing.assert_array_equal(result, expected_result)

if __name__ == '__main__':
    unittest.main()