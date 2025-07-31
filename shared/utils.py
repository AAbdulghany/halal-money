import re
from alpaca.data.timeframe import TimeFrameUnit, TimeFrame

# --- HELPER FUNCTION: Parse string to TimeFrame object ---
def parse_timeframe(timeframe_str: str) -> TimeFrame:
    """
    Parses a string like "5Min" into an Alpaca SDK TimeFrame object.
    e.g., "15Min" -> TimeFrame(15, TimeFrameUnit.Minute)
    """
    # Use a regular expression to extract the number and the unit
    match = re.match(r"(\d+)(Min|Hour|Day|Week|Month)", timeframe_str)
    if not match:
        raise ValueError(f"Invalid timeframe format: '{timeframe_str}'. Expected format like '1Min', '1Day', etc.")

    amount, unit_str = match.groups()
    amount = int(amount)

    # Map the unit string to the TimeFrameUnit enum
    unit_map = {
        "Min": TimeFrameUnit.Minute,
        "Hour": TimeFrameUnit.Hour,
        "Day": TimeFrameUnit.Day,
        "Week": TimeFrameUnit.Week,
        "Month": TimeFrameUnit.Month,
    }
    unit = unit_map.get(unit_str)
    
    if not unit:
         raise ValueError(f"Invalid timeframe unit in '{timeframe_str}'")

    # The SDK's own validation will run inside the TimeFrame constructor
    return TimeFrame(amount, unit)