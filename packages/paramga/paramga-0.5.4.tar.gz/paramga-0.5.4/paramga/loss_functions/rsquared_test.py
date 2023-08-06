import pytest
import numpy as np
from math import isclose
from functools import partial
from paramga.demo import demo_runner, demo_model, demo_best_params, demo_data
from paramga.post_processing.normalize_outputs import scale_outputs
from .rsquared import rsquared, rsquared_err_func, rsquared_exp
from .testing_utils import ErrorFuncTestBase, wrap_cls_fn


class TestRsquaredExp(ErrorFuncTestBase):
    handles_nan = True
    max_val = 5.0
    min_val = -999999999
    target_score = 0.01
    scale_sensativity = 11
    point_sensativity = 40
    intercept = None
    error_fn = wrap_cls_fn(rsquared_exp)


class TestRsquared(ErrorFuncTestBase):
    handles_nan = True
    max_val = 999999999
    min_val = 0.0
    target_score = 0.9
    intercept = None
    error_fn = wrap_cls_fn(rsquared)


class TestRSquared:

    def test_perfect(self):
        out = rsquared(np.ones((3, 2)), np.ones((3, 2)))
        assert out == 0.0

    def test_not_perfect(self):
        out = rsquared(np.ones((3, 2)) * 100, np.ones((3, 2)))
        assert 0.0 < out < 999999


class TestRSquaredImplementation:

    def test_perfect(self):
        observed_data = np.array([demo_model()(demo_best_params(), demo_data(), abc="hello")])
        runner = demo_runner(
            loss_func=partial(rsquared_err_func, observed_data, validate=True),
            process_outputs=lambda o: np.array([o]),
            tolerance=0.0005,
        )
        iteration_state = runner.run().iteration_state
        assert 100 > iteration_state.iterations > 5
        assert iteration_state.best_parameters == demo_best_params()


class TestRSquaredImplementationIssues:
    class TestNormalizedOutputs:
        def test_none_normalised_outputs(self):
            """If the model outputs are not normalised then this error function
            will prioritize the output with the highest value.


            """
            def model(params, data, abc=None):
                return [params['foo'], params['bar']*1000, 10]
            mutation_conf = {
                "foo": {
                    "type": "number",
                    "min": 1,
                    "max": 80,
                    "step": 8,
                },
                "bar": {
                    "type": "number",
                    "min": 1,
                    "max": 80,
                    "step": 8,
                },
            }
            observed_data = np.array([[100, 50000, 10]])
            runner = demo_runner(
                loss_func=partial(rsquared_err_func, observed_data, validate=True),
                mutation_conf=mutation_conf,
                process_outputs=lambda o: np.array([o]),
                func=model,
                tolerance=0.0001,
            ).store_iterations()
            iteration_state = runner.run().iteration_state
            modelled_observed_ratio_foo = abs(1 - iteration_state.outputs[0][0]/observed_data[0][0])
            modelled_observed_ratio_bar = abs(1 - iteration_state.outputs[0][1]/observed_data[0][1])
            assert not isclose(modelled_observed_ratio_foo,
                               modelled_observed_ratio_bar, abs_tol=1e-1)
            assert modelled_observed_ratio_foo > modelled_observed_ratio_bar

        def test_normalised_outputs(self):
            """To resolve this issue we need to know the min and max values of
            each output."""
            def model(params, data, abc=None):
                return [params['foo'], params['bar']*1000, 10]
            mutation_conf = {
                "foo": {
                    "type": "number",
                    "min": 1,
                    "max": 80,
                    "step": 8,
                },
                "bar": {
                    "type": "number",
                    "min": 1,
                    "max": 80,
                    "step": 8,
                },
            }
            variables = ['a', 'b', 'c']
            variable_scales = {
                "a": {
                    "min": 0,
                    "max": 200,
                },
                "b": {
                    "min": 40000,
                    "max": 60000,
                },
                "c": {
                    "min": 0,
                    "max": 200,
                },
            }
            observed_data = np.array([[100, 50000, 10]])
            _scale_outputs = scale_outputs(variables, variable_scales)
            observed_data_normalised = _scale_outputs(observed_data)
            assert all(0 < o < 1 for o in observed_data_normalised[0])
            runner = demo_runner(
                loss_func=partial(rsquared_err_func, observed_data_normalised, validate=True),
                mutation_conf=mutation_conf,
                process_outputs=lambda o: _scale_outputs(np.array([o])),
                func=model,
                tolerance=0.0001,
            ).store_iterations()
            iteration_state = runner.run().iteration_state
            modelled_observed_ratio_foo = abs(1 - iteration_state.outputs[0][0]/observed_data[0][0])
            modelled_observed_ratio_bar = abs(1 - iteration_state.outputs[0][1]/observed_data[0][1])
            assert isclose(modelled_observed_ratio_foo, modelled_observed_ratio_bar, abs_tol=1e-1)
