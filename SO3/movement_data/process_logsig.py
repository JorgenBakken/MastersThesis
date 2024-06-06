import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from SO3.utils.logsig_utils import initialize_logsig, calculate_logsig, calculate_distances
from SO3.utils.io_utils import load_movements, save_results
from my_help_functions import tictoc

def process_logsig(movements, level) -> dict:

    print(f"Initializing logsig with level {level}")
    s = initialize_logsig(level)
    print("Done initializing logsig")

    log_signature_dict = {}
    num_movements = len(movements)
    operation_count = 0  
    for key, value in movements.items():
        log_signature_dict[key] = calculate_logsig(value["curve"], s)
        operation_count += 1
        print(f"Finished {operation_count} of {num_movements} ")


    return log_signature_dict

@tictoc
def main():
    movements = load_movements()

    truncation_level = 3

    log_signature_dict = process_logsig(movements, truncation_level)
    logsig_distances = calculate_distances(log_signature_dict)

    result_path = f'SO3/movement_data/pickle_data/logsig_distances/distances_{truncation_level}.pkl'
    save_results(logsig_distances, result_path)

if __name__ == "__main__":
    main()
