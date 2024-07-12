from numpy.typing import NDArray
import numpy as np

def np_concat(*args: float | int | str | NDArray) -> NDArray:
    processed_args = []
    for arg in args:
        if isinstance(arg, (int, float, str)):
            processed_args.append(np.array([arg]))
        elif isinstance(arg, np.ndarray):
            processed_args.append(arg)
        else:
            raise TypeError(f"Unsupported type: {type(arg)}. Expected int, float, or NDArray.")
    
    return np.concatenate(processed_args)
