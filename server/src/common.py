import numpy as np


def nan_to_none(value):
    if value is np.nan:
        return None

    return value
