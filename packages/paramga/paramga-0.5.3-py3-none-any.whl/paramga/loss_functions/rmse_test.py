from .rmse import rmse
from .testing_utils import ErrorFuncTestBase, wrap_cls_fn


class TestRmse(ErrorFuncTestBase):
    handles_nan = False
    max_val = 1.0
    min_val = 0.0
    target_score = 0.9
    error_fn = wrap_cls_fn(rmse)
