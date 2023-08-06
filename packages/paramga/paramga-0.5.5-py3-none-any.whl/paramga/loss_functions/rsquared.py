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
            Y.shape : {Y.shape }
        """)
        raise e


def rsquared(X: np.ndarray, Y: np.ndarray, NAN_SENS: float = 2.0, validate: bool = False) -> float:
    """Calculate the rsquared error value of 2x (Nr*Np) arrays

    Author: @nbooth99

    Parameters
    ----------
    X : np.ndarray
        _description_
    Y : np.ndarray
        _description_
    NAN_SENS : float, optional
        _description_, by default 2.0
    validate : bool, optional
        _description_, by default False

    Returns
    -------
    float
        _description_

    """
    if validate:
        validate_inputs(X, Y)

    [n, p] = X.shape

    xbar = np.nanmean(X.flatten())

    r_squared = 0

    ssr = 0
    sst = 0

    for j in range(p):

        for i in range(n):
            if np.isnan(X[i, j]):
                # Observed is NaN so we skip this value
                pass
            elif np.isnan(Y[i, j]):
                # modelled is NaN so we set high error
                ssr += (X[i, j] - xbar*NAN_SENS) ** 2
                # ssr += (X[i, j] - xbar[j]) ** 2
                sst += (X[i, j] - xbar) ** 2
            elif not (np.isnan(X[i, j])) and not(np.isnan(Y[i, j])):
                ssr += (X[i, j] - Y[i, j]) ** 2
                sst += (X[i, j] - xbar) ** 2
    if not math.isclose(sst, 0, abs_tol=0.00001):
        r_squared = 1 - (ssr/sst)
    else:
        if not math.isclose(xbar, 0, abs_tol=0.00001):
            r_squared = 1 - (ssr / xbar)
        else:
            r_squared = 1 - ssr
    loss = -r_squared + 1
    return loss


def rsquared_exp(X: np.ndarray, Y: np.ndarray) -> float:
    """Calculate the rsquared_exp

    Author: @nbooth99

    Parameters
    ----------
    X : np.ndarray
        _description_
    Y : np.ndarray
        _description_

    Returns
    -------
    float
        _description_

    """
    validate_inputs(X, Y)
    r_squared = -(1 + rsquared(X, Y))
    loss = 1 - math.exp(r_squared - 1) + math.log(1 - r_squared) if 1 - r_squared > 0 else 0
    return loss


def rsquared_err_func(observed: np.ndarray, modelled: np.ndarray, params: dict, **kwargs):
    observed_float = observed.astype(float)
    output_float = modelled.astype(float)
    return rsquared(observed_float, output_float, **kwargs)
