import pytest
import numpy as np
from unittest.mock import MagicMock
from paramga.random_helpers import set_seed
from paramga.run import IterationState, get_outputs_parallel, iteration, run, run_iterator
from paramga.demo import(
    demo_state,
    demo_conf,
    demo_model,
    demo_loss_function,
    demo_data,
    demo_best_params,
    demo_kwargs,
    demo_runner,
)

__module_loc__ = 'paramga.run'


class TestIteration:

    class TestUnitTests:

        @pytest.fixture(autouse=True)
        def _setup(self, mocker):
            # default args
            self.population = 10
            self.parameters = [MagicMock() for _ in range(self.population)]
            self.iteration_state = IterationState(
                self.parameters,
                self.parameters,
                loss=999999,
                lowest_loss=99999,
            )
            self.mock_func_result = 99
            self.mock_func_result_processed = 99.9
            self.func = MagicMock(return_value=self.mock_func_result)
            self.loss_func = MagicMock(side_effect=lambda out,
                                       param: 0 if param == self.parameters[0] else 1)
            self.mutation_conf = {}
            self.input_data = []
            self.parallel = False

            # Mocks
            self.mutated_params = MagicMock()
            self.crossover_params = MagicMock()
            self.mock_output_postprocess = MagicMock(return_value=self.mock_func_result_processed)

            self.mock_mutate_param_state = mocker.patch(
                __module_loc__ + '.mutate_param_state', return_value=self.mutated_params)

            self.mock_param_crossover = mocker.patch(
                __module_loc__ + '.param_crossover', return_value=self.crossover_params)

        def _default_run(self, **kwargs):
            default_args = dict(
                iteration_state=self.iteration_state,
                func=self.func,
                loss_func=self.loss_func,
                population=self.population,
                mutation_conf=self.mutation_conf,
                input_data=self.input_data,
                process_outputs=self.mock_output_postprocess,
                parallel=self.parallel,
            )
            _kwargs = {
                **default_args,
                **kwargs,
            }
            return set_seed(1)(iteration)(**_kwargs)

        def test_runs_ok(self):
            self._default_run()

        def test_runs_ok_parallel(self):
            self._default_run(parallel=True)

        def test_model_func_is_called(self):
            self._default_run()
            assert self.func.call_count == self.population
            for params in self.parameters:
                self.func.assert_any_call(
                    params,
                    self.input_data,
                )

        def test_output_post_process_called(self):
            self._default_run()
            assert self.mock_output_postprocess.call_count == self.population
            self.mock_output_postprocess.assert_any_call(
                self.mock_func_result,
            )

        def test_loss_func_is_called(self):
            self._default_run()
            assert self.loss_func.call_count == self.population
            self.loss_func.assert_called_with(
                self.mock_func_result_processed,
                self.parameters[-1],
            )

        def test_param_crossover_called(self):
            self._default_run()
            assert self.mock_param_crossover.call_count == self.population
            self.mock_param_crossover.assert_any_call(
                self.parameters[0],
                self.parameters[0],
            )

        def test_should_call_mutate_param_state(self):
            self._default_run()
            assert self.mock_mutate_param_state.call_count == self.population

        def test_returns_updated_state(self):
            out = self._default_run()
            assert out.iterations == self.iteration_state.iterations + 1
            assert out.parameters == [self.mutated_params for _ in range(self.population)]

        def test_should_pass_extra_model_args_to_model_run(self):
            self.func_kwargs = {
                "a": 123,
            }
            self._default_run(func_kwargs=self.func_kwargs)
            assert self.func.call_count == self.population
            for params in self.parameters:
                self.func.assert_any_call(
                    params,
                    self.input_data,
                    **self.func_kwargs,
                )

    class TestFuncTests:

        @pytest.fixture(autouse=True)
        def _setup(self, mocker):
            # default args
            self.population = 10
            self.parameters = [{"foo": 1, "bar": 1} for _ in range(self.population)]
            self.iteration_state = IterationState(
                self.parameters,
                self.parameters,
                loss=999999,
                lowest_loss=99999,
            )
            self.func = lambda params, data: params['foo'] * 2 + params['bar'] * 4
            self.loss_func = lambda output, params: output - 42
            self.max_foo = 10
            self.mutation_conf = {
                "foo": {
                    "type": "float",
                    "min": 1,
                    "max": self.max_foo,
                    "step": 0.1,
                },
                "bar": {
                    "type": "number",
                    "min": 1,
                    "max": 20,
                    "step": 1,
                },
            }
            self.input_data = []
            self.parallel = False

        def _default_run(self, **kwargs):
            default_args = dict(
                iteration_state=self.iteration_state,
                func=self.func,
                loss_func=self.loss_func,
                population=self.population,
                mutation_conf=self.mutation_conf,
                input_data=self.input_data,
                parallel=self.parallel,
            )
            _kwargs = {
                **default_args,
                **kwargs,
            }
            return set_seed(1)(iteration)(**_kwargs)

        def test_run_without_error(self):
            self._default_run()

        def test_should_have_reduced_loss(self):
            out = self._default_run()
            assert out.loss < self.iteration_state.loss

        def test_should_have_mutated_parameters(self):
            out = self._default_run()
            assert len(out.parameters) == len(self.parameters)
            assert out.parameters != self.parameters
            assert all(o['foo'] < self.max_foo for o in out.parameters)

        def test_can_handle_different_loss_functions(self):
            self._default_run(loss_func=lambda *args, **kwargs: 99)
            self._default_run(loss_func=lambda *args, **kwargs: -100)


class TestRun:

    def demo_state(self):
        return {
            "foo": 10,
            "bar": 360,
        }

    def demo_conf(self):
        return {
            "foo": {
                "type": "number",
                "min": 1,
                "max": 80,
                "step": 8,
            }
        }

    def demo_model(self):
        def model(params, data):
            return sum(data) * params['foo']
        return model

    def demo_process_outputs_func(self):
        def process_outputs(outputs):
            return outputs + 100
        return process_outputs

    def demo_loss_function(self):
        def loss_function(output, params):
            return abs(params['bar'] - output)
        return loss_function

    def demo_data(self):
        return [1, 2, 3, 3]

    def demo_best_params(self):
        return {
            "foo": 40,
            "bar": 360,
        }

    def _default_run(self, **kwargs):
        default_args = dict(
            param_base=self.demo_state(),
            mutation_conf=self.demo_conf(),
            func=self.demo_model(),
            loss_func=self.demo_loss_function(),
            input_data=self.demo_data(),
            population=8,
            tolerance=0.05,
            max_iterations=100,
            verbose=False,
            parallel=False,
        )
        _kwargs = {**default_args, **kwargs}
        return set_seed(1)(run)(**_kwargs)

    def test_simple_run(self):
        iteration_state = self._default_run()
        assert 100 > iteration_state.iterations > 5
        assert iteration_state.best_parameters == self.demo_best_params()

    def test_limited_by_max_iterations(self):
        tolerance = 0.00000001
        iteration_state = self._default_run(max_iterations=5, tolerance=tolerance)
        assert iteration_state.loss > tolerance
        assert iteration_state.iterations == 5
        assert iteration_state.best_parameters != self.demo_best_params()

    def test_running_in_parallel(self):
        tolerance = 0.0001
        iteration_state = self._default_run(
            tolerance=tolerance,
            parallel=True,
        )

        assert 100 > iteration_state.iterations > 5
        assert iteration_state.loss < tolerance
        assert iteration_state.best_parameters == self.demo_best_params()


class TestRunCls:

    def test_simple_run(self):
        runner = demo_runner()
        iteration_state = runner.run().iteration_state
        assert 100 > iteration_state.iterations > 5
        assert iteration_state.best_parameters == demo_best_params()

    def test_limited_by_max_iterations(self):
        tolerance = 0.00000001

        runner = demo_runner(
            tolerance=tolerance,
            max_iterations=5,
        )

        iteration_state = runner.run().iteration_state
        assert iteration_state.loss > tolerance
        assert iteration_state.iterations == 5
        assert iteration_state.best_parameters != demo_best_params()

    def test_best_parameters_is_best_from_current_set(self):
        tolerance = 0.00000001
        runner = demo_runner(
            tolerance=tolerance,
            max_iterations=5,
        )

        iteration_state = runner.run().iteration_state
        assert iteration_state.loss > tolerance
        assert iteration_state.iterations == 5
        assert iteration_state.best_parameters != demo_best_params()

    def test_running_in_parallel(self):
        tolerance = 0.00000001
        runner = demo_runner(
            tolerance=tolerance,
            parallel=True,
        )

        iteration_state = runner.run().iteration_state
        assert 100 > iteration_state.iterations > 5
        assert iteration_state.loss <= tolerance
        assert iteration_state.loss == 0
        assert iteration_state.best_parameters == demo_best_params()

    def test_run_as_iterator(self):
        tolerance = 0.05
        runner = demo_runner(
            tolerance=tolerance,
            parallel=True,
        )

        for iteration_state in iter(runner):
            pass
        assert 100 > iteration_state.iterations > 5
        assert iteration_state.loss <= tolerance

    def test_can_store_iteration_data(self):
        tolerance = 0.05
        runner = demo_runner(
            tolerance=tolerance,
            parallel=True,
        )
        runner.store_iterations()
        final_state = runner.run().iteration_state
        assert len(runner.history) == final_state.iterations + 1

    # def test_should_store_parameters_in_order(self):
    #     tolerance = 0.05
    #     runner = Runner(
    #         demo_state(),
    #         demo_conf(),
    #         demo_model(),
    #         demo_loss_function(),
    #         demo_data(),
    #         max_iterations=100,
    #         tolerance=tolerance,
    #         parallel=True,
    #     )
    #     runner.store_iterations()
    #     runner.run().iteration_state
    #     assert runner.initial_parameters == runner.history[0].parameters

    def test_should_plot_loss(self):
        tolerance = 0.001
        runner = demo_runner(
            tolerance=tolerance,
            parallel=True,
        )
        runner = demo_runner(
            tolerance=tolerance,
        )
        runner.store_iterations()
        runner.run()
        runner.plot()

    def test_should_plot_param(self):
        tolerance = 0.001
        runner = demo_runner(
            tolerance=tolerance,
        )
        runner.store_iterations()
        runner.run()
        runner.plot_param('foo')

    def test_should_plot_param_compare(self):
        tolerance = 0.001
        runner = demo_runner(
            tolerance=tolerance,
        )
        runner.store_iterations()
        runner.run()
        runner.plot_param_compare('foo', 'bar')

    def test_should_plot_observed_compare(self):
        tolerance = 0.001
        runner = demo_runner(
            tolerance=tolerance,
        )
        runner.store_iterations()
        runner.run()
        print(runner.func(runner.iteration_state.best_parameters, runner.input_data, **demo_kwargs()))
        observed_data = np.array(runner.input_data)
        runner.plot_compare_with_observed(observed_data)

    def test_setting_seed_makes_results_reproducable(self):
        runner = demo_runner(seed=0, max_iterations=3)
        runner.store_iterations()
        runner.run()
        assert runner.iteration_state.lowest_loss == 198
        runner = demo_runner(seed=1, max_iterations=3)
        runner.store_iterations()
        runner.run()
        assert runner.iteration_state.lowest_loss != 198
        assert runner.iteration_state.lowest_loss == 108

    def test_setting_seed_makes_results_reproducable_parallel(self):
        runner = demo_runner(seed=0, max_iterations=3, parallel=True)
        runner.store_iterations()
        runner.run()
        assert runner.iteration_state.lowest_loss == 198
        runner = demo_runner(seed=1, max_iterations=3)
        runner.store_iterations()
        runner.run()
        assert runner.iteration_state.lowest_loss != 198
        assert runner.iteration_state.lowest_loss == 108

    def test_can_get_initial_output(self):
        tolerance = 0.00000001
        runner = demo_runner(
            tolerance=tolerance,
            max_iterations=100,
        )
        runner.store_iterations()
        runner.run()

        initial_output = runner.get_initial_model_output()
        expected_initial_output = demo_model()(demo_state(), demo_data(), **demo_kwargs())
        assert len(initial_output) == len(expected_initial_output)
        for a, b in zip(initial_output, expected_initial_output):
            assert a == b

    def test_can_get_best_output(self):
        tolerance = 0.00000001
        runner = demo_runner(
            tolerance=tolerance,
            max_iterations=100,
        )
        runner.store_iterations()
        runner.run()

        best_output = runner.get_best_model_output()
        expected_best_output = demo_model()(demo_best_params(), demo_data(), **demo_kwargs())
        assert len(best_output) == len(expected_best_output)
        for a, b in zip(best_output, expected_best_output):
            assert a == b

    def test_outputs_should_be_normalized_before_error_function(self):
        runner = demo_runner()
        iteration_state = runner.run().iteration_state
        assert 100 > iteration_state.iterations > 5
        assert iteration_state.best_parameters == demo_best_params()

    @pytest.mark.skip(reason="Not implemented")
    def test_can_split_test_and_train_data(self):
        tolerance = 0.00000001
        runner = demo_runner(
            tolerance=tolerance,
            max_iterations=100,
            test_train_split=0.5,
        )
        runner.store_iterations()
        runner.run()

        best_output = runner.get_best_model_output()
        expected_best_output = demo_model()(demo_best_params(), demo_data(), **demo_kwargs())
        assert len(best_output) == len(expected_best_output)
        for a, b in zip(best_output, expected_best_output):
            assert a == b


class TestRunParallelIterator:

    @set_seed(1)
    def test_simple_run(self):
        model = run_iterator(
            demo_state(),
            demo_conf(),
            demo_model(),
            demo_loss_function(),
            demo_data(),
            max_iterations=100,
            tolerance=0.005,
            verbose=True,
            func_kwargs=demo_kwargs(),
        )
        iterations_state = next(model)
        assert iterations_state.iterations == 1
        assert iterations_state.loss < 99999


class TestGetOutputsParallel:
    def test_get_outputs_parallel(self):
        from time import sleep
        input_args = [
            [0, 0.1],
            [1, 0.4],
            [2, 0.3],
            [3, 0.4],
        ]

        def func(i, t, j=0, k=1):
            sleep(t)
            return i, t, j+k
        func_kwargs = {"j": 98, "k": 1}
        # func_kwargs = {}
        outputs = get_outputs_parallel(func, input_args, func_kwargs)
        expected_outputs = [
            [i, t, 99] for i, t in input_args
        ]
        np.testing.assert_array_equal(outputs, expected_outputs)

    def test_should_catch_errors(self):
        from time import sleep
        input_args = [
            [0, 3],
            [1, 3],
            [2, 3],
            [3, 3],
        ]

        def func(i, t, j=0, k=1):
            sleep(t)
            raise Exception("RANDOM_ERROR_IN_PROCESS")

        func_kwargs = {}
        with pytest.raises(Exception) as e:
            get_outputs_parallel(func, input_args, func_kwargs, TIMEOUT=1)

        assert "Model run multiprocessing failed" in str(e)
        assert "RANDOM_ERROR_IN_PROCESS" in str(e)
        # assert "Model run multiprocessing failed" in str(e)
