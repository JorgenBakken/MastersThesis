import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation

def SE3_transform_element(T, point, orientation):
    """

    """
    point_homogeneous = np.append(point, 1)
    point_transformed_homogeneous = np.dot(T, point_homogeneous)
    point_transformed = point_transformed_homogeneous[:3]
    orientation_transformed = np.dot(T[:3, :3], orientation)
    return point_transformed, orientation_transformed

def SE3_transform_curve(c, initial_point=np.zeros(3), initial_orientation=np.eye(3)):
    """
    Transform a curve in SE3 to a set of points and orientations
    This makes it possible to visualize the curve in 3D
    The points are given as (x, y, z) and the orientations as 3x3 matrices in SO3

    Input:
        c: np.array, shape (n, 4, 4)
        initial_point: np.array, shape (3,)
        initial_orientation: np.array, shape (3,3)

    Output:
        points: np.array, shape (n+1, 3)
        orientations: np.array, shape (n+1, 3, 3)
    """
    points = np.zeros((c.shape[0] + 1, 3))
    orientations = np.zeros((c.shape[0] + 1, 3, 3)) 
    points[0], orientations[0] = initial_point, initial_orientation
    
    for i, T in enumerate(c):
        points[i + 1], orientations[i + 1] = SE3_transform_element(T, points[i], orientations[i])
    
    return points, orientations

def SE3_visualize_curve(points, orientations, scale):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting points
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='k', s=5)
    ax.plot(points[:, 0], points[:, 1], points[:, 2], color='blue', linestyle='dotted')

    # Colors for the x, y, and z axes
    colors = ['r', 'g', 'b']

    for i in range(len(points)):
        start_point = points[i]
        for j in range(3):
            # Orientation vector for each axis
            direction = orientations[i, :, j]
            end_point = start_point + scale * direction
            ax.quiver(start_point[0], start_point[1], start_point[2],
                        direction[0], direction[1], direction[2], length=scale, color=colors[j])

    # Assuming 'ax' is your 3D axis and 'points' is your data
    max_range = np.array([points[:, 0].max()-points[:, 0].min(), points[:, 1].max()-points[:, 1].min(), points[:, 2].max()-points[:, 2].min()]).max() / 2.0

    mid_x = (points[:, 0].max()+points[:, 0].min()) * 0.5
    mid_y = (points[:, 1].max()+points[:, 1].min()) * 0.5
    mid_z = (points[:, 2].max()+points[:, 2].min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def SO3_to_euler_angles_scipy(R_matrix):
    """
    Convert a rotation matrix to euler angles using scipy

    Input:
        R_matrix: 3x3 rotation matrix (SO(3))

    Output:
        euler_angles_degrees: 3x1 vector of euler angles in degrees
    """
    rotation = Rotation.from_matrix(R_matrix)
    euler_angles_radians = rotation.as_euler('xyz', degrees=True)
    return euler_angles_radians