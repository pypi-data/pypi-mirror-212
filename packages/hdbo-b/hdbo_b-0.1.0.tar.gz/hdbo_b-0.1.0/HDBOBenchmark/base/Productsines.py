import numpy as np
from .FunctionBase import TestFunction


class ProductSines(TestFunction):
    def __init__(
        self,
        dim,
        x_scaler=None,
        y_scaler=None,
        auto_init_x_scaler=True,
        auto_init_y_scaler=True,
    ):
        super().__init__(dim, "ProductSines", x_scaler, y_scaler)

        self._x_bound = np.array([[-np.pi / 2, np.pi / 2]] * self.dim)  # shape(dim, 2)
        self.y_scale = 2
        self._min_pt = np.ones((dim,)) * np.pi / 2
        self._min_val = self._evaluate(self._min_pt)

        self.auto_init_scaler(auto_init_x_scaler, auto_init_y_scaler)

    def _evaluate(self, x):  # black-box objective function to minimize
        prod_f = -1
        for t in x:
            prod_f *= np.sin(t)
        return prod_f
