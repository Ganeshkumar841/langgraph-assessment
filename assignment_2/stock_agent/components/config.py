try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        pass

load_dotenv()


class StockConfig(BaseSettings):
    """Settings and indicator parameters for the stock agent."""

    HISTORY_PERIOD: str = "60d"
    HISTORY_INTERVAL: str = "1d"
    MIN_REQUIRED_DAYS: int = 20

    SMA_SHORT_WINDOW: int = 10
    SMA_LONG_WINDOW: int = 20
    RSI_PERIOD: int = 14

    RSI_OVERBOUGHT: float = 70.0
    RSI_OVERSOLD: float = 30.0

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


config = StockConfig()
