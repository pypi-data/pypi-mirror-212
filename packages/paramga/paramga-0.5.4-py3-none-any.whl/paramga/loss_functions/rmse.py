import math
import numpy as np


def validate_inputs(X, Y):
    try:
        assert type(X) == np.ndarray
        assert type(Y) == np.ndarray
        assert X.dtype == np.dtype(float)
        assert Y.dtype == np.dtype(float)
        assert X.shape == Y.shape
    except AssertionError as e:
        print(f"""Check input and outputs match.
            type(X): {type(X)}
            type(Y): {type(Y)}
            X.dtype : {X.dtype }
            Y.dtype : {Y.dtype }
            X.shape : {X.shape }

        """)
        raise e


def rmse(
    x: np.ndarray,
    y: np.ndarray,
) -> float:
    """Calcultates the Root Mean Square Error of data, which normalises the data into
    a [0,1] interval on a variable-by-variable basis. Then calculates the RMSE of
    using all data as seperate samples.

    Inputs are a ndarray with shape (n, p) where n is number of variables and p is the population

    Author: Nathan Booth

    Parameters
    ----------
    x: np.ndarray
        expected values with shape (n, p)
    y: np.ndarray
        modelled values with shape (n, p)

    Returns
    -------
    float
        0 -> 1 where 0 is perfect and 1 is noise

    """
    validate_inputs(x, y)

    # Check the data has been normalised?
    # Or nomralise it in the function?

    # Finds the number of predictions we have
    [n, p] = x.shape

    """
    Normalises the data
    Would require some pretreatment for phenology dates
    """
    # Merges data for normalisation and initialised a matrix for normalisation
    merged = np.concatenate((x, y))
    merged_normalised = merged

    # Finds the minimum and maximum of the data variables
    temp_min_vals = np.array([np.nanmin(x[:, i]) for i in range(p)])
    temp_max_vals = np.array([np.nanmax(y[:, i]) for i in range(p)])

    # Calculates the range of the variable and a scales for normalisation
    range_vals = temp_max_vals - temp_min_vals
    norm_scale = 1

    # Finds the maximum value of the variable for scaling into the 0-1 range
    min_vals = temp_min_vals - norm_scale * range_vals
    max_vals = temp_max_vals + norm_scale * range_vals

    for j in range(p):
        if max_vals[j] != min_vals[j]:
            # Calculates coefficients used to normalise data into a 0-1 interval
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

    # Initialises summations to calculate RMSE and ME
    rmse_sum = 0
    me_sum = 0
    for i in range(n):
        for j in range(p):
            # Ignores NaN values
            if not (np.isnan(x[i, j])) and not (np.isnan(y[i, j])):
                # Calculates sum of square errors and sum of errors
                rmse_sum += (x[i, j] - y[i, j]) ** 2
                me_sum += (x[i, j] - y[i, j])
            else:
                pass

    # Calculates RMSE by MSE and ME
    mse = rmse_sum / (n * p)
    rmse = math.sqrt(mse)
    me = me_sum / (n * p)

    return rmse
