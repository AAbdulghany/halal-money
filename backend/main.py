from fastapi import FastAPI
from api.finnhub_client import router as finnhub_router
from api.alpaca_client import router as alpaca_router

app = FastAPI(
    title="Halal Trading-MVP API",
    description="Back-end API for your Halal Trading MVP with comprehensive stock analysis and Alpaca integration.",
    version="0.3.0",
)

# Stock analysis and data APIs (free tier)
app.include_router(finnhub_router)

# # Alpaca trading APIs (isolated and unchanged)
# app.include_router(alpaca_router, prefix="/alpaca")

@app.get("/")
def read_root():
    """API health check and information"""
    return {
        "message": "Halal Trading MVP API",
        "version": "0.3.0",
        "endpoints": {
            "stock_analysis": "/api/stocks",
            # "alpaca_trading": "/alpaca"
        },
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "halal-trading-api"}
