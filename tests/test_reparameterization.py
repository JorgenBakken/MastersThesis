import unittest
import numpy as np
from SO3.mock_data.reparameterization import ShapeDistance
from SO3.mock_data.curve import Curve

class TestReparameterization(unittest.TestCase):
    def setUp(self):
        self.sd = ShapeDistance()  # Create an instance of ShapeDistance
        self.R0 = np.eye(3)
        self.R1 = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
        self.I = np.linspace(0,1,10)
        self.I_new = [0, .1,.2,.3,.43,.45,.6, .7, .8,1]
        self.curve = Curve(10)
        self.c = self.curve.get_rotations()

    def test_interpolate_s_zero(self):
        result = self.sd.interpolate(self.R0, self.R1, s=0)
        np.testing.assert_allclose(result, self.R0, atol=1e-15)

    def test_interpolate_s_one(self):
        result = self.sd.interpolate(self.R0, self.R1, s=1)
        np.testing.assert_allclose(result, self.R1, atol=1e-15)

    def test_reparameterize_first_rotation(self):
        result = self.sd.reparameterize(self.I_new, self.I, self.c)
        np.testing.assert_allclose(result[0], self.c[0], atol=1e-15)

    def test_reparameterize_last_rotation(self):
        result = self.sd.reparameterize(self.I_new, self.I, self.c)
        np.testing.assert_allclose(result[-1], self.c[-1], atol=1e-15)

if __name__ == '__main__':
    unittest.main()