import pickle
from typing import Tuple

def load_movements(file_path = 'SO3/movement_data/pickle_data/movements.pkl') -> dict:
    with open(file_path, 'rb') as f:
        return pickle.load(f)
    
def save_results(results: Tuple[str, str, float], file_path: str) -> None:
    aggregated_results = {}
    for element_1, element_2, result in results:
        aggregated_results[(element_1, element_2)] = result

    with open(file_path, 'wb') as f:
        pickle.dump(aggregated_results, f)