import mayavi.mlab as mlab
import numpy as np
import traceback

@mlab.animate(delay=10, ui=True)
def mayavi_animate(skeleton, animation, offset, fixed_cam=False):
    """
    Animate a 3D skeleton using Mayavi.
    
    Parameters:
    - skeleton: Object containing skeleton information
    - animation: Object containing animation information
    - offset: 3D offset to apply to the model
    - fixed_cam: Boolean indicating whether to fix the camera view
    """
    surf = init_mayavi_animation(skeleton)

    # Set initial camera view
    mlab.view(0, 135, 25, np.zeros(3), roll=0)
    num_steps = 1

    # Iterate over animation frames
    for _ in range(int(np.floor(animation.num_frames() / num_steps))):  

        try:
            # Create a new figure for every frame
            # surf = init_mayavi_animation(skeleton, line_width=5)
            update_mayavi_animation(surf, skeleton, animation, offset, num_steps=num_steps) 
            # else:
            #     update_mayavi_animation(surf, skeleton, animation, offset, set = False)
            if not fixed_cam:
                mlab.view(30, 35, 10, roll=0)

        except:  
            print(traceback.format_exc())
            return
        
        yield


def init_mayavi_animation(skeleton, line_width = 5):
    """
    Initialize a Mayavi animation.

    Parameters:
    - skeleton: Object containing skeleton information
    """
    
    # Get skeleton coordinates and lines
    coords = skeleton.get_skeleton_neutral_coords() 
    skeleton.get_skeleton_neutral_lines()

    # Create figure
    src = mlab.pipeline.scalar_scatter(coords[0], coords[1], coords[2])
    src.mlab_source.dataset.lines = skeleton._lines
    src.update()
    plotlines = mlab.pipeline.stripper(src)
    surf = mlab.pipeline.surface(plotlines, color=(0,0,0), line_width=line_width)
    return surf

def update_mayavi_animation(surf, skeleton, animation, offset, num_steps = 1):
    """
    Update a Mayavi animation.

    Parameters:
    - surf: Mayavi surface object
    - skeleton: Object containing skeleton information
    - animation: Object containing animation information
    - offset: 3D offset to apply to the model
    """
    for _ in range(num_steps):
        animation.step(animation)
    frame, anim_offset = animation.get_current_frame()
    coords = skeleton.get_coords_for_frame(frame, anim_offset)
    surf.mlab_source.reset(
        x = coords[0] + offset[0],
        y = coords[1] + offset[1],
        z = coords[2] + offset[2]
    )
