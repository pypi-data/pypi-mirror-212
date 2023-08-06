import numpy as np
from typing import List, Dict, TypedDict


class OutputVariableMetaData(TypedDict):
    min: float
    max: float


def scale_variable(observed_variable: float, min_val: float, max_val: float, nan_val: float = None) -> float:
    """Scale variable to range.

    Parameters
    ----------
    observed_variable : float
        Input variable
    min_val : float
        Min val
    max_val : float
        Max val
    nan_val : float, optional
        If this is not None then values outside range will have this value, by default None

    Returns
    -------
    float
        normalized value

    Raises
    ------
    Exception
        _description_
    """
    if max_val == min_val:
        raise Exception("Division by zero error: Maximum and Minimum values are equal")
    return (observed_variable - min_val) / (max_val - min_val)


def scale_outputs(variables: List[str], variable_scales: Dict[str, OutputVariableMetaData]):
    _variables = [v for v in variables if v in variable_scales]
    assert all([variable_scales[k]['min'] < variable_scales[k]['max'] for k in _variables]
               ), "Check that all min and max values in output variable meta data are correct"

    def _scale_outputs(model_outputs: np.ndarray, params=None) -> np.ndarray:

        scales = [[variable_scales[k]['min'], variable_scales[k]['max'],
                   variable_scales[k].get('nan', None)] for k in _variables]
        scaled_modelled = np.array([scale_variable(model_outputs[:, i], temp_min, temp_max, temp_nan) for i, [
            temp_min, temp_max, temp_nan] in enumerate(scales)]).transpose()
        return scaled_modelled

    return _scale_outputs
