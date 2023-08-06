import pytest
import numpy as np
from math import isclose
from sklearn.linear_model import LinearRegression
from paramga.post_processing.scaling_functions import scaling_function


def wrap_cls_fn(fn):
    def _inner(self, *args, **kwargs):
        return fn(*args, **kwargs)
    return _inner


def get_coeff_and_intercept(x, y):
    X = np.expand_dims(np.array(x), axis=1)
    y = np.array(y)
    reg = LinearRegression().fit(X, y)
    reg.coef_, reg.intercept_
    return reg.coef_[0], reg.intercept_, reg.score(X, y)


class InputDataModifiers:
    @staticmethod
    def noise(shape, i, x, y, scale, error_fn):
        np.random.seed(0)
        r = ((np.random.rand(np.product(shape)) - 0.5) * i).reshape(shape)
        x_r = x + (r * scale)
        loss = error_fn(y, x_r)
        return loss

    @staticmethod
    def translate(shape, i, x, y, scale, error_fn):
        r = i
        x_r = x + (r * scale)
        loss = error_fn(y, x_r)
        return loss

    @staticmethod
    def drop(shape, i, x, y, scale, error_fn):
        np.random.seed(0)
        for j in range(shape[0]):
            for k in range(shape[0]):
                if j == k:
                    y[j, k] = np.nan

        r = ((np.random.rand(np.product(shape)) - 0.5) * i).reshape(shape)
        x_r = x + (r * scale)
        loss = error_fn(y, x_r)
        return loss

    @staticmethod
    def drop(shape, i, x, y, scale, error_fn):
        np.random.seed(0)
        for j in range(shape[0]):
            for k in range(shape[0]):
                if j == k:
                    y[j, k] = 99999

        r = ((np.random.rand(np.product(shape)) - 0.5) * i).reshape(shape)
        x_r = x + (r * scale)
        loss = error_fn(y, x_r)
        return loss


class ErrorFuncTestBase:
    error_fn = None
    scaling_fn = wrap_cls_fn(scaling_function)
    intercept = 0
    scale_sensativity = 0
    point_sensativity = 0

    def test_should_return_0_value_when_inputs_match(self):
        if self.min_val != 0.0:
            return
        example_x = np.random.randint(0, 10, 9).reshape(3, 3)
        example_y = np.copy(example_x)
        [scaled_x, scaled_y] = self.scaling_fn(example_x, example_y)

        err = self.error_fn(scaled_x, scaled_y)
        assert err == 0.0

    def test_should_have_none_zero_value_when_x_and_y_differ(self):
        example_x = np.random.randint(0, 10, 9).reshape(3, 3)
        example_y = np.ones(example_x.shape)
        [scaled_x, scaled_y] = self.scaling_fn(example_x, example_y)
        err = self.error_fn(scaled_x, scaled_y)
        assert err != 0

    def test_should_have_none_zero_value_when_y_is_noise(self):
        example_x = np.random.randint(0, 10, 9).reshape(3, 3)
        example_y = np.random.randint(0, 10, example_x.size).reshape(example_x.shape)
        [scaled_x, scaled_y] = self.scaling_fn(example_x, example_y)
        err = self.error_fn(scaled_x, scaled_y)
        assert err != 0

    def test_getting_closer_to_perfect_reduces_error(self):
        np.random.seed(0)
        example_x = np.random.randint(0, 10, 9).reshape(3, 3)
        example_y = np.copy(example_x)
        example_y[0, 0] = example_x[0, 0] + 5000
        [scaled_x, scaled_y] = self.scaling_fn(example_x, example_y)
        err_1_scaled = self.error_fn(scaled_x, scaled_y)
        example_y[0, 0] = example_x[0, 0] + 2000
        [scaled_x, scaled_y] = self.scaling_fn(example_x, example_y)
        err_2_scaled = self.error_fn(scaled_x, scaled_y)
        example_y[0, 0] = example_x[0, 0] + 2
        [scaled_x, scaled_y] = self.scaling_fn(example_x, example_y)
        err_3_scaled = self.error_fn(scaled_x, scaled_y)
        example_y[0, 0] = example_x[0, 0] + 1
        [scaled_x, scaled_y] = self.scaling_fn(example_x, example_y)
        err_4_scaled = self.error_fn(scaled_x, scaled_y)
        assert err_4_scaled < err_3_scaled < err_2_scaled < err_1_scaled

    @pytest.mark.parametrize('scale', [10, 100, 200])
    @pytest.mark.parametrize('shape', [(3, 3), (9, 9)])
    @pytest.mark.parametrize('point_count', [10, 200])
    @pytest.mark.parametrize('modifier_fn', [
        InputDataModifiers.translate,
        InputDataModifiers.noise,
        InputDataModifiers.drop,
    ])
    def test_loss_function_should_increase_loss(self, scale, shape, point_count, modifier_fn):
        if scale < self.scale_sensativity:
            # some models are less sensative at small scales
            return
        if point_count < self.point_sensativity:
            return
        observed_data = np.linspace(0, 200, np.product(shape)).reshape(shape)
        modelled_data = observed_data
        loss_values = []
        i_vals = np.linspace(0, 1, point_count)
        loss_values = [modifier_fn(shape, i, modelled_data, observed_data,
                                   scale, self.error_fn) for i in i_vals]

        # Assert that the gradient of a linear regression is positive
        grad, intercept, score = get_coeff_and_intercept(i_vals, loss_values)
        assert grad > 0
        assert isclose(intercept, self.intercept,
                       abs_tol=1e-1) if self.intercept is not None else True
        assert score > self.target_score
        assert max(loss_values) <= self.max_val
        assert min(loss_values) >= self.min_val

    def test_nan_a(self):
        if self.handles_nan:
            x = np.array([[94, 174, 217], [94, 174, 223], [127, 180, 216]]).astype(float)
            y = np.array([[96, 133, np.nan], [96, 133, np.nan], [
                         np.nan, np.nan, np.nan]]).astype(float)
            e = self.error_fn(x, y)
            assert e > 0.0

    def test_nan_all_nan(self):
        if self.handles_nan:
            x = np.array([[94, 174, 217], [94, 174, 223], [127, 180, 216]]).astype(float)
            y = np.array([[np.nan for _ in range(3)] for _ in range(3)]).astype(float)
            e = self.error_fn(x, y)
            assert e > 0.0

    def test_nan_all_nan_a(self):
        if self.handles_nan:
            x = np.array([[94, 174, 217], [94, 174, 223], [127, 180, 216]]).astype(float)
            y = np.array([[np.nan for _ in range(3)] for _ in range(3)]).astype(float)
            e_a = self.error_fn(x, y)
            y[0, 0] = x[0, 0]
            e_b = self.error_fn(x, y)
            assert e_b < e_a

    def test_increasing_nan_should_increase_error(self):
        if self.handles_nan:
            x = np.array([[94, 174, 217], [94, 174, 223], [127, 180, 216]]).astype(float)
            y = np.copy(x)

            # perfect match
            e_a = self.error_fn(x, y)
            # assert e_a == 0.0

            # perfect match with single NaN
            y[0, 0] = np.nan
            y[0, 2] = np.nan
            e_b = self.error_fn(x, y)
            assert e_a < e_b

            # replace nan with noise
            y = np.array([[96, 133, 99999], [96, 133, 99999], [9999, 99999, 99999]]).astype(float)
            e_c = self.error_fn(x, y)

            assert e_a < e_b < e_c
