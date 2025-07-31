# Halal Money - AlgoTrading MVP

A comprehensive algorithmic trading platform with Alpaca integration, designed for Halal (Sharia-compliant) trading strategies.

## 🚀 Project Overview

This project provides a full-stack solution for algorithmic trading with:
- **Backend API**: FastAPI-based REST API with Alpaca integration
- **Frontend**: Streamlit web interface for user interaction
- **Paper Trading**: Safe testing environment using Alpaca's paper trading
- **Real-time Data**: Stock market data and historical analysis

## 📁 Project Structure

```
halal-money/
├── backend/           # FastAPI backend server
│   └── main.py       # Main API endpoints and trading logic
├── frontend/         # Streamlit web application
│   └── app.py       # Frontend interface
├── shared/          # Shared utilities and configurations
├── docs/            # Documentation files
├── requirements.txt # Python dependencies
├── SECRETS         # Environment variables (not in git)
└── README.md       # This file
```

## 🛠️ Features

### Backend API Endpoints

- **`GET /ping`** - Health check endpoint
- **`GET /account`** - Fetch Alpaca account information
- **`GET /positions`** - List all open trading positions
- **`GET /orders`** - Retrieve order history with filters
- **`GET /stocks/bar`** - Get historical stock data (OHLCV bars)
- **`POST /order`** - Place buy/sell orders (paper trading)
- **`POST /cancel_order/{order_id}`** - Cancel specific orders
- **`GET /assets`** - List all tradeable assets

### Stock Data Features

- Multiple timeframes: 1Min, 5Min, 15Min, 1Hour, 1Day
- Historical data with customizable date ranges
- OHLCV (Open, High, Low, Close, Volume) data
- Adjustments for splits and dividends

## 📋 Prerequisites

- Python 3.8+
- Alpaca Trading Account (Paper Trading)
- Alpaca API Keys

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AAbdulghany/halal-money.git
   cd halal-money
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `SECRETS` file or set environment variables:
   ```
   APCA_API_KEY_ID=your_alpaca_api_key
   APCA_API_SECRET_KEY=your_alpaca_secret_key
   ```

## 🚀 Running the Application

### Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Start the Frontend

```bash
cd frontend
streamlit run app.py
```

The web interface will be available at `http://localhost:8501`

## 📊 API Usage Examples

### Get Account Information
```bash
curl http://localhost:8000/account
```

### Get Stock Data
```bash
curl "http://localhost:8000/stocks/bar?symbol=AAPL&timeframe=1Day&bars=10"
```

### Place an Order
```bash
curl -X POST "http://localhost:8000/order" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "qty": 1,
    "side": "buy",
    "type": "market",
    "time_in_force": "gtc"
  }'
```

## 🔒 Security & Configuration

- **Paper Trading Only**: Currently configured for Alpaca's paper trading environment
- **Environment Variables**: Sensitive credentials stored in environment variables
- **API Rate Limits**: Respects Alpaca API rate limiting

## 🏗️ Technology Stack

- **Backend**: FastAPI, Python 3.11, Alpaca-py
- **Frontend**: Streamlit
- **Data**: Alpaca Markets API
- **Deployment**: Uvicorn ASGI server

## 📈 Supported Markets

- US Equity Markets
- Paper Trading Environment
- Real-time and Historical Data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Paper trading is simulated trading and does not involve real money. Always conduct thorough testing before considering live trading.

## 🔮 Roadmap

- [ ] Zoya API integration for Halal stock screening
- [ ] Advanced trading strategies
- [ ] Portfolio management features
- [ ] Risk management tools
- [ ] Enhanced frontend dashboard
- [ ] Real-time alerts and notifications
- [ ] Backtesting capabilities

## 📞 Support

For questions or support:
1. Check the [API documentation](http://localhost:8000/docs) when running locally
2. Review the code in `backend/main.py` for implementation details
3. Open an issue in this repository

---

**Happy Trading! 📈**