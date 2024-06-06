import unittest
import numpy as np
from SO3.utils.curve_utils import skew_matrix_to_vector_single_rotation

class TestCurveUtils(unittest.TestCase):
    def test_skew_matrix_to_vector_single_rotation(self):
        # Define a test case
        rotation = np.array([
            [[0, -3, 2], [3, 0, -1], [-2, 1, 0]],
            [[0, -4, 5], [4, 0, -6], [-5, 6, 0]],
            [[0, -7, 8], [7, 0, -9], [-8, 9, 0]]
        ])

        # Call the function with the test case
        result = skew_matrix_to_vector_single_rotation(rotation)

        # Define the expected result
        expected_result =  np.array([ 
            [1, 2, 3], 
            [6, 5, 4], 
            [9, 8, 7] 
        ])

        # Assert that the result is as expected
        np.testing.assert_array_equal(result, expected_result)

if __name__ == '__main__':
    unittest.main()