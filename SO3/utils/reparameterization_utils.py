import numpy as np
import functools

from SO3.utils.curve_utils import interpolate

def create_shared_parameterization(q0, q1, I0, I1):

    if np.array_equal(I0, I1):
        return I0, q0, q1

    #create array of shared interpolation points
    I = np.unique(np.concatenate((I0, I1)))
    i,j = 0,0
    q0_new = np.zeros((I.shape[0], q0.shape[1]))
    q1_new = np.zeros((I.shape[0], q0.shape[1]))

    #interpolate to previous when creating diff
    for k in range(I.shape[0]-1):
        q0_new[k] = q0[i]
        q1_new[k] = q1[j]

        if I0[i+1] <= I[k+1]:
            i +=1
        if I1[j+1] <= I[k+1]:
            j +=1

    return I, q0_new, q1_new


def L2_metric(q0, q1, I0, I1):
    if np.array_equal(I0, I1):
        dI = np.diff(I0) 
        squared_L2_norms = np.sum((q0 - q1)**2, axis=1)      
        integral_approximation = np.sum(squared_L2_norms * dI)
        return np.sqrt(integral_approximation)
    
    #create array of shared interpolation points
    I = np.unique(np.concatenate((I0, I1)))
    i,j = 0,0
    l2_sum = 0.0

    #interpolate to previous when creating diff
    for k in range(I.shape[0]-1):
        l2_sum += (I[k+1] - I[k]) * (np.linalg.norm(q0[i] - q1[j])**2)

        if I0[i+1] <= I[k+1]:
            i +=1
        if I1[j+1] <= I[k+1]:
            j +=1

    return np.sqrt(l2_sum)

def L2_metric_SE3(q0, q1, I0, I1):
    if np.array_equal(I0, I1):
        dI = np.diff(I0) 
        squared_L2_norms = 2 * np.sum((q0[:,:3] - q1[:,:3])**2, axis=1) +  np.sum((q0[:,3:] - q1[:,3:])**2, axis=1)      
        integral_approximation = np.sum(squared_L2_norms * dI)
        return np.sqrt(integral_approximation)

    #create array of shared interpolation points
    I = np.unique(np.concatenate((I0, I1)))
    i,j = 0,0
    l2_sum = 0.0

    #interpolate to previous when creating diff
    for k in range(I.shape[0]-1):
        l2_sum += (I[k+1] - I[k]) * (np.linalg.norm(q0[i] - q1[j])**2)

        if I0[i+1] <= I[k+1]:
            i +=1
        if I1[j+1] <= I[k+1]:
            j +=1

    return np.sqrt(l2_sum)

def local_cost(k, l, i, j, q0, q1, I, lambda_reg = 1e-9):
    def warp(k, l, i, j, t): 
        return l + (t-k) * (j-l) / (i-k)
    s_m = I[k + 1: i + 1]
    diff_reg = lambda_reg * np.sum(np.abs(warp(k, l, i, j, s_m) - s_m)**2)
    cost = L2_metric(
            q0[k:i+1],
            np.sqrt((I[j]-I[l])/(I[i]-I[k]))*q1[l:j+1],
            I[k:i+1],
            np.linspace(I[k], I[i], (j-l+1))
        )
    return cost + diff_reg

def local_cost_SE3(k, l, i, j, q0, q1, I, lambda_reg = 1e-9):
    def warp(k, l, i, j, t): 
        return l + (t-k) * (j-l) / (i-k)
    s_m = I[k + 1: i + 1]
    diff_reg = lambda_reg * np.sum(np.abs(warp(k, l, i, j, s_m) - s_m)**2)
    cost = L2_metric_SE3(
            q0[k:i+1],
            np.sqrt((I[j]-I[l])/(I[i]-I[k]))*q1[l:j+1],
            I[k:i+1],
            np.linspace(I[k], I[i], (j-l+1))
            )
    return cost + diff_reg

def local_cost_regulated(k, l, i, j, q0, q1, I):
    cost_l2 = local_cost(k, l, i, j, q0, q1, I)
    new_q1 = np.sqrt((I[j]-I[l])/(I[i]-I[k]))*q1[l:j] 

    # # This regulates how much the curve can change
    # def warp(k, l, i, j, t): 
    #     return l + (t-k) * (j-l) / (i-k)
    
    # # k < s_m <= i 
    # s_m = I[k + 1: i + 1]
    # lambda_reg = 0.0001
    # diff_reg = lambda_reg * np.sum(np.abs(warp(k, l, i, j, s_m) - s_m)**2)

    lambda_reg = 10
    L1_reg = lambda_reg * np.mean(np.abs(new_q1))

    return cost_l2 + L1_reg

    

def dynamic(local_cost, M, depth):
    A = np.zeros((M, M))
    pointers = dict()

    for i in range(M):
        for j in range(M):
            if i == 0 and j == 0:
                A[i, j] = 0
                continue
            min_cost = np.inf
            best_pred = None

            for pred in predecessors(i, j, depth):
                k, l = pred
                cost = local_cost(k, l, i, j) + A[k, l]
                if min_cost > cost:
                    min_cost = cost
                    best_pred = pred
            A[i, j] = min_cost
            pointers[(i, j)] = best_pred

    return pointers, A


def predecessors(i, j, depth):
    return ((k, l) for k in range(np.maximum(0, i - depth), i) for l in range(np.maximum(0, j - depth), j) if np.gcd(i-k, j-l) == 1)

def find_optimal_diffeomorphism(q0, q1, I0, I1, depth):
    I, q0_new, q1_new = create_shared_parameterization(q0, q1, I0, I1)
    M = I.shape[0]
    local_cost_partial = functools.partial(local_cost, q0 = q0_new, q1 = q1_new, I = I)

    pointers, A = dynamic(local_cost_partial, M, depth)
    path = reconstruct(pointers, M-1, M-1)

    #Construct reparametrization
    x = np.array([p[0] for p in path])/float(M-1)
    y = np.array([p[1] for p in path])/float(M-1)

    I_new = np.interp(I1, x, y)
    return I_new

def find_optimal_diffeomorphism_SE3(q0, q1, I0, I1, depth):
    I, q0_new, q1_new = create_shared_parameterization(q0, q1, I0, I1)
    M = I.shape[0]
    local_cost_partial = functools.partial(local_cost_SE3, q0 = q0_new, q1 = q1_new, I = I)

    pointers, A = dynamic(local_cost_partial, M, depth)
    path = reconstruct(pointers, M-1, M-1)

    #Construct reparametrization
    x = np.array([p[0] for p in path])/float(M-1)
    y = np.array([p[1] for p in path])/float(M-1)

    I_new = np.interp(I1, x, y)
    return I_new
    

def reconstruct(pointers, M, N):
    path = [(M,N)]
    try:
        while True:
            pred = path[-1]
            path.append(pointers[pred])
    except:
        pass

    path.reverse()
    return path


    
def reparameterize_multiple_rotations(I_new, I, c):
    """
    Creates the new movement
    Input:
        I_new: new parameterization
        I: old parameterization
        c: old movement
    Output:
        c_new: new movement
    """
    c_new = np.zeros(c.shape)
    for i in range(c.shape[0]):
        c_new[i] = reparameterize_rotation(I_new, I, c[i])
    return c_new


def reparameterize_rotation(I_new, I, c):
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
        c_new[i] = interpolate(c[j], c[(j+1)], s)

    return c_new

