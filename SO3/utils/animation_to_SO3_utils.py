import numpy as np

# Rotation matrices
def Rx(a):
    s, c = np.sin(a), np.cos(a)
    return np.array( [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]] )

def Ry(a):
    s, c = np.sin(a), np.cos(a)
    return np.array( [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]] )

def Rz(a):
    s, c = np.sin(a), np.cos(a)
    return np.array( [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]] )

def convert_timeframe_to_SO3(skeleton, frame, filter_noisy_channels=False):
    """
    Converts the rotations of the bones in a given frame into a set of 4x4 matrices that are part of the special orthogonal group (SO3).
    """
    def convert(node):
        """
        Handles the conversion for each bone.
        Computes the rotation matrix for a single bone based on the degress of freedom (dof). 
        """
        if node == 'root':
            transf = [np.deg2rad(x) for x in frame['root']]
            return np.dot(Rz(transf[5]), np.dot(Ry(transf[4]), Rx(transf[3])))


        cbone = skeleton.bones[node]
        #Motion matrix
        M = np.eye(4)
        try:
            for dof, val in zip(cbone.dof, frame[node]):
                val = np.deg2rad(val)
                R = np.eye(4)
                if dof == 'rx':
                    R = Rx(val)
                elif dof == 'ry':
                    R = Ry(val)
                elif dof == 'rz':
                    R = Rz(val)

                M = np.dot(R,M)
        except: #We might not have dof data for the current bone
            pass
        return M

    return { key: convert(key) for key in ['root'] + list(skeleton.bones.keys()) }

def convert_animation_to_SO3(skeleton, animation):
    # Get rotation matrices for all joints and all frames
    bone_names = ['root'] + list(skeleton.bones.keys())

    frames = []
    for frame in animation.get_frames():
        frames.append(convert_timeframe_to_SO3(skeleton, frame, True))
        
    # Convert into numpy arrays
    channels = np.zeros((len(bone_names), len(frames), 3, 3))
    
    i = 0
    for key in animation.channel_order:
        
        if not key in bone_names:
            continue
        i += 1
        for j, frame in enumerate(frames):
            channels[i, j, :, :] = frame[key][:3,:3]

    for i in range(channels.shape[0]):
        for j in range(channels.shape[1]):
            if np.array_equal(channels[i,j,:,:], np.zeros((3,3))):
                channels[i, j, :, :] = np.eye(3) 
            
    return channels