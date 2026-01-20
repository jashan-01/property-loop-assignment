import pandas as pd
from pathlib import Path


def get_data_path() -> Path:
    return Path(__file__).parent.parent / "data"


def load_holdings() -> pd.DataFrame:
    path = get_data_path() / "holdings.csv"
    if not path.exists():
        raise FileNotFoundError(f"Holdings file not found: {path}")
    return pd.read_csv(path)


def load_trades() -> pd.DataFrame:
    path = get_data_path() / "trades.csv"
    if not path.exists():
        raise FileNotFoundError(f"Trades file not found: {path}")
    return pd.read_csv(path)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    holdings_df = load_holdings()
    trades_df = load_trades()
    return holdings_df, trades_df
