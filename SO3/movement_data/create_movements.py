import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from animation import fetch_animations
from SO3.utils.animation_to_SO3_utils import convert_animation_to_SO3
import numpy as np
import pickle
import os

# 9 movements 
FORWARD_JUMP = {
    "16_05.amc" : {"start":90, "end":220},
    "16_06.amc" : {"start":200, "end":330},
    "16_07.amc" : {"start":200, "end":330},
    "16_09.amc" : {"start":240, "end":370},
    "16_10.amc" : {"start":260, "end":390},
    "13_11.amc" : {"start":190, "end":320},
    "13_13.amc" : {"start":160, "end":290},
    "13_19.amc" : {"start":205, "end":335},
    "13_32.amc" : {"start":125, "end":255},
}

# 9 movements
RUN_JOG = {
    "16_45.amc" : {"start": 0, "end": 130},
    "16_46.amc" : {"start": 0, "end": 130},
    "35_26.amc" : {"start": 0, "end": 130},
    "35_22.amc" : {"start": 0, "end": 130},
    "16_35.amc" : {"start": 0, "end": 130},
    "16_36.amc" : {"start": 0, "end": 130},
    "35_18.amc" : {"start": 0, "end": 130},
    "02_03.amc" : {"start": 0, "end": 130},
    "16_56.amc" : {"start": 0, "end": 130},
}

# 10 movements
WALK = {
    "16_16.amc" : {"start": 0, "end": 130},
    "35_12.amc" : {"start": 0, "end": 130},
    "16_58.amc" : {"start": 0, "end": 130 },
    "35_32.amc" : {"start": 0, "end": 130 },
    "35_11.amc" : {"start": 0, "end": 130 },
    "16_21.amc" : {"start": 0, "end": 130 },
    "16_22.amc" : {"start": 0, "end": 130 },
    "16_15.amc" : {"start": 40, "end": 170 },
    "16_31.amc" : {"start": 40, "end": 170 },
    "16_47.amc" : {"start": 40, "end": 170 },
}

# 9 movements
BOXING = {
    "13_17.amc" : {"start": 30, "end": 160},
    "13_18.amc" : {"start": 30, "end": 160},
    "14_01.amc" : {"start": 40, "end": 170},
    "14_02.amc" : {"start": 40, "end": 170},
    "14_03.amc" : {"start": 80, "end": 210},
    "15_13.amc" : {"start": 80, "end": 210},
    "17_10.amc" : {"start": 80, "end": 210},
    "15_04.amc" : {"start": 22200, "end": 22330},
    "15_05.amc" : {"start": 22400, "end": 22530},
}

# 7 movements
CLIMB_STAIRS = {
    "13_35.amc" : {"start": 200, "end": 330},
    "13_36.amc" : {"start": 230, "end": 360},
    "13_37.amc" : {"start": 220, "end": 350},
    "13_38.amc" : {"start": 220, "end": 350},
    "14_21.amc" : {"start": 220, "end": 350},
    "14_22.amc" : {"start": 220, "end": 350},
    "14_23.amc" : {"start": 220, "end": 350},
}



def set_time_range(curve, time_range) -> np.ndarray:
    start_time, end_time = time_range["start"], time_range["end"]
    return curve[:, start_time:end_time]


def process_file(file_name, time_range) -> dict:
    try:
        skeleton, animation, description = fetch_animations(1, file_name=file_name)
        curve = convert_animation_to_SO3(skeleton, animation)
        curve_segment = set_time_range(curve, time_range)
        return {"curve": curve_segment, "description": description}
    except Exception as e:  # Replace with specific exceptions
        print(f"Error processing file {file_name}: {e}")
        return None

def process_files(file_name_dict) -> dict:
    movements = {}
    for file_name, time_range in file_name_dict.items():
        result = process_file(file_name, time_range)
        if result is not None:
            movements[file_name] = result
    return movements

def save_movements(movements, file_name) -> None:
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'wb') as f:
        pickle.dump(movements, f)

def main():
    file_name_dict = {**FORWARD_JUMP, **RUN_JOG, **WALK, **BOXING, **CLIMB_STAIRS}
    movements = process_files(file_name_dict)
    save_movements(movements, "SO3/movement_data/pickle_data/movements.pkl")

if __name__ == "__main__":
    main()