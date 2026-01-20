import pandas as pd
import logging
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)


def get_data_path() -> Path:
    """Get the path to the data directory."""
    return Path(__file__).parent.parent / "data"


def load_holdings() -> pd.DataFrame:
    """Load holdings data with validation."""
    path = get_data_path() / "holdings.csv"
    if not path.exists():
        raise FileNotFoundError(f"Holdings file not found: {path}")
    
    try:
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} holdings records")
        return df
    except Exception as e:
        logger.error(f"Error loading holdings.csv: {e}")
        raise


def load_trades() -> pd.DataFrame:
    """Load trades data with validation."""
    path = get_data_path() / "trades.csv"
    if not path.exists():
        raise FileNotFoundError(f"Trades file not found: {path}")
    
    try:
        df = pd.read_csv(path)
        logger.info(f"Loaded {len(df)} trade records")
        return df
    except Exception as e:
        logger.error(f"Error loading trades.csv: {e}")
        raise


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load both datasets and return as tuple."""
    holdings_df = load_holdings()
    trades_df = load_trades()
    return holdings_df, trades_df
