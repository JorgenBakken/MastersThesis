import pickle

def load_movements(file_path = 'results/movements.pkl') -> dict:
    with open(file_path, 'rb') as f:
        return pickle.load(f)
    
def tictoc(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time elapsed for {func.__name__}: {end - start}")
        return result
    return wrapper
    
