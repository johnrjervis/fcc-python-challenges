import numpy as np

def calculate(input_list):
    """Returns a dict containing summary statistics for a 3x3 array constructed from an input list of nine numbers"""
    if (len(input_list) < 9):
        raise ValueError("List must contain nine numbers.")

    arr = np.array(input_list[:9]).reshape(3, 3)
    analyses = {"mean": np.mean, "variance": np.var, "standard deviation": np.std, "max": np.max, "min": np.min, "sum": np.sum}

    return {key: [list(analyses[key](arr, axis=0)), list(analyses[key](arr, axis=1)), analyses[key](input_list[:9])] for key in analyses}
