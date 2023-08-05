from .helpers import Helpers
from .models import MarketInfo, SymbolInfo, SymbolInfoBasic

class Mappers:
    @staticmethod
    def map_api_results_to_symbol_info_basic(market_info: MarketInfo, api_data: object) -> SymbolInfo:
        try:
            return SymbolInfoBasic(
                market_name=market_info.name.value,
                description=str(api_data[market_info.field_description]),
                symbol=api_data[market_info.field_symbol]
            )
        except Exception as ex:
            print(f"Error parsing info - {ex}")
            return None

    @staticmethod
    def map_api_results_to_symbol_info(market_info: MarketInfo, symbol: str) -> SymbolInfo:
        try:
            api_data = next(filter(lambda symbol_data: symbol_data[market_info.field_symbol] == symbol, market_info.data))
            result = Mappers.map_api_results_to_symbol_info_basic(market_info, api_data)

            result.average_percentage_change=Helpers.convert_to_percentage(str(api_data[market_info.field_average_percentage_change]))
            result.latest_price=Helpers.convert_to_money(api_data[market_info.field_latest_price])
    
            return result
        except Exception as ex:
            print(f"Error parsing info - {ex}")
            return None
