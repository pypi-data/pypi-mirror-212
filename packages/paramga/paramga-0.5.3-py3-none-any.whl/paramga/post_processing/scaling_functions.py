from typing import Callable, List
import numpy as np
from functools import partial

ScalingFunc = Callable[[np.ndarray], np.ndarray]


def scaling_function(x: np.ndarray, y: np.ndarray) -> list:
    """
        Scales the input variables into a 0-1 range based on the range of the expected values

        Inputs are an ndarray with shape (n, p) where n is the population and p is the number of variables

        Author: Nathan Booth

        Parameters
        ----------
        x: np.ndarray
            expected value with shape (n, p)
        y: np.ndarray
            modelled value with shape (n, p)

        Returns
        -------
        list
            two arrays of shape (n, p) representing the input variables scaled into a 0-1 range
    """
    assert type(x) == np.ndarray
    assert type(y) == np.ndarray
    assert x.shape == y.shape

    [n, p] = x.shape

    # Merges data for normalisation and initialised a matrix for normalisation
    merged = np.concatenate((x, y))
    merged_normalised = np.zeros(shape=merged.shape)

    # Finds the minimum and maximum of the data variables
    temp_min_vals = np.array([np.nanmin(x[:, i]) for i in range(p)])
    temp_max_vals = np.array([np.nanmax(x[:, i]) for i in range(p)])

    # Calculates the range of the variable and a scale for normalisation
    col_range = temp_max_vals - temp_min_vals
    range_scale = 1

    # Finds the minimum and maximum value of the variable for scaling into the 0-1 range
    min_vals = temp_min_vals - range_scale * col_range
    max_vals = temp_max_vals + range_scale * col_range

    for j in range(p):
        if max_vals[j] != min_vals[j]:
            # Calculates coefficients used to normalise data into the 0-1 interval
            b = -min_vals[j]
            a = 1 / (max_vals[j] - min_vals[j])
            for i in range(2 * n):
                # Normalises the data
                merged_normalised[i, j] = a * (merged[i, j] + b)
        else:
            for i in range(2 * n):
                merged_normalised[i, j] = merged[i, j]

    # Separates the data into the modelled and expected data
    x_normalised = merged_normalised[:n, :]
    y_normalised = merged_normalised[n:, :]

    assert x_normalised.shape == x.shape
    assert y_normalised.shape == y.shape
    x = x_normalised
    y = y_normalised

    return x, y

def alt_scaling_func(min_values, offsets, data_range, outputs):
    outputs_offset = (outputs.astype(float).transpose() - offsets).transpose()
    a = ((outputs_offset - min_values) / data_range).clip(0,1).astype(float)
    return a



def get_alt_scaling_func(
    input_data: np.ndarray,
    offsets: List[int],
) -> ScalingFunc:
    try:
        # get the min and max value for each key date

        min_values = 0.8 * np.nanmin((input_data.astype(float).transpose()-offsets).transpose(), axis=0) # np.array([0, 50, 100])
        max_values = 1.2 * np.nanmax((input_data.astype(float).transpose()-offsets).transpose(), axis=0) # np.array([30, 110, 150])
        data_range = max_values - min_values
        return partial(
            alt_scaling_func,
            min_values=min_values,
            offsets=offsets,
            data_range=data_range,
        )
    except TypeError as e:
        print(e)
        raise ValueError('Failed to get scaling function. Check input data does not contain None values.')
    except Exception as e:
        print(input_data.shape)
        print(offsets)
        raise e

def get_skip_scaling_func() -> ScalingFunc:
    def _scaling_func(values):
        return values
    return _scaling_func