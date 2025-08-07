import streamlit as st
import requests
import pandas as pd

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"

# Page Configuration
st.set_page_config(
    page_title="Trading Dashboard - Halal Money",
    page_icon="📈",
    layout="wide"
)

# Helper Functions
def get_account_info():
    """Fetches account data from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/alpaca/account")
        response.raise_for_status()
        return response.json().get('account', {})
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to trading backend: {e}")
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

def place_order(symbol, qty, side, order_type="market", time_in_force="day"):
    """Place a trading order"""
    payload = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": order_type,
        "time_in_force": time_in_force
    }
    try:
        response = requests.post(f"{BACKEND_URL}/alpaca/orders", json=payload)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        error_msg = "Order placement failed"
        try:
            error_data = e.response.json() if e.response else str(e)
            error_msg = f"Order failed: {error_data}"
        except:
            error_msg = f"Order failed: {str(e)}"
        return False, error_msg

def get_stock_quote(symbol):
    """Get stock information for trading"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/stocks/{symbol}/info")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def main():
    st.title("📈 Trading Dashboard")
    st.markdown("*Paper trading with real market data*")
    
    # Navigation
    if st.button("← Back to Stock Analysis", help="Return to stock research"):
        st.switch_page("pages/stock_analysis.py")
    
    st.markdown("---")
    
    # Account Overview Section
    st.header("💼 Account Overview")
    
    account_info = get_account_info()
    if account_info:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            equity = float(account_info.get('equity', 0))
            st.metric("Total Equity", f"${equity:,.2f}")
        
        with col2:
            buying_power = float(account_info.get('buying_power', 0))
            st.metric("Buying Power", f"${buying_power:,.2f}")
        
        with col3:
            status = account_info.get('status', 'N/A').upper()
            st.metric("Account Status", status)
        
        with col4:
            daytrade_count = account_info.get('daytrade_count', 0)
            st.metric("Day Trade Count", daytrade_count)
    
    else:
        st.error("Unable to connect to trading account. Please check your Alpaca API configuration.")
        return
    
    # Create tabs for different trading functions
    tab1, tab2, tab3, tab4 = st.tabs([
        "🛒 Place Order", "📊 Portfolio", "📋 Order History", "📈 Market Data"
    ])
    
    with tab1:
        st.subheader("Place New Order")
        
        with st.form("trading_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                symbol = st.text_input(
                    "Stock Symbol", 
                    value="AAPL",
                    help="Enter the stock symbol (e.g., AAPL, MSFT)"
                ).upper()
                
                qty = st.number_input(
                    "Quantity", 
                    min_value=0.001, 
                    value=1.0, 
                    step=0.001,
                    help="Number of shares to buy/sell"
                )
                
                side = st.radio(
                    "Order Side", 
                    ["buy", "sell"],
                    horizontal=True
                )
            
            with col2:
                order_type = st.selectbox(
                    "Order Type", 
                    ["market", "limit"],
                    help="Market orders execute immediately at current price"
                )
                
                time_in_force = st.selectbox(
                    "Time in Force", 
                    ["day", "gtc", "opg", "cls"],
                    help="How long the order remains active"
                )
                
                # Get current stock info
                if symbol:
                    stock_info = get_stock_quote(symbol)
                    if stock_info:
                        st.info(f"**{stock_info['name']}**\nCurrent Price: ${stock_info['current_price']:.2f}")
                    else:
                        st.warning(f"Could not fetch data for {symbol}")
            
            submitted = st.form_submit_button("🚀 Place Order", type="primary")
            
            if submitted:
                if not symbol:
                    st.error("Please enter a stock symbol")
                elif qty <= 0:
                    st.error("Quantity must be greater than 0")
                else:
                    success, result = place_order(symbol, qty, side, order_type, time_in_force)
                    
                    if success:
                        st.success("✅ Order placed successfully!")
                        st.json(result)
                    else:
                        st.error(result)
    
    with tab2:
        st.subheader("Current Portfolio")
        
        positions = get_positions()
        if positions:
            # Create portfolio DataFrame
            portfolio_data = []
            total_value = 0
            
            for pos in positions:
                market_value = float(pos.get('market_value', 0))
                unrealized_pl = float(pos.get('unrealized_pl', 0))
                current_price = float(pos.get('current_price', 0))
                
                portfolio_data.append({
                    'Symbol': pos['symbol'],
                    'Quantity': float(pos['qty']),
                    'Side': pos['side'],
                    'Current Price': f"${current_price:.2f}",
                    'Market Value': f"${market_value:.2f}",
                    'Unrealized P&L': f"${unrealized_pl:.2f}",
                    'P&L %': f"{(unrealized_pl/market_value)*100:.2f}%" if market_value != 0 else "0.00%"
                })
                
                total_value += market_value
            
            if portfolio_data:
                st.metric("Total Portfolio Value", f"${total_value:.2f}")
                
                df = pd.DataFrame(portfolio_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No open positions found.")
    
    with tab3:
        st.subheader("Order History")
        
        # Order status filter
        order_status_filter = st.selectbox(
            "Filter by Status", 
            ["all", "open", "closed"],
            help="Filter orders by their current status"
        )
        
        orders = get_orders(order_status_filter)
        if orders:
            order_data = []
            
            for order in orders:
                order_data.append({
                    'Symbol': order.get('symbol', ''),
                    'Quantity': float(order.get('qty', 0)),
                    'Side': order.get('side', '').upper(),
                    'Type': order.get('type', '').upper(),
                    'Status': order.get('status', '').upper(),
                    'Submitted': order.get('submitted_at', ''),
                    'Filled': order.get('filled_at', '') or 'N/A'
                })
            
            if order_data:
                df = pd.DataFrame(order_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info(f"No {order_status_filter} orders found.")
    
    with tab4:
        st.subheader("Market Data")
        st.info("📊 For detailed market analysis and charts, visit our Stock Analysis page.")
        
        if st.button("🔍 Go to Stock Analysis", type="primary"):
            st.switch_page("pages/stock_analysis.py")
        
        # Quick market data
        popular_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        
        st.write("**Quick Quotes:**")
        quote_cols = st.columns(len(popular_symbols))
        
        for i, symbol in enumerate(popular_symbols):
            stock_info = get_stock_quote(symbol)
            if stock_info:
                with quote_cols[i]:
                    change_color = "🟢" if stock_info['day_change'] >= 0 else "🔴"
                    st.metric(
                        f"{symbol} {change_color}",
                        f"${stock_info['current_price']:.2f}",
                        delta=f"{stock_info['day_change']:.2f}"
                    )
    
    # Risk Disclaimer
    st.markdown("---")
    st.warning("""
    ⚠️ **Risk Disclaimer**: This is a paper trading environment for educational purposes. 
    All trades are simulated and no real money is involved. Always conduct thorough research 
    and consider consulting financial advisors before real trading.
    """)

if __name__ == "__main__":
    main()
