from __future__ import annotations

import pandas as pd
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CSVLoader:
    path: str
    parse_dates: bool = True
    index_col: Optional[str] = None

    def load(self) -> pd.DataFrame:
        return pd.read_csv(
            self.path,
            parse_dates=self.parse_dates,
            index_col=self.index_col,
        )


@dataclass
class DataFrameLoader:
    df: pd.DataFrame

    def load(self) -> pd.DataFrame:
        return self.df.copy()


@dataclass
class DictLoader:
    data: Dict[str, Any]

    def load(self) -> pd.DataFrame:
        return pd.DataFrame(self.data)