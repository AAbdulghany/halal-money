import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"

# Page Configuration
st.set_page_config(
    page_title="Stock Analysis - Halal Money",
    page_icon="📊",
    layout="wide"
)

def fetch_stock_info(symbol):
    """Fetch detailed stock information"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/stocks/{symbol}/info")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def fetch_stock_analysis(symbol):
    """Fetch ML analysis for stock"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/stocks/{symbol}/analysis")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def fetch_stock_chart(symbol, interval="1d", period="1y"):
    """Fetch stock chart data"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/stocks/{symbol}/chart", 
                              params={"interval": interval, "period": period})
        return response.json() if response.status_code == 200 else None
    except:
        return None

def fetch_stock_news(symbol, limit=5):
    """Fetch stock news"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/stocks/{symbol}/news", 
                              params={"limit": limit})
        return response.json() if response.status_code == 200 else []
    except:
        return []

def search_stocks(query):
    """Search for stocks"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/stocks/search", 
                              params={"q": query, "limit": 20})
        return response.json() if response.status_code == 200 else []
    except:
        return []

def create_price_chart(chart_data, symbol):
    """Create interactive price chart"""
    if not chart_data or not chart_data.get('data'):
        return None
    
    df = pd.DataFrame(chart_data['data'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create subplots for price and volume
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(f'{symbol} Price', 'Volume'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name=symbol
        ),
        row=1, col=1
    )
    
    # Add volume bars
    fig.add_trace(
        go.Bar(
            x=df['timestamp'],
            y=df['volume'],
            name='Volume',
            marker_color='rgba(158, 185, 243, 0.6)'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"{symbol} Stock Chart",
        height=600,
        xaxis_rangeslider_visible=False,
        template="plotly_white"
    )
    
    return fig

def display_stock_metrics(stock_info):
    """Display key stock metrics"""
    if not stock_info:
        st.error("Unable to load stock information")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price", 
            f"${stock_info['current_price']:.2f}",
            delta=f"{stock_info['day_change']:.2f} ({stock_info['day_change_percent']:.2f}%)"
        )
    
    with col2:
        st.metric(
            "Market Cap", 
            f"${stock_info['market_cap']:,.0f}" if stock_info['market_cap'] else "N/A"
        )
    
    with col3:
        st.metric(
            "P/E Ratio", 
            f"{stock_info['pe_ratio']:.2f}" if stock_info.get('pe_ratio') else "N/A"
        )
    
    with col4:
        st.metric(
            "Volume", 
            f"{stock_info['volume']:,}" if stock_info['volume'] else "N/A"
        )

def display_analysis_summary(analysis):
    """Display ML analysis summary"""
    if not analysis:
        st.error("Unable to load analysis")
        return
    
    # Overall signal
    signal_colors = {
        "STRONG_BUY": "🟢", "BUY": "🟢", 
        "HOLD": "🟡", 
        "SELL": "🔴", "STRONG_SELL": "🔴"
    }
    
    signal_color = signal_colors.get(analysis['overall_signal'], "⚪")
    
    st.subheader(f"Analysis Summary {signal_color}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Signal", analysis['overall_signal'])
    
    with col2:
        st.metric("Confidence Score", f"{analysis['confidence_score']:.1f}%")
    
    with col3:
        st.metric("Risk Level", analysis['risk_level'])
    
    # Key insights
    if analysis.get('key_insights'):
        st.subheader("🔍 Key Insights")
        for insight in analysis['key_insights']:
            st.write(f"• {insight}")
    
    # Warnings
    if analysis.get('warnings'):
        st.subheader("⚠️ Warnings")
        for warning in analysis['warnings']:
            st.warning(warning)

def display_technical_indicators(analysis):
    """Display technical indicators"""
    if not analysis or not analysis.get('technical_indicators'):
        return
    
    st.subheader("📈 Technical Indicators")
    
    indicators_df = pd.DataFrame(analysis['technical_indicators'])
    
    for _, indicator in indicators_df.iterrows():
        col1, col2, col3 = st.columns([2, 1, 3])
        
        with col1:
            st.write(f"**{indicator['name']}**")
        
        with col2:
            signal_color = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡"}.get(indicator['signal'], "⚪")
            st.write(f"{signal_color} {indicator['signal']}")
        
        with col3:
            st.write(indicator['description'])

def display_news(news_items):
    """Display stock news"""
    if not news_items:
        st.info("No recent news available")
        return
    
    st.subheader("📰 Latest News")
    
    for item in news_items[:5]:  # Show top 5 news items
        with st.expander(item['title']):
            st.write(item.get('summary', 'No summary available'))
            if item.get('url'):
                st.write(f"[Read more]({item['url']})")
            st.write(f"*Source: {item.get('source', 'Unknown')} | Sentiment: {item.get('sentiment', 'neutral')}*")

def main():
    st.title("📊 Stock Analysis Dashboard")
    st.markdown("*Comprehensive stock analysis with ML-powered insights*")
    
    # Search and stock selection
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_query = st.text_input(
            "🔍 Search for a stock", 
            placeholder="Enter symbol (e.g., AAPL) or company name",
            help="Search by stock symbol or company name"
        )
    
    with search_col2:
        search_button = st.button("Search", type="primary")
    
    # Handle search
    selected_symbol = None
    
    if search_button and search_query:
        search_results = search_stocks(search_query)
        
        if search_results:
            st.subheader("Search Results")
            
            # Display search results in a nice format
            for stock in search_results[:10]:  # Show top 10 results
                col1, col2, col3 = st.columns([2, 3, 1])
                
                with col1:
                    if st.button(f"📈 {stock['symbol']}", key=stock['symbol']):
                        selected_symbol = stock['symbol']
                        st.session_state.selected_stock = stock['symbol']
                
                with col2:
                    st.write(f"**{stock.get('name', 'N/A')}**")
                    st.caption(f"Exchange: {stock.get('exchange', 'N/A')}")
                
                with col3:
                    st.write(stock.get('type', 'stock').upper())
        else:
            st.error("No stocks found matching your search.")
    
    # Use session state to maintain selected stock
    if not selected_symbol and 'selected_stock' in st.session_state:
        selected_symbol = st.session_state.selected_stock
    
    # Display stock analysis if a stock is selected
    if selected_symbol:
        st.markdown("---")
        st.header(f"Analysis for {selected_symbol}")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", "📈 Charts", "🤖 ML Analysis", "📰 News", "⚖️ Trading"
        ])
        
        with tab1:
            st.subheader("Company Overview")
            stock_info = fetch_stock_info(selected_symbol)
            
            if stock_info:
                # Display metrics
                display_stock_metrics(stock_info)
                
                # Company information
                st.subheader("Company Information")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Company:** {stock_info.get('name', 'N/A')}")
                    st.write(f"**Sector:** {stock_info.get('sector', 'N/A')}")
                    st.write(f"**Industry:** {stock_info.get('industry', 'N/A')}")
                    st.write(f"**Exchange:** {stock_info.get('exchange', 'N/A')}")
                
                with col2:
                    st.write(f"**CEO:** {stock_info.get('ceo', 'N/A')}")
                    st.write(f"**Employees:** {stock_info.get('employees', 'N/A'):,}")
                    st.write(f"**Website:** {stock_info.get('website', 'N/A')}")
                    st.write(f"**Headquarters:** {stock_info.get('headquarters', 'N/A')}")
                
                # Company description
                if stock_info.get('description'):
                    st.subheader("Description")
                    st.write(stock_info['description'])
            
        with tab2:
            st.subheader("Price Charts")
            
            # Chart timeframe selection
            col1, col2 = st.columns(2)
            
            with col1:
                interval = st.selectbox(
                    "Chart Interval",
                    ["1d", "1h", "30m", "15m", "5m", "1m"],
                    index=0,
                    help="Select chart interval"
                )
            
            with col2:
                period = st.selectbox(
                    "Chart Period",
                    ["1y", "6mo", "3mo", "1mo", "1d", "5d"],
                    index=0,
                    help="Select chart period"
                )
            
            # Fetch and display chart
            chart_data = fetch_stock_chart(selected_symbol, interval, period)
            
            if chart_data:
                fig = create_price_chart(chart_data, selected_symbol)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Unable to load chart data")
        
        with tab3:
            st.subheader("ML-Powered Analysis")
            
            # Fetch analysis
            analysis = fetch_stock_analysis(selected_symbol)
            
            if analysis:
                # Display analysis summary
                display_analysis_summary(analysis)
                
                # Technical indicators
                display_technical_indicators(analysis)
                
                # Price predictions
                if any([analysis.get('price_target_1d'), analysis.get('price_target_1w'), analysis.get('price_target_1m')]):
                    st.subheader("🎯 Price Predictions")
                    pred_col1, pred_col2, pred_col3 = st.columns(3)
                    
                    with pred_col1:
                        if analysis.get('price_target_1d'):
                            st.metric("1 Day Target", f"${analysis['price_target_1d']:.2f}")
                    
                    with pred_col2:
                        if analysis.get('price_target_1w'):
                            st.metric("1 Week Target", f"${analysis['price_target_1w']:.2f}")
                    
                    with pred_col3:
                        if analysis.get('price_target_1m'):
                            st.metric("1 Month Target", f"${analysis['price_target_1m']:.2f}")
            else:
                st.error("Unable to load ML analysis")
        
        with tab4:
            st.subheader("Latest News")
            news_items = fetch_stock_news(selected_symbol)
            display_news(news_items)
        
        with tab5:
            st.subheader("Ready to Trade?")
            st.info("📈 Ready to trade? Click below to access the Alpaca trading platform with paper trading.")
            
            if st.button("🚀 Go to Trading Platform", type="primary"):
                st.switch_page("app.py")  # Redirect to main trading app
            
            st.markdown("---")
            st.caption("⚠️ This analysis is for educational purposes only and should not be considered financial advice. Always do your own research and consult with financial advisors before making investment decisions.")

if __name__ == "__main__":
    main()
