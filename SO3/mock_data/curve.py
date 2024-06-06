import numpy as np
from dataclasses import dataclass
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

from SO3.utils.curve_utils import move_rotation_origin_to_identity

@dataclass
class Curve:
    number_of_points: int
    angle_x: float = np.pi / 2
    angle_y: float = np.pi
    f : callable = lambda x: x

    def __post_init__(self):
        self.x_axis : np.ndarray = np.array([1, 0, 0])
        self.y_axis : np.ndarray = np.array([0, 1, 0])
        self.I : np.ndarray  = self.f(np.linspace(0, 1, self.number_of_points))
        self.rotations : np.ndarray = self.create_curve()
        self.move_origin_to_identity()

    def get_parameterization(self) -> np.ndarray:
        return self.I
    
    def get_rotations(self) -> np.ndarray:
        return self.rotations

    def rotate(self, axis: np.ndarray, angle: float) -> np.ndarray:
        return R.from_rotvec(axis * angle).as_matrix()

    def rotate_x(self, angle: float) -> np.ndarray:
        return self.rotate(self.x_axis, angle)

    def rotate_y(self, angle: float) -> np.ndarray:
        return self.rotate(self.y_axis, angle)
    
    def create_curve(self) -> np.ndarray:
        rotations = np.zeros((self.number_of_points, 3, 3))
        for i in range(self.number_of_points):
            rotation_x = self.rotate_x(self.angle_x * self.I[i])
            rotation_y = self.rotate_y(self.angle_y * (1 - self.I[i]))
            rotations[i] = rotation_x @ rotation_y 
        return rotations
    
    def move_origin_to_identity(self) -> np.ndarray:
        self.rotations = move_rotation_origin_to_identity(self.rotations)

    def plot_rotations(self, plot_sphere=True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Original unit vector (z-axis)
        original_vector = np.array([0, 0, 1])

        for R in self.rotations:
            # Apply the rotation to the vector
            rotated_vector = np.dot(R, original_vector)

            # Plotting
            ax.scatter(*rotated_vector, color='red', alpha=0.5)

        # Create a sphere
        def sphere(ax):
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = np.outer(np.cos(u), np.sin(v))
            y = np.outer(np.sin(u), np.sin(v))
            z = np.outer(np.ones(np.size(u)), np.cos(v))

            ax.plot_surface(x, y, z, color='y', alpha=.5)

        if plot_sphere:
            sphere(ax)


        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show()


def main():
    curve = Curve(100, np.pi / 2, 1.5 * np.pi)
    curve.plot_rotations()
    print(curve.number_of_points)
if __name__ == "__main__":
    main()

