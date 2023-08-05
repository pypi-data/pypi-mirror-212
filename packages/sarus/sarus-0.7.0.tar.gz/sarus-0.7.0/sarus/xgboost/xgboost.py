from __future__ import annotations

from typing import Any, Optional

import sarus_data_spec.protobuf as sp

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.utils import register_ops, sarus_init, sarus_method

try:
    import xgboost
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class XGBClassifier(DataSpecWrapper[xgboost.XGBClassifier]):
    @sarus_init("xgboost.XGB_CLASSIFIER")
    def __init__(
        self,
        *,
        objective="binary:logistic",
        use_label_encoder: Optional[bool] = None,
        _dataspec=None,
        **kwargs: Any,
    ):
        ...

    @sarus_method("sklearn.SK_FIT", inplace=True)
    def fit(self, X, y, sample_weight=None):
        ...


register_ops()
