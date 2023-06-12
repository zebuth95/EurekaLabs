from typing import Dict
from enum import Enum
from pydantic import BaseModel, root_validator, Field


class AlphaOptions(str, Enum):
    Facebook = ("META",)
    Apple = ("AAPL",)
    Google = ("GOOGL",)
    Amazon = "AMZN"


class AlphaOptionsSchema(BaseModel):
    symbol = AlphaOptions


class AlphaDetailSchema(BaseModel):
    open_price: str = Field(alias="1. open")
    higher_price: str = Field(alias="2. high")
    lower_price: str = Field(alias="3. low")

    @root_validator
    def compute_variation(cls, values) -> Dict:
        h_price = values.get("higher_price", 0)
        l_price = values.get("lower_price", 0)
        values["variation"] = str(abs(float(h_price) - float(l_price)))

        return values
