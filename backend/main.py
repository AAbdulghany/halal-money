import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from typing import Optional

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.requests import GetOrdersRequest, OrderRequest
from datetime import datetime
from pydantic import BaseModel

sys.path.append(str(Path(__file__).parent.parent))
from shared.utils import parse_timeframe

# --- 1. Load .env for Local Dev (optional) ---

ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
ALPACA_API_SECRET = os.getenv("APCA_API_SECRET_KEY")

if not ALPACA_API_KEY or not ALPACA_API_SECRET:
    raise RuntimeError("Missing Alpaca API credentials")

trading_client = TradingClient(
    ALPACA_API_KEY, ALPACA_API_SECRET, paper=True
)
data_client = StockHistoricalDataClient(
    ALPACA_API_KEY, ALPACA_API_SECRET
)

app = FastAPI(
    title="AlgoTrading-MVP API",
    description="Back-end API for your AlgoTrading MVP with Alpaca and (soon) Zoya integration."
)


# --- 2. Diagnostics ---
@app.get("/ping")
def ping():
    """Test connectivity."""
    return {"msg": "pong"}

# --- 3. Account Info ---
@app.get("/account")
def get_account():
    """Fetch your Alpaca account state (funding, status, etc)."""
    try:
        account = trading_client.get_account()
        return {"account": account.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 4. List All Positions ---
@app.get("/positions")
def get_positions():
    """List all open positions."""
    try:
        positions = trading_client.get_all_positions()
        return {"positions": [pos.dict() for pos in positions]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 5. List All Orders ---
@app.get("/orders")
def get_orders(
    status: str = Query("all", regex="^(open|closed|all)$", description="Filter orders by status"),
    limit: int = Query(50, ge=1, le=500, description="Max number of orders to return")
):
    """Fetch all recent orders (open, closed, or all)."""
    filter = GetOrdersRequest(
        status=status.lower(),
        limit=limit
    )

    try:
        orders = trading_client.get_orders(filter=filter)
        return {"orders": [o.dict() for o in orders]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 6. Get Stock Bars ---
@app.get("/stocks/bars")
def get_stock_bars(
    symbols: str = Query("AAPL", description="Comma-separated stock symbols"),
    timeframe: str = Query("15Min", description="Bar interval (e.g. 1Min, 15Min, 1Hour, 1Day)"),
    limit: Optional[int] = Query(1000, description="Max bars per symbol"),
    adjustment: str = Query("raw", description='Adjustment type'),
    start: Optional[str] = Query(None, description="Start ISO8601 date/time"),
    end: Optional[str] = Query(None, description="End ISO8601 date/time"),
    sort: str = Query("asc", description='Sort order: "asc" or "desc"'),
    feed: Optional[str] = Query("sip", description="Data feed (e.g. sip, iex, otc)")
):
    """
    Fetch historical OHLCV bars using a dynamically parsed timeframe.
    """
    # --- Use the new helper function to parse the timeframe string ---
    try:
        tf_object = parse_timeframe(timeframe)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    start_dt = datetime.fromisoformat(start) if start else None
    end_dt = datetime.fromisoformat(end) if end else None
    
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]

    try:
        request = StockBarsRequest(
            symbol_or_symbols=symbol_list,
            timeframe=tf_object,
            start=start_dt,
            end=end_dt,
            limit=limit,
            adjustment=adjustment,
            sort=sort,
            feed=feed
        )
        
        bars = data_client.get_stock_bars(request)
        df = bars.df

    except Exception as e:
        # The SDK might raise its own validation errors (e.g., "5Day" is invalid)
        raise HTTPException(status_code=500, detail=f"Alpaca SDK error: {str(e)}")

    # Convert DataFrame output to dict keyed by symbol (this part remains the same)
    output = {}
    if not df.empty:
        for symbol in symbol_list:
            if "symbol" in df.index.names:
                symbol_df = df[df.index.get_level_values("symbol") == symbol]
            else:
                symbol_df = df
            output[symbol] = symbol_df.reset_index().to_dict(orient="records")
    else:
        for symbol in symbol_list:
            output[symbol] = []

    return output

# --- 7. Place Paper Trade Order ---
class PlaceOrderRequest(BaseModel):
    symbol: str = "AAPL"    # Stock symbol to trade
    qty: int = 1            # Quantity to buy/sell
    side: str = "buy"       # "buy" or "sell"
    type: str = "market"    # "market", "limit", stop, stop_limit, trailing_stop
    time_in_force: str = "day"  # Default time_in_force to "day" for simplicity, can be changed to "gtc" or others as needed
    
@app.post("/orders")
def place_order(payload: PlaceOrderRequest): # Renamed to 'payload' for clarity
    """Place a paper trade order (buy or sell)."""
    # --- FIX: Create the OrderRequest using data FROM the payload ---
    order_data = OrderRequest(
        symbol=payload.symbol.upper(),
        qty=payload.qty,
        side=payload.side.lower(),
        type=payload.type,
        time_in_force=payload.time_in_force
    )

    try:
        order_response = trading_client.submit_order(order_data=order_data)
        
        return {"order": order_response.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alpaca API error: {str(e)}")


# --- 8. Cancel Existing Order ---
@app.post("/cancel_order/{order_id}")
def cancel_order(order_id: str):
    """Cancel a specific order by ID."""
    try:
        resp = trading_client.cancel_order_by_id(order_id)
        return {"status": "cancelled", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 9. List Supported Assets ---
@app.get("/assets")
def get_assets(status: str = "active", asset_class: str = "us_equity"):
    """Fetch all supported (tradable) assets."""
    try:
        assets = trading_client.get_all_assets(status=status, asset_class=asset_class)
        return {"assets": [a.dict() for a in assets]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
