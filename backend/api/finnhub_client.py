import os
from pathlib import Path
import sys
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
import finnhub
import requests
from datetime import datetime, timedelta
from pydantic import BaseModel
import time

sys.path.append(str(Path(__file__).parent.parent.parent))

# Finnhub API configuration
FINNHUB_API_KEY = os.getenv("FNHB_API_KEY")

if not FINNHUB_API_KEY:
    raise RuntimeError("Missing Finnhub API key. Please set FNHB_API_KEY environment variable.")


# Initialize Finnhub client with custom session
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


router = APIRouter()

class StockSymbol(BaseModel):
    """Stock symbol data model"""
    currency: str
    description: str
    displaySymbol: str
    figi: str
    mic: str
    symbol: str
    type: str

class StockQuote(BaseModel):
    """Stock quote data model"""
    symbol: str
    current_price: float
    change: float
    percent_change: float
    high_price: float
    low_price: float
    open_price: float
    previous_close: float
    timestamp: int

# --- Connectivity Test ---
@router.get("/ping")
def ping():
    """Test Finnhub API connectivity."""
    return {"msg": "Finnhub client is ready", "timestamp": datetime.now().isoformat()}

# --- Get All Stocks (Default US Exchange) ---
@router.get("/stocks", response_model=List[StockSymbol])
def get_all_stocks(exchange:str = Query("US", description="Exchange code (default: US)")):
    try:
        stocks = finnhub_client.stock_symbols(exchange.upper(), mic="XNAS")
        return stocks
    except Exception as e:
        raise HTTPException(detail=f"Error fetching stocks from US: {str(e)}")


# --- Get Company Profile ---
@router.get("/profile/{symbol}")
def get_company_profile(symbol: str):
    """
    Get company profile information.
    """
    try:
        # Get company profile from Finnhub with retry logic
        def api_call():
            return finnhub_client.company_profile2(symbol=symbol.upper())
        
        profile = retry_api_call(api_call)
        
        return {
            "symbol": symbol.upper(),
            "profile": profile
        }
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions (like timeout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching profile for {symbol}: {str(e)}")
