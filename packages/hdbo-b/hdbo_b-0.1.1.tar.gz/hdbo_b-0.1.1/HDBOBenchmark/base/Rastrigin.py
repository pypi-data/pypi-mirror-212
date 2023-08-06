from .FunctionBase import BOTorchTestFunction
from botorch.test_functions import Rastrigin as Rastrigin_


class Rastrigin(BOTorchTestFunction):
    def __init__(
        self,
        dim,
        x_scaler=None,
        y_scaler=None,
        auto_init_x_scaler=True,
        auto_init_y_scaler=True,
    ):
        super().__init__(Rastrigin_(dim=dim), "Rastrigin", x_scaler, y_scaler)
        self.y_scale = 40 * self.dim
        self.auto_init_scaler(auto_init_x_scaler, auto_init_y_scaler)
