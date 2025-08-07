import streamlit as st
import requests

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"

# Page Configuration
st.set_page_config(
    page_title="Halal Money - Islamic Trading Platform",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def fetch_market_overview():
    """Fetch market overview data"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/market/overview")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def main():
    # Header
    st.title("🕌 Halal Money")
    st.subheader("Islamic Trading Platform with AI-Powered Stock Analysis")
    st.markdown("*Trade halal, invest wisely, grow sustainably*")
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Stock Analysis & Research", use_container_width=True, type="primary"):
            st.switch_page("pages/stock_analysis.py")
    
    with col2:
        if st.button("📈 Trading Dashboard", use_container_width=True):
            st.switch_page("pages/trading_dashboard.py")
    
    with col3:
        if st.button("ℹ️ About Platform", use_container_width=True):
            st.switch_page("pages/about.py")
    
    st.markdown("---")
    
    # Market Overview Section
    st.header("🌐 Market Overview")
    
    market_data = fetch_market_overview()
    
    if market_data and market_data.get('popular_stocks'):
        st.subheader("📈 Popular Stocks")
        
        # Display popular stocks in a nice table
        stocks_df = []
        for stock in market_data['popular_stocks']:
            stocks_df.append({
                'Symbol': stock['symbol'],
                'Company': stock['name'],
                'Price': f"${stock['price']:.2f}",
                'Change': f"{stock['change']:.2f}",
                'Change %': f"{stock['change_percent']:.2f}%",
                'Volume': f"{stock['volume']:,}" if stock['volume'] else 'N/A'
            })
        
        if stocks_df:
            st.dataframe(stocks_df, use_container_width=True, hide_index=True)
    else:
        st.info("Market data temporarily unavailable. Please check back later.")
    
    # Features Section
    st.markdown("---")
    st.header("🎯 Platform Features")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.subheader("🤖 AI-Powered Analysis")
        st.write("""
        - Technical indicator analysis
        - Price prediction models
        - Risk assessment
        - Sentiment analysis
        - Pattern recognition
        """)
    
    with feature_col2:
        st.subheader("📊 Comprehensive Data")
        st.write("""
        - Real-time stock prices
        - Historical charts
        - Company fundamentals
        - Financial news
        - Market trends
        """)
    
    with feature_col3:
        st.subheader("🛡️ Halal Trading")
        st.write("""
        - Sharia-compliant stocks
        - Paper trading practice
        - Risk management
        - Educational resources
        - Community insights
        """)
    
    # Quick Start Section
    st.markdown("---")
    st.header("🚀 Quick Start Guide")
    
    with st.expander("📖 How to get started"):
        st.markdown("""
        ### 1. Research Stocks 📊
        - Use our **Stock Analysis** page to research companies
        - Get AI-powered insights and technical analysis
        - Read latest news and market sentiment
        
        ### 2. Paper Trading 📈
        - Practice with virtual money on our **Trading Dashboard**
        - Test your strategies risk-free
        - Learn from real market conditions
        
        ### 3. Learn & Grow 📚
        - Study our technical indicators
        - Understand risk management
        - Follow halal investment principles
        
        ### 4. Go Live (Coming Soon) 🎯
        - Connect your real brokerage account
        - Apply your tested strategies
        - Trade with confidence
        """)
    
    # Important Disclaimers
    st.markdown("---")
    st.header("⚠️ Important Information")
    
    disclaimer_col1, disclaimer_col2 = st.columns(2)
    
    with disclaimer_col1:
        st.warning("""
        **Investment Risk Warning**
        
        All investments carry risk. Past performance does not guarantee future results. 
        Please consult with qualified financial advisors before making investment decisions.
        """)
    
    with disclaimer_col2:
        st.info("""
        **Halal Trading**
        
        This platform aims to facilitate Sharia-compliant trading. Please verify the 
        halal status of investments with qualified Islamic scholars.
        """)
    
    # Footer
    st.markdown("---")
    st.caption("Halal Money Platform • Empowering Islamic Finance • Built with ❤️")

if __name__ == "__main__":
    main()
