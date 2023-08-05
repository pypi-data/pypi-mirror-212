from __future__ import annotations

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

from typing import Tuple

import pandas as pd

TrainTestDataType: TypeAlias = Tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
]
