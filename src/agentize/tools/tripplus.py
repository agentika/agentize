from typing import Literal

from agents import function_tool
from loguru import logger
from tripplus import RedemptionRequest


@function_tool
def search_award(ori: str, dst: str, cabin: Literal["y", "c", "f"], type: Literal["ow", "rt"]) -> str:
    """
    Search for award flight options between two airports.

    Args:
        ori: Origin airport code (e.g., TPE for Taipei Taoyuan, LHR for London Heathrow)
        dst: Destination airport code (e.g., NRT for Tokyo Narita, LAX for Los Angeles)
        cabin: Cabin class, y: economy, c: business, f: first
        type: Redemption type, ow: one way, rt: round trip

    Returns:
        JSON string with redemption options

    Examples:
        >>> search_award("TPE", "NRT", "c", "ow")
        >>> search_award("LHR", "JFK", "y", "rt")
    """
    try:
        req = RedemptionRequest(
            ori=ori,
            dst=dst,
            cabin=cabin,
            type=type,
            programs="ALL",
        )
        resp = req.do()
    except Exception as e:
        logger.error(f"Failed to search for award flights: {e}")
        return "Failed to search for award flights."

    return resp.model_dump_json()
