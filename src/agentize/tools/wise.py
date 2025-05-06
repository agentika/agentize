from agents import function_tool
from loguru import logger
from wisest.rate import RateHistoryRequest
from wisest.rate import Resolution
from wisest.rate import Unit


@function_tool
async def query_rate_history(source: str, target: str, length: int, resolution: Resolution, unit: Unit) -> str:
    """Query the exchange rate history between two currencies.

    Args:
        source (str): The source currency code (e.g., "EUR").
        target (str): The target currency code (e.g., "USD").
        length (int): The number of data points to retrieve.
        resolution (Resolution): The resolution of the data points.
        unit (Unit): The unit of time for the data points.
    """
    logger.debug(f"Querying rate history for {source} to {target}")

    req = RateHistoryRequest(
        source=source,
        target=target,
        length=length,
        resolution=resolution,
        unit=unit,
    )
    rates = await req.async_do()
    return "\n".join([str(rate) for rate in rates])
