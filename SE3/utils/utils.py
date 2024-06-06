import numpy as np

TOL = 1e-8

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

def SO3_hat(v): 
    """
    R^3 -> so(3) isomorphism 
    """
    assert v.shape == (3,), f"v must be a 3D vector. v has shape {v.shape}, {v}"
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def SO3_vee(v_hat):
    """
    so(3) -> R^3 isomorphism
    """
    assert v_hat.shape == (3,3), "v_hat must be a 3x3 matrix"
    return np.array([v_hat[2,1], v_hat[0,2], v_hat[1,0]])

def is_SO3(R):
    if R.shape != (3,3):
        return False
    if not np.array_equal(np.dot(R.T, R), np.eye(3)):
        return False
    if not np.array_equal(np.dot(R, R.T), np.eye(3)):
        return False
    if np.linalg.det(R) != 1:
        return False
    return True

def is_SE3(T, tol=1e-6):
    """
    Check if matrix is an element of SE(3), but allow for some tolerance
    """
    R = T[:3, :3]
    is_orthogonal = np.allclose(R.T @ R, np.eye(3), atol=tol)
    has_correct_determinant = np.isclose(np.linalg.det(R), 1, atol=tol)
    has_correct_bottom_row = np.allclose(T[3], [0, 0, 0, 1])
    return is_orthogonal and has_correct_determinant and has_correct_bottom_row

def SE3_assemble_T(R,t): 
    """
    Assemble an element of SE(3) from R in SO(3) and t in R^3
    """
    assert R.shape == (3,3) and t.shape == (3,), "R must be a 3x3 matrix and t must be a 3D vector"
    SE3 = np.eye(4)
    SE3[:3,:3] = R
    SE3[:3,3] = t
    return SE3

def SE3_disassemble_T(T):
    """
    Disassemble an element of SE(3) into R in SO(3) and t in R^3
    """
    assert is_SE3(T), "SE3 must be a 4x4 matrix in SE(3)"
    return T[:3,:3], T[:3,3]

def SE3_assemble_xi(v, rho): 
    """
    Assemble an element of se(3) from v in R^3 and rho in R^3
    """
    assert v.shape == (3,) and rho.shape == (3,), "v and rho must be 3D vectors"
    return np.concatenate([v, rho])

def SE3_disassemble_xi(xi):
    """
    Disassemble an element of se(3) into v in R^3 and rho in R^3
    """
    assert xi.shape == (6,), "xi must be a 6D vector"
    return xi[:3], xi[3:]

def SE3_dot(T_0, T_1):
    """
    Dot product in SE(3)
    """
    assert T_0.shape == (4,4) and T_1.shape == (4,4), f"T_0 and T_1 must be 4x4 matrices in SE(3) \n T_0: \n {T_0.shape} \n T_1: \n {T_1.shape}"
    assert is_SE3(T_0) and is_SE3(T_1), f"T_0 and T_1 must be 4x4 matrices in SE(3) \n T_0: \n {T_0} \n T_1: \n {T_1}"
    R_0, t_0 = SE3_disassemble_T(T_0)
    R_1, t_1 = SE3_disassemble_T(T_1)
    T_new = SE3_assemble_T(np.dot(R_0, R_1), t_0 + np.dot(R_0, t_1))
    assert np.allclose(T_new, np.dot(T_0, T_1)), f"T_new must be equal to the dot product of T_0 and T_1 \n T_new: \n {T_new} \n T_0.dot(T_1): \n {T_0.dot(T_1)}"
    return T_new

def SE3_inv(T):
    """
    Inverse in SE(3)
    """
    assert is_SE3(T), f"SE3 must be a 4x4 matrix in SE(3), but is {T}"
    R, t = SE3_disassemble_T(T)
    return SE3_assemble_T(R.T, -np.dot(R.T, t))

def left_jacobian(v):
    """
    Left Jacobian for v in R^3 (se(3) isomorphism)   
    """
    assert v.shape == (3,), "v must be in R^3"
    
    if np.linalg.norm(v, 2) < TOL:
        return np.eye(3)

    v_hat = SO3_hat(v)
    v_norm = np.linalg.norm(v)
    return np.eye(3) + (1 - np.cos(v_norm)) / v_norm**2 * v_hat + (v_norm - np.sin(v_norm)) / v_norm**3 * np.dot(v_hat, v_hat)

def inv_left_jacobian(v):
    assert v.shape == (3,), "v must be in R^3"
    if np.linalg.norm(v, 2) < TOL:
        return np.eye(3)
    v_hat = SO3_hat(v)
    v_norm = np.linalg.norm(v)
    return np.eye(3) - 0.5 * v_hat + (1 / v_norm**2 - (1 + np.cos(v_norm)) / (2 * v_norm * np.sin(v_norm))) * np.dot(v_hat, v_hat)

def SE3_exp(xi_hat):
    """
    Lie algebra se(3) -> Lie group SE(3)
    
    Input: 
        xi_hat: 4x4 matrix in se(3)
    """
    assert xi_hat.shape == (4,4), "xi_hat must be a 4x4 matrix"
    v_hat = xi_hat[:3,:3]
    v = SO3_vee(v_hat)
    rho = xi_hat[:3,3] 
    exp_xi_hat = np.eye(4)
    exp_xi_hat[:3,:3] = exp_map(v_hat)
    exp_xi_hat[:3,3] = np.dot(left_jacobian(v), rho)
    assert not np.isnan(exp_xi_hat).any(), "exp_xi_hat contains NaNs"
    return exp_xi_hat

def SE3_hat(xi): 
    """
    Isoomorphism from R^6 to se(3)
    """
    assert xi.shape == (6,), "xi must be a 6D vector"
    xi_hat = np.zeros((4,4))
    xi_hat[:3,:3] = SO3_hat(xi[:3])
    xi_hat[:3,3] = xi[3:]
    return xi_hat

def SE3_vee(xi_hat):
    """
    Isoomorphism from se(3) to R^6
    """
    assert xi_hat.shape == (4,4), "xi_hat must be a 4x4 matrix"
    v_hat = xi_hat[:3,:3]
    v = SO3_vee(v_hat)
    rho = xi_hat[:3,3]
    return SE3_assemble_xi(v, rho)

def SE3_log(T): 
    """
    Lie group SE(3) -> Lie algebra se(3)

    Input:
        T: 4x4 matrix in SE(3)
    """
    assert is_SE3(T), f"T must be a 4x4 matrix in SE(3), but is {T}"
    R, t = SE3_disassemble_T(T)
    v_hat = log_map(R)
    v = SO3_vee(v_hat)
    rho = np.dot(inv_left_jacobian(v), t)
    return SE3_hat(np.concatenate([v, rho]))

def SE3_interpolate(T0, T1, s):
    """
    Interpolate in SE(3)

    Input:
        T0: 4x4 matrix in SE(3)
        T1: 4x4 matrix in SE(3)
        s: scalar in [0,1]
    
    Output:
        T: 4x4 matrix in SE(3)
    """
    return SE3_dot(SE3_exp(s * SE3_log(SE3_dot(T1, SE3_inv(T0)))), T0)

def SE3_reparameterize(I_new, I, c):
    assert I.shape[0] == c.shape[0], "I and c must have the same length"
    assert I_new[0] == 0, "I_new must start at 0"
    assert I_new[-1] == 1, "I_new must end at 1"
    assert np.all(np.diff(I_new) > 0), "I_new must be in ascending order"

    c_new = np.zeros(c.shape)
    N = c.shape[0]
    j = 0
    for i in range(N):
        phi = I_new[i]
        while not I[j] <= phi <= I[(j+1)]:
            j += 1

        # Linear assumption? 
        s = (phi - I[j]) / (I[(j+1)] - I[j])
        assert 0 <= s <= 1, f"s must be between 0 and 1, but is {s}"
        c_new[i] = SE3_interpolate(c[j], c[(j+1)], s)

    return c_new