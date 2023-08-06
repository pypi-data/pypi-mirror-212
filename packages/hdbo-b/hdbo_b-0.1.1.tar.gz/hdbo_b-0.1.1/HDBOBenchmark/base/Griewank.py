from .FunctionBase import BOTorchTestFunction
from botorch.test_functions import Griewank as Griewank_


class Griewank(BOTorchTestFunction):
    def __init__(
        self,
        dim,
        x_scaler=None,
        y_scaler=None,
        auto_init_x_scaler=True,
        auto_init_y_scaler=True,
    ):
        super().__init__(Griewank_(dim=dim), "Griewank", x_scaler, y_scaler)
        self.y_scale = 90 * self.dim
        self.auto_init_scaler(auto_init_x_scaler, auto_init_y_scaler)
