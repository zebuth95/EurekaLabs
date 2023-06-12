import requests
from abc import ABC

from configs.Environment import get_environment_variables
from schemas.AlphaSchema import AlphaDetailSchema

env = get_environment_variables()


class AlphaBase(ABC):
    def __init__(self, params) -> None:
        self.ulr = env.ALPHA_URL
        self.apy_key = env.API_KEY
        self.params = params

    def get(self):
        self.params.update(
            {
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "outputsize": "compact",
                "apikey": self.apy_key,
            }
        )
        try:
            response = (
                requests.get(self.ulr, params=self.params)
                .json()
                .get("Time Series (Daily)")
            )
            return {
                i: AlphaDetailSchema(**response.get(i)).dict(by_alias=False)
                for i in response.keys()
            }
        except ConnectionError:
            return 400, {"errors": [{"message": "Error connection", "code": 400}]}
        except Exception:
            return 400, {"errors": [{"message": "Source error", "code": 400}]}


class MetaAlpha(AlphaBase):
    def __init__(self):
        super(MetaAlpha, self).__init__({"symbol": "META"})


class AppleAlpha(AlphaBase):
    def __init__(self):
        super(AppleAlpha, self).__init__({"symbol": "AAPL"})


class MicrosoftAlpha(AlphaBase):
    def __init__(self):
        super(MicrosoftAlpha, self).__init__({"symbol": "MSFT"})


class GoogleAlpha(AlphaBase):
    def __init__(self):
        super(GoogleAlpha, self).__init__({"symbol": "GOOGL"})


class AmazonAlpha(AlphaBase):
    def __init__(self):
        super(AmazonAlpha, self).__init__({"symbol": "AMZN"})


def alpa_search(symbol: str):
    symbols = {
        "AMZN": AmazonAlpha(),
        "GOOGL": GoogleAlpha(),
        "MSFT": MicrosoftAlpha(),
        "AAPL": AppleAlpha(),
        "META": MetaAlpha(),
    }

    return symbols.get(symbol, None)
