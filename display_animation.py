"""
Script to display animations using Mayavi.

Usage:
    Windows: python display_animation.py YY XX

Arguments:
    YY, XX: Identifiers for the animation to be displayed
"""

from mayavi import mlab
from animation.src.mayavi_animate import mayavi_animate
from animation import fetch_animations, unpack
import sys

# Load data
file_name = sys.argv[1] + "_" + sys.argv[2] + ".amc"
data = fetch_animations(1, file_name=file_name)

# Check if animations are found
if not data:
    print("No animations found for the given identifiers.")
    sys.exit(1)

# Parse data
skeleton, animation, description = unpack(data)
total_frames = animation.num_frames()
print(f"Total number of frames: {total_frames}")
print(f"Description: {description}")
t = 220
animation.crop(t,t + 130)
print(f"Number of frames after cropping: {animation.num_frames()}")

# Run animation
try:
    fig = mlab.figure(bgcolor=(1, 1, 1))  # Set the background color to white
    animator = mayavi_animate(skeleton, animation, [0, 0, 0], fixed_cam=False)
except Exception as e:
    print(f"An error occurred while running the animation: {e}")
    sys.exit(1)

mlab.show()