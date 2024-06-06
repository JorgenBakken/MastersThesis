import unittest
import numpy as np
from SO3.mock_data.curve import Curve  

class TestCurve(unittest.TestCase):
    def test_rotations_are_so3(self):
        """
        Test that the rotations are in SO(3)
            - det(R) = 1
            - R.T = R^-1
        """
        curve = Curve(100)  
        for R in curve.create_curve():
            self.assertAlmostEqual(np.linalg.det(R), 1, places=6)
            self.assertTrue(np.allclose(R.T, np.linalg.inv(R)))

    def test_I_range(self):
        """
        Test that the I values are in the range [0, 1], and strictly increasing
            - I[0] = 0
            - I[-1] = 1
            - I[i] < I[i+1] for all i
        """
        for i, f in enumerate([lambda x: x, lambda x: x**2, lambda x: np.sin(x) / np.sin(1), lambda x: np.log(1 + x) / np.log(2)]):
            curve = Curve(1000, f = f)
            self.assertEqual(curve.I[0], 0, f"Failed at function {i} for I[0]")
            self.assertEqual(curve.I[-1], 1, f"Failed at function {i} for I[-1]")
            self.assertTrue(np.all(np.diff(curve.I) > 0), f"Failed at function {i} for I strictly increasing")

    def test_curve_creation_without_f(self):
        """
        Test that the curve is created without a function
        """
        curve = Curve(100)
        self.assertIsInstance(curve, Curve)

    def test_curve_start_in_identity(self):
        """
        Test that the curve starts in the identity
        """
        curve = Curve(100)
        self.assertTrue(np.allclose(curve.rotations[0], np.eye(3)))

if __name__ == '__main__':
    unittest.main()