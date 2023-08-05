
from enum import Enum

from dataclasses import dataclass
from typing import Optional

class Markets(str, Enum):
    BLBE = "BLBE"
    SASE = "SASE"

@dataclass
class MarketInfo:
    field_name: str
    field_latest_price: str
    field_symbol: str
    name: Markets
    request_type: str
    root_url: str
    status_url: str
    type: str
    data: Optional[dict] = None
    field_average_percentage_change: Optional[str] = None
    field_description: Optional[str] = None
    content_type: Optional[str] = "application/json"
    request_info_params: Optional[dict] = None

@dataclass
class SymbolInfoBasic:
    market_name: str
    description: str
    symbol: str


@dataclass
class SymbolInfo(SymbolInfoBasic):
    average_percentage_change: str
    latest_price: str
