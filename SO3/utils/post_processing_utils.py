import numpy as np
from sklearn.cluster import KMeans

def dictionary_to_matrix(dictionary: dict) -> np.ndarray:
    # Extract unique keys from the tuples
    unique_keys = sorted(set(key for pair in dictionary.keys() for key in pair))
    
    # Create a map from key to index
    key_to_index = {key: index for index, key in enumerate(unique_keys)}

    # Initialize the matrix
    size = len(unique_keys)
    matrix = np.ones((size, size)) * -1 

    # Populate the matrix
    for (key1, key2), value in dictionary.items():
        i = key_to_index[key1]
        j = key_to_index[key2]
        matrix[i][j] = value
        matrix[j][i] = value  
    
    assert np.all(matrix >= 0), "Matrix was not populated correctly"

    return matrix, key_to_index

def cluster_distances(matrix: np.ndarray, key_to_index: dict, number_of_clusters: int) -> list:
    """
    Takes in a matrix and try to cluster it into number_of_clusters clusters.
    After clustering, it maps each point to a key in the key_to_index dictionary.
    Returns a dictionary of the form: key: cluster_number
    """
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=number_of_clusters, n_init = 10, random_state=0).fit(matrix)

    # Get the cluster labels for each point in the matrix
    labels = kmeans.labels_

    # Create a dictionary mapping keys to cluster numbers
    #cluster_dict = {key: labels[index] for key, index in key_to_index.items()}

    return labels


def cMDS(matrix: np.ndarray) -> np.ndarray:
    # Center the matrix
    n = len(matrix)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -J.dot(matrix ** 2).dot(J) / 2

    # Diagonalize the matrix
    eigenvalues, eigenvectors = np.linalg.eig(B)
    eigenvalues = np.where((eigenvalues < 0) & (np.abs(eigenvalues) < 1e-6), 0, eigenvalues)

    #assert np.all(eigenvalues >= 0), f"Eigenvalues were not all positive {eigenvalues}"
    if not np.all(eigenvalues >= 0):
        print(f"Eigenvalues were not all positive {eigenvalues}")

    # Make sure all eigenvalues are positive
    eigenvalues = np.maximum(eigenvalues, 0)


    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Compute the coordinates
    coordinates = eigenvectors * np.sqrt(eigenvalues)
    return coordinates

def inner_cluster_distance(dict_of_movements: dict, dict_of_distances: dict) -> dict:
    # Initialize dictionaries to hold distances for each movement type
    distances = {
        "forward jump": {"distances": [], "mean": None},
        "walk": {"distances": [], "mean": None},
        "run/jog": {"distances": [], "mean": None}
    }

    # Loop through the dictionary of distances
    for key, distance in dict_of_distances.items():
        # Skip if the movement is compared to itself or if they are not in the same cluster
        if key[0] == key[1] or dict_of_movements[key[0]]["description"] != dict_of_movements[key[1]]["description"]:
            continue

        # Add the distance to the appropriate list
        description = dict_of_movements[key[0]]["description"]
        if description in distances:
            distances[description]["distances"].append(distance)
        else:
            raise ValueError("Description not found")
        
    for description in distances:
        if len(distances[description]["distances"]) == 0:
            raise AssertionError(f"No distances were added to the {description} cluster")
        distances[description]["mean"] = np.mean(distances[description]["distances"])

    return distances

def outer_cluster_distance(dict_of_movements: dict, dict_of_distances: dict) -> float:
    # Initialize a list to hold distances between movements of different types
    distances = []

    # Loop through the dictionary of distances
    for key, distance in dict_of_distances.items():
        # Check if the movements are of different types
        if dict_of_movements[key[0]]["description"] != dict_of_movements[key[1]]["description"]:
            # If they are, add the distance to the list of distances
            distances.append(distance)

    assert len(distances) > 0, f"No distances were added to the outer cluster"

    # Calculate the average distance and return it
    return np.mean(distances)

