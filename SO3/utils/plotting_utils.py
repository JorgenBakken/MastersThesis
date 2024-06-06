import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

def plot_2d(descriptions: np.ndarray, coordinates_2d: np.ndarray, labels: list) -> None:
    # Define a color map
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, 3))
    # Define a mapping from descriptions to integers
    description_to_int = {'forward jump': 0, 'walk': 1, 'run/jog': 2}

    # Plot the coordinates
    plt.figure(figsize=(10, 10))
    for i, description in enumerate(descriptions):
        plt.scatter(coordinates_2d[i, 0], coordinates_2d[i, 1], color=colors[description_to_int[description]])

    for i, label in enumerate(labels):
        plt.annotate(label, (coordinates_2d[i, 0], coordinates_2d[i, 1]))

    # Create a custom legend
    legend_elements = [Patch(facecolor=colors[i], label=description) for description, i in description_to_int.items()]
    plt.legend(handles=legend_elements)
    plt.show()