# /frontend/app.py
import streamlit as st
import requests
import pandas as pd

# --- Configuration ---
st.set_page_config(
    layout="wide", 
    page_title="Halal Money - Islamic Trading Platform", 
    page_icon="�",
    initial_sidebar_state="expanded"
)

BACKEND_URL = "http://127.0.0.1:8000"

# --- Helper Functions ---
def get_account_info():
    """Fetches account data from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/alpaca/account")
        response.raise_for_status()
        return response.json().get('account', {})
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to backend: {e}")
        return None

def get_positions():
    """Fetches current positions."""
    try:
        response = requests.get(f"{BACKEND_URL}/alpaca/positions")
        response.raise_for_status()
        return response.json().get('positions', [])
    except requests.exceptions.RequestException:
        return []

def get_orders(status='all'):
    """Fetches orders with a given status."""
    try:
        response = requests.get(f"{BACKEND_URL}/alpaca/orders", params={"status": status})
        response.raise_for_status()
        return response.json().get('orders', [])
    except requests.exceptions.RequestException:
        return []

# --- Main App Layout ---
st.title("� Halal Money - Trading Platform")

# Top navigation
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Stock Analysis & Research", use_container_width=True, type="primary"):
        st.switch_page("pages/stock_analysis.py")

with col2:
    if st.button("📈 Enhanced Trading Dashboard", use_container_width=True):
        st.switch_page("pages/trading_dashboard.py")

with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("home.py")

st.markdown("---")

# Sidebar for navigation
page = st.sidebar.radio("Navigate", ["Dashboard", "Trading", "Market Data"])

# ==============================================================================
# 1. DASHBOARD PAGE
# ==============================================================================
if page == "Dashboard":
    st.header("Account Dashboard")

    account_info = get_account_info()
    if account_info:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Equity", f"${float(account_info.get('equity', 0)):,.2f}")
        col2.metric("Buying Power", f"${float(account_info.get('buying_power', 0)):,.2f}")
        col3.metric("Status", account_info.get('status', 'N/A').upper())
        col4.metric("Daytrade Count", account_info.get('daytrade_count', 0))

    st.subheader("Current Positions")
    positions = get_positions()
    if positions:
        df_positions = pd.DataFrame(positions)
        st.dataframe(df_positions[['symbol', 'qty', 'side', 'market_value', 'unrealized_pl', 'current_price']])
    else:
        st.info("No open positions.")

# ==============================================================================
# 2. TRADING PAGE
# ==============================================================================
elif page == "Trading":
    st.header("Trade Execution")

    # --- Place a New Order Form ---
    with st.form("new_order_form", clear_on_submit=True):
        st.subheader("Place New Order")
        c1, c2, c3, c4 = st.columns(4)
        symbol = c1.text_input("Symbol", "AAPL").upper()
        qty = c2.number_input("Quantity", min_value=0.001, value=1.0, step=0.01)
        side = c3.radio("Side", ["buy", "sell"])
        time_in_force = c4.selectbox("Time in Force", ["day", "gtc", "opg", "cls"])
        
        submitted = st.form_submit_button("Submit Order")
        if submitted:
            payload = {
                "symbol": symbol,
                "qty": qty,
                "side": side,
                "type": "market",  # MVP focuses on market orders
                "time_in_force": time_in_force
            }
            try:
                response = requests.post(f"{BACKEND_URL}/alpaca/orders", json=payload)
                response.raise_for_status()
                st.success(f"Order submitted successfully!")
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                error_data = e.response.json() if e.response else str(e)
                st.error(f"Failed to place order: {error_data}")
    
    # --- View Existing Orders ---
    st.subheader("Order History")
    order_status_filter = st.selectbox("Filter orders by status", ["all", "open", "closed"])
    orders = get_orders(order_status_filter)
    if orders:
        df_orders = pd.DataFrame(orders)
        st.dataframe(df_orders[['symbol', 'qty', 'side', 'type', 'status', 'filled_at', 'submitted_at']])
    else:
        st.info(f"No {order_status_filter} orders found.")

# ==============================================================================
# 3. MARKET DATA PAGE
# ==============================================================================
elif page == "Market Data":
    st.header("Market Data & Charting")
    
    st.info("📊 For advanced market analysis, charting, and AI insights, visit our enhanced Stock Analysis page!")
    
    if st.button("🚀 Go to Stock Analysis Page", type="primary"):
        st.switch_page("pages/stock_analysis.py")
    
    st.markdown("---")
    
    c1, c2, c3 = st.columns(3)
    symbols_input = c1.text_input("Symbols (comma-separated)", "AAPL,TSLA").upper()
    timeframe_input = c2.selectbox("Timeframe", ["15Min", "1Day", "1Hour", "5Min", "1Min"])
    limit_input = c3.number_input("Bar Limit", min_value=1, max_value=1000, value=100)
    
    if st.button("Get Market Data"):
        params = {
            "symbols": symbols_input,
            "timeframe": timeframe_input,
            "limit": limit_input
        }
        try:
            response = requests.get(f"{BACKEND_URL}/alpaca/stocks/bars", params=params)
            response.raise_for_status()
            data = response.json()
            
            for symbol, bars in data.items():
                if bars:
                    st.subheader(f"Chart for {symbol}")
                    df = pd.DataFrame(bars)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df.set_index('timestamp', inplace=True)
                    st.line_chart(df['close'])
                    with st.expander("View Raw Data"):
                        st.dataframe(df)
                else:
                    st.warning(f"No data returned for {symbol}.")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch market data: {e}")

# Footer
st.markdown("---")
st.caption("💡 **New Features Available!** Try our AI-powered Stock Analysis and enhanced Trading Dashboard using the buttons above.")