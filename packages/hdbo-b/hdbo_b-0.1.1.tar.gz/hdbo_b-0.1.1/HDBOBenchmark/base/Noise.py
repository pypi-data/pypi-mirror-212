import numpy as np
from .FunctionBase import TestFunction


class Noise(TestFunction):
    def __init__(
        self,
        dim,
        x_scaler=None,
        y_scaler=None,
        auto_init_x_scaler=True,
        auto_init_y_scaler=True,
    ):
        super().__init__(dim, "Noise", x_scaler, y_scaler)

        self._min_pt = np.zeros(self.dim)
        self._min_val = 0

    def _evaluate(self, x):  # black-box objective function to minimize
        return np.random.normal()
