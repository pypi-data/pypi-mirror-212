# collect.py

import threading
from typing import (
    Optional, Dict, Iterable, List, Callable, Union
)

from cryptofeed.feed import Feed
from cryptofeed.exchanges import EXCHANGE_MAP

from auto_screener.symbols import ticker_to_parts, Separator
from auto_screener.symbols import parts_to_symbol

__all__ = [
    "collect_assets",
    "collect_tickers",
    "collect_mutual_assets",
    "collect_mutual_tickers",
    "is_valid_ticker",
    "validate_ticker",
    "collect_exchanges",
    "is_valid_source",
    "find_name"
]

def _collect_exchange_assets(
        data: Dict[str, List[str]],
        exchange: str,
        feed: Feed,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> None:
    """
    Collects the tickers from the exchanges.

    :param exchange: The name of the exchange.
    :param feed: The exchange object.
    :param data: The data to collect the assets.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    quotes = quotes or []
    excluded = excluded or []
    assets = []

    # noinspection PyBroadException
    try:
        for ticker in feed.symbols():
            ticker: str

            base, quote = ticker_to_parts(ticker, separator='-')

            if (
                quotes and
                (quote not in quotes) or
                (quote in excluded) or
                (base in excluded)
            ):
                continue
            # end if

            assets.append(base)
        # end for

        data[exchange] = list(set(assets))

    except Exception:
        data[exchange] = []
    # end try
# end _collect_exchange_assets

def _collect_exchange_tickers(
        data: Dict[str, List[str]],
        exchange: str,
        feed: Feed,
        quotes: Optional[Iterable[str]] = None,
        separator: Optional[str] = Separator.value,
        excluded: Optional[Iterable[str]] = None
) -> None:
    """
    Collects the tickers from the exchanges.

    :param exchange: The name of the exchange.
    :param feed: The exchange object.
    :param data: The data to collect the assets.
    :param quotes: The quotes of the asset pairs.
    :param separator: The separator of the assets.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    quotes = quotes or []
    excluded = excluded or []
    tickers = []

    # noinspection PyBroadException
    try:
        for ticker in feed.symbols():
            ticker: str

            base, quote = ticker_to_parts(ticker, separator='-')

            if (
                quotes and
                (quote not in quotes) or
                (tickers in excluded) or
                (ticker.replace('-', separator) in excluded)
            ):
                continue
            # end if

            tickers.append(ticker.replace('-', separator))
        # end for

        data[exchange] = list(set(tickers))

    except Exception:
        data[exchange] = []
    # end try
# end _collect_exchange_tickers

Collector = Callable[
    [Dict[str, List[str]], str, Feed, Optional[Iterable[str]]], None
]

def find_name(name: str, names: Iterable[str]) -> str:
    """
    Finds the exchange in the exchanges.

    :param name: The name of the exchange.
    :param names: The exchanges to search in.

    :return: The valid exchange name.
    """

    for value in names:
        if value.lower() == name.lower():
            return value
        # end if
    # end for

    return name
# end find_name

def _collect_data(
        collector: Collector,
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    excluded_tickers = []

    excluded = excluded or {}

    if not excluded:
        excluded_tickers = excluded
    # end if

    if (
        excluded and
        all(isinstance(value, str) for value in excluded) and
        not isinstance(excluded, dict)
    ):
        excluded = {exchange: excluded_tickers for exchange in exchanges}
    # end if

    quotes = quotes or []

    data = {}
    markets = {}

    for source in (exchanges or EXCHANGE_MAP.keys()):
        if source.upper() not in EXCHANGE_MAP.keys():
            continue
        # end if

        exchange = EXCHANGE_MAP[source.upper()]

        markets[source] = exchange
    # end for

    for exchange, feed in markets.items():
        excluded_source = find_name(name=exchange, names=excluded)

        threading.Thread(
            target=collector,
            kwargs=dict(
                exchange=exchange, feed=feed,
                data=data, quotes=quotes, excluded=(
                    excluded[excluded_source]
                    if excluded_source in excluded else None
                )
            )
        ).start()
    # end for

    while len(markets) > len(data):
        pass
    # end while

    return {key: value for key, value in data.items() if value}
# end collect_tickers

def collect_assets(
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    return _collect_data(
        collector=_collect_exchange_assets,
        exchanges=exchanges, quotes=quotes, excluded=excluded
    )
# end collect_tickers

def _collect_mutual_data(
        data: Dict[str, Iterable[str]],
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param data: The exchanges' data.

    :return: The data of the exchanges.
    """

    values = {}

    for source in data:
        for asset in data[source]:
            values[asset] = values.setdefault(asset, 0) + 1
        # end for
    # end for

    return {
        source: [
            asset for asset in data[source]
            if values.get(asset, 0) > 1
        ]
        for source in data
    }
# end collect_mutual_assets

def collect_mutual_assets(
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        data: Optional[Dict[str, Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.
    :param data: The data to search in.

    :return: The data of the exchanges.
    """

    return _collect_mutual_data(
        data=data or collect_assets(
            exchanges=exchanges, quotes=quotes, excluded=excluded
        )
    )
# end collect_mutual_assets

def collect_tickers(
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    return _collect_data(
        collector=_collect_exchange_tickers,
        exchanges=exchanges, quotes=quotes, excluded=excluded
    )
# end collect_tickers

def collect_mutual_tickers(
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        data: Optional[Dict[str, Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.
    :param data: The data to search in.

    :return: The data of the exchanges.
    """

    return _collect_mutual_data(
        data=data or collect_tickers(
            exchanges=exchanges, quotes=quotes, excluded=excluded
        )
    )
# end collect_mutual_tickers

def is_valid_ticker(exchange: str, symbol: str) -> bool:
    """
    Returns a value for the ticker being valid for the source exchange.

    :param exchange: The name of the exchange platform.
    :param symbol: The ticker of the assets.

    :return: The validation-value.
    """

    if not is_valid_source(exchange):
        return False
    # end if

    return (
            symbol.replace(Separator.value, '-') in
            EXCHANGE_MAP[exchange.upper()].symbols()
    )
# end is_valid_ticker

def validate_ticker(exchange: str, symbol: str) -> str:
    """
    Validates the ticker value.

    :param exchange: The name of the exchange platform.
    :param symbol: The name of the ticker.

    :return: The validates ticker.
    """

    validate_source(exchange)

    if not is_valid_ticker(exchange, symbol):
        raise ValueError(
            f"ticker {symbol} is not a valid "
            f"ticker for the {exchange} exchange."
        )
    # end if

    return symbol
# end validate_ticker

def is_valid_source(exchange: str) -> bool:
    """
    checks of the source os a valid exchange name.

    :param exchange: The source name to validate.

    :return: The validation value.
    """

    return exchange.upper() in EXCHANGE_MAP
# end is_valid_source

def validate_source(exchange: str) -> str:
    """
    Validates the source value.

    :param exchange: The name of the exchange platform.

    :return: The validates ticker.
    """

    if not is_valid_source(exchange):
        raise ValueError(
            f"source {exchange} is not a valid exchange."
        )
    # end if

    return exchange
# end validate_source

def collect_exchanges(
        currencies: Dict[str, List[str]],
        pairs: Dict[str, List[str]],
        excluded: Optional[Dict[str, Iterable[str]]] = None,
) -> Dict[str, List[str]]:
    """
    Collects the exchanges.

    :param pairs: The data of currencies and their traded quote assets.
    :param currencies: The data of exchanges and their traded currencies.
    :param excluded: The data of excluded pairs for each exchange.

    :return: The data of exchanges and their tickers.
    """

    exchanges: Dict[str, List[str]] = {}

    for platform, currencies in currencies.items():
        exchanges[platform] = []

        for currency in currencies:
            for asset in pairs[currency]:
                if (
                    parts_to_symbol(asset, currency) in
                    excluded.get(platform, [])
                ):
                    continue
                # end if

                exchanges[platform].append(
                    parts_to_symbol(asset, currency)
                )
            # end for
        # end for
    # end for

    return exchanges
# end collect_exchanges