import numpy as np
from .FunctionBase import TestFunction


class Sphere(TestFunction):
    def __init__(
        self,
        dim,
        x_scaler=None,
        y_scaler=None,
        auto_init_x_scaler=True,
        auto_init_y_scaler=True,
    ):
        super().__init__(dim, "Sphere", x_scaler, y_scaler)

        self._x_bound = np.array([[-5, 5]] * self.dim)  # shape(dim, 2)
        self.y_scale = 25 * self.dim
        self._min_pt = np.zeros(self.dim)
        # self._min_val = self._evaluate(self._min_pt)
        self._min_val = 0

        self.auto_init_scaler(auto_init_x_scaler, auto_init_y_scaler)

    def _evaluate(self, x: np.ndarray):  # black-box objective function to minimize
        y = np.power(x[: self.dim], 2).sum()
        return y
