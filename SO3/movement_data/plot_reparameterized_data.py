import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from dataclasses import dataclass
import numpy as np
import pickle
import argparse


from SO3.utils.post_processing_utils import cMDS, inner_cluster_distance, outer_cluster_distance, dictionary_to_matrix, cluster_distances
from SO3.utils.plotting_utils import plot_2d


@dataclass
class plot_distance_matrix:
    level: int = None
    depth: int = None

    def __post_init__(self) -> None:
        if self.level is not None:
            self.distance_path = f'SO3/movement_data/pickle_data/logsig_distances/distances_{self.level}.pkl'
        elif self.depth is not None:
            self.distance_path = f'SO3/movement_data/pickle_data/reparameterized_distances/distances_{self.depth}.pkl'
            
        self.movement_path = 'SO3/movement_data/pickle_data/movements.pkl'

        self.movement_dict = self.load_data(self.movement_path)
        self.distance_dict = self.load_data(self.distance_path)

        self.matrix, self.key_to_index = self.dictionary_to_matrix(self.distance_dict)
        self.descriptions = self.create_list_of_descriptions()
        self.cMDS_coordinates = self.cMDS()
        self.inner_cluster_distance = self.calculate_inner_cluster_distance()
        self.outer_cluster_distance = self.calculate_outer_cluster_distance()
        self.labels = self.cluster_distances()

    def load_data(self, file_path: str) -> dict:
        with open(file_path, 'rb') as f:
            return pickle.load(f) 
        
    def dictionary_to_matrix(self, dictionary: dict) -> np.ndarray:
        return dictionary_to_matrix(dictionary)
    
    def create_list_of_descriptions(self) -> np.ndarray:
        return np.array([self.movement_dict[key]["description"] for key in self.key_to_index.keys()])
    
    def cMDS(self) -> np.ndarray: 
        return cMDS(self.matrix)
    
    def plot(self) -> None:
        plot_2d(self.descriptions, self.cMDS_coordinates[:, :2], self.labels)

    def calculate_inner_cluster_distance(self) -> dict: 
        return inner_cluster_distance(self.movement_dict, self.distance_dict)

    def calculate_outer_cluster_distance(self) -> float:
        return outer_cluster_distance(self.movement_dict, self.distance_dict)
    
    def cluster_distances(self) -> dict:
        number_of_clusters = 3
        return cluster_distances(self.matrix, self.key_to_index, number_of_clusters)


def print_cluster_info(depth: int) -> None:
    plotter = plot_distance_matrix(depth = depth)
    print(f"Depth: {plotter.depth}")
    print(f"Mean 'forward jump': {plotter.inner_cluster_distance['forward jump']['mean']}")
    print(f"Mean 'walk':         {plotter.inner_cluster_distance['walk']['mean']}")
    print(f"Mean 'run/jog':      {plotter.inner_cluster_distance['run/jog']['mean']}")
    print(f"Outer cluster:       {plotter.outer_cluster_distance}")
    # plotter.plot()
    print()


def main(level, depth): 
    plotter = plot_distance_matrix(level = level, depth = depth)
    plotter.plot()
    # print_cluster_info(10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot distance matrix at a given level and depth.')
    parser.add_argument('--level', type=int, default=3, help='Level for the distance matrix.')
    parser.add_argument('--depth', type=int, default=2, help='Depth for the distance matrix.')
    args = parser.parse_args()
    main(args.level, args.depth)
        