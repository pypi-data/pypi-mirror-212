import numpy as np
from paramga.run import Runner


def demo_state():
    return {
        "foo": 10,
        "bar": 360,
    }


def demo_conf():
    return {
        "foo": {
            "type": "number",
            "min": 1,
            "max": 80,
            "step": 8,
        }
    }


def demo_model():
    def model(params, data, abc=None):
        assert abc  # example kwarg
        return np.array([d * params['foo'] for d in data])
    return model


def demo_process_outputs():
    def process_outputs(outputs):
        return outputs + 10
    return process_outputs


def demo_loss_function():
    def loss_function(output, params):
        return abs(params['bar'] - sum(output) + 40)
    return loss_function


def demo_data():
    return [1, 2, 3, 3]


def demo_best_params():
    return {
        "foo": 40,
        "bar": 360,
    }


def demo_kwargs():
    return dict(abc=123)


def demo_runner(**kwargs):
    default_args = dict(
        param_base=demo_state(),
        mutation_conf=demo_conf(),
        func=demo_model(),
        loss_func=demo_loss_function(),
        input_data=demo_data(),
        process_outputs=demo_process_outputs(),
        func_kwargs=demo_kwargs(),
        population=8,
        max_iterations=100,
        tolerance=0.05,
    )
    return Runner(**{**default_args, **kwargs})
