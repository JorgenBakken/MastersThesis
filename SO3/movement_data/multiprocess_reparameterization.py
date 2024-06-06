import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import multiprocessing
import time

from SO3.movement_data.calculate_reparameterized_distance import reparameterized_distance
from my_help_functions import tictoc
from SO3.utils.io_utils import load_movements, save_results


def operation(id_1, id_2, matrix_1, matrix_2, depth) -> float:
    if id_1 == id_2:
        return 0.0
    return reparameterized_distance(matrix_1, matrix_2, depth).distance

def worker(args) -> tuple:
    id_1, id_2, value_1, value_2, depth = args

    print(f"Comparing {id_1} and {id_2}")
    result = operation(id_1, id_2, value_1["curve"], value_2["curve"], depth)
    print(f"Done comparing {id_1} and {id_2}")

    return (id_1, id_2, result)

@tictoc
def multiprocess_comparisons(movements, file_path, depth, leq):
    num_cores = multiprocessing.cpu_count()
    print(f'Number of CPU cores: {num_cores}')

    pool = multiprocessing.Pool(num_cores)

    tasks = []
    if leq:
        for key_1, value_1 in movements.items():
            for key_2, value_2 in movements.items():
                if key_1 <= key_2:
                    tasks.append((key_1, key_2, value_1, value_2, depth))
    else:
        print("Need to implement this")
        # Implement your logic for when leq is False

    results = pool.map(worker, tasks)

    pool.close()
    pool.join()

    save_results(results, file_path)

def main():
    movements = load_movements()

    depth = 10
    print(f"Solving for depth {depth}")
    result_path = f'SO3/movement_data/pickle_data/reparameterized_distances/distances_{depth}.pkl'
    multiprocess_comparisons(movements, result_path, depth, leq = True)
    print(f"Done with depth {depth}")

    # depth = 4
    # print(f"Solving for depth {depth}")
    # result_path = f'SO3/movement_data/pickle_data/reparameterized_distances/distances_{depth}.pkl'
    # multiprocess_comparisons(movements, result_path, depth, leq = True)
    # print(f"Done with depth {depth}")

    # movement1 = movements["16_15.amc"]["curve"] 
    # movement2 = movements["16_31.amc"]["curve"] 
    # movement3 = movements["16_56.amc"]["curve"] 

    # print(movement1.shape)
    # print(movement2.shape)
    # print(movement3.shape)

    # import time 

    # print(f"Full data set ##########################################################")
    # depth = 5
    # start = time.time() 
    # rep_dist = reparameterized_distance(movement1[:,:170], movement2[:,:170], depth)
    # print(rep_dist.distance)
    # print(f"Time elapsed: {time.time() - start}")

    # start = time.time()
    # rep_dist = reparameterized_distance(movement1[:,:170], movement3[:,:170], depth)
    # print(rep_dist.distance)
    # print(f"Time elapsed: {time.time() - start}")

    # print(f"Reduced data set ##########################################################")
    # depth = 10
    # start = time.time() 
    # rep_dist = reparameterized_distance(movement1, movement2, depth)
    # print(rep_dist.distance)
    # print(f"Time elapsed: {time.time() - start}")

    # start = time.time()
    # rep_dist = reparameterized_distance(movement1[:,:130], movement3[:,:130], depth)
    # print(rep_dist.distance)
    # print(f"Time elapsed: {time.time() - start}")


if __name__ == "__main__":
    main()
