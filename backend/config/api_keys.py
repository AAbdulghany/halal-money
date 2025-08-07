import os
from typing import Optional

# Free API configurations
class APIConfig:
    # Alpha Vantage (12k free requests/month)
    ALPHA_VANTAGE_KEY: Optional[str] = os.getenv("ALPHA_VANGE_KEY")
    ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
    
    # Financial Modeling Prep (250 free requests/day)
    FMP_KEY: Optional[str] = os.getenv("FMP_API_KEY")
    FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
    
    # Finnhub (60 calls/minute for free tier)
    FINNHUB_KEY: Optional[str] = os.getenv("FINNHUB_API_KEY")
    FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
    
    # NewsAPI.org (1000 free requests/month)
    NEWS_API_KEY: Optional[str] = os.getenv("NEWS_API_KEY")
    NEWS_API_BASE_URL = "https://newsapi.org/v2"
    
    # Yahoo Finance (free, no key needed)
    YAHOO_FINANCE_BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart"
    
    @classmethod
    def get_available_apis(cls):
        """Return list of available API services based on configured keys"""
        available = []
        # if cls.ALPHA_VANTAGE_KEY and cls.ALPHA_VANTAGE_KEY != "demo":
        #     available.append("alpha_vantage")
        if cls.FMP_KEY:
            available.append("fmp")
        if cls.FINNHUB_KEY:
            available.append("finnhub")
        if cls.NEWS_API_KEY:
            available.append("news_api")
        available.append("yahoo_finance")  # Always available
        return available
