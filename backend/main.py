import os
from fastapi import FastAPI, HTTPException, Query
from typing import Optional

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.requests import GetOrdersRequest, OrderRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

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
@app.get("/stocks/bar?")
def get_stock_bars(
    symbol: str,
    timeframe: str = Query("1Day", description="Bar interval: 1Min, 5Min, 1Hour, 1Day"),
    bars: Optional[int] = Query(5, description="Number of most recent bars to fetch"),
    limit: Optional[int] = Query(1000, description="The maximum number of data points to return in the response page"),
    start: Optional[str] = Query(None, description="Start date/time ISO8601 (e.g. 2023-01-01)"),
    end: Optional[str] = Query(None, description="End date/time ISO8601 (inclusive)"),
    adjustment: str = Query("raw", description='adjustment: "raw", "split", "dividend", or "all"'),    
):
    """
    Fetch historical OHLCV bars for a stock symbol using Alpaca 'stock bars' API.
    """
    # --- Validate timeframe:
    valid_timeframes = {"1Min": TimeFrame.Min, "5Min": TimeFrame.FiveMin, "15Min": TimeFrame.FifteenMin,
                        "1Hour": TimeFrame.Hour, "1Day": TimeFrame.Day}
    tf = valid_timeframes.get(timeframe)
    if tf is None:
        raise HTTPException(status_code=400, detail=f"Invalid timeframe '{timeframe}'. Allowed: {list(valid_timeframes)}")

    # --- Date parsing (ISO 8601):
    try:
        end_dt = datetime.fromisoformat(end) if end else datetime.now()
        if start:
            start_dt = datetime.fromisoformat(start)
        else:
            # Default: go 'bars' worth of periods backwards (factor ×2 for market closure days)
            days_back = bars * 2 if tf == TimeFrame.Day else bars // 20  # estimate extra span for weekends
            start_dt = end_dt - timedelta(days=days_back)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format for start/end ({e})")

    # --- Build bar request ---
    req = StockBarsRequest(
        symbol_or_symbols=symbol.upper(),
        timeframe=tf,
        limit=limit,
        adjustment=adjustment
    )

    try:
        bars = data_client.get_stock_bars(req)
        df = bars.df
        if df.empty:
            return {"symbol": symbol.upper(), "bars": []}

        # Use only the last N bars if 'bars' param used
        if bars is not None and 'bars' in locals() and df.shape[0] > bars:
            df = df.tail(bars)
        # Always reset index for serializable output
        result = df.reset_index().to_dict(orient="records")
        return {"symbol": symbol.upper(), "bars": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alpaca error: {str(e)}")

# --- 7. Place Paper Trade Order ---
from pydantic import BaseModel

class PlaceOrderRequest(BaseModel):
    symbol: str
    qty: int
    side: str  # "buy" or "sell"
    type: str = "market"
    time_in_force: str = "gtc"  # good till canceled

@app.post("/order")
def place_order(order: PlaceOrderRequest):
    """Place a paper trade order (buy or sell)."""
    order = OrderRequest()
    try:
        order_response = trading_client.submit_order(
            symbol=order.symbol.upper(),
            qty=order.qty,
            side=order.side.lower(),
            type=order.type,
            time_in_force=order.time_in_force
        )
        return {"order": order_response.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
