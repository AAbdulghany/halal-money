import streamlit as st

st.set_page_config(
    page_title="About - Halal Money",
    page_icon="ℹ️",
    layout="wide"
)

def main():
    st.title("ℹ️ About Halal Money Platform")
    
    # Navigation
    if st.button("← Back to Home"):
        st.switch_page("home.py")
    
    st.markdown("---")
    
    # Introduction
    st.header("🕌 Our Mission")
    st.write("""
    Halal Money is an Islamic trading platform that combines modern financial technology 
    with Sharia-compliant investment principles. Our mission is to empower Muslim investors 
    with the tools and knowledge they need to build wealth in a halal manner.
    """)
    
    # Features
    st.header("🎯 Platform Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.subheader("📊 Stock Analysis")
        st.write("""
        - **AI-Powered Analysis**: Machine learning algorithms analyze stocks
        - **Technical Indicators**: RSI, MACD, Bollinger Bands, and more
        - **Price Predictions**: Short and long-term price forecasts
        - **Risk Assessment**: Comprehensive risk evaluation
        - **News Sentiment**: Real-time news analysis with sentiment scoring
        """)
        
        st.subheader("📈 Trading Features")
        st.write("""
        - **Paper Trading**: Practice with virtual money
        - **Real-time Data**: Live market data and quotes
        - **Order Management**: Place, track, and manage orders
        - **Portfolio Tracking**: Monitor your investments
        - **Risk Management**: Built-in risk controls
        """)
    
    with feature_col2:
        st.subheader("🛡️ Halal Compliance")
        st.write("""
        - **Sharia Screening**: Focus on compliant investments
        - **Educational Resources**: Learn Islamic finance principles
        - **Scholar Guidance**: Access to Islamic finance experts
        - **Transparency**: Clear disclosure of investment practices
        - **Community**: Connect with like-minded investors
        """)
        
        st.subheader("🔧 Technology")
        st.write("""
        - **Free Data Sources**: No expensive subscriptions required
        - **Multiple APIs**: Redundant data sources for reliability
        - **Real-time Processing**: Fast and responsive platform
        - **Secure**: Industry-standard security practices
        - **Open Architecture**: Extensible and customizable
        """)
    
    # API Information
    st.header("🔌 Data Sources & APIs")
    st.write("""
    Our platform uses multiple free and reliable data sources to provide comprehensive market information:
    """)
    
    api_col1, api_col2, api_col3 = st.columns(3)
    
    with api_col1:
        st.subheader("📊 Market Data")
        st.write("""
        - **Yahoo Finance**: Free real-time and historical data
        - **Alpha Vantage**: Technical indicators and news
        - **Financial Modeling Prep**: Company fundamentals
        """)
    
    with api_col2:
        st.subheader("📰 News & Analysis")
        st.write("""
        - **NewsAPI**: Global financial news
        - **Alpha Vantage News**: Sentiment analysis
        - **Company Reports**: Earnings and announcements
        """)
    
    with api_col3:
        st.subheader("💹 Trading")
        st.write("""
        - **Alpaca API**: Commission-free paper trading
        - **Real-time Execution**: Fast order processing
        - **Portfolio Management**: Position tracking
        """)
    
    # Technical Architecture
    st.header("🏗️ Technical Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Backend (FastAPI)")
        st.write("""
        - **API Structure**: RESTful API design
        - **Stock Analysis**: `/api/stocks/` endpoints
        - **ML Analysis**: `/api/stocks/{symbol}/analysis`
        - **Trading**: `/alpaca/` endpoints (isolated)
        - **Real-time Data**: Multiple data source integration
        """)
    
    with col2:
        st.subheader("Frontend (Streamlit)")
        st.write("""
        - **Multi-page App**: Organized page structure
        - **Interactive Charts**: Plotly visualizations
        - **Real-time Updates**: Live market data display
        - **User-friendly Interface**: Intuitive design
        - **Mobile Responsive**: Works on all devices
        """)
    
    # Getting Started
    st.header("🚀 Getting Started")
    
    with st.expander("📋 Setup Instructions"):
        st.markdown("""
        ### Prerequisites
        - Python 3.8+
        - API Keys (optional for enhanced features):
          - Alpha Vantage API Key
          - NewsAPI Key
          - Financial Modeling Prep API Key
          - Alpaca API Keys (for trading)
        
        ### Installation
        1. Clone the repository
        2. Install dependencies: `pip install -r requirements.txt`
        3. Set up API keys in environment variables
        4. Run backend: `uvicorn backend.main:app --reload`
        5. Run frontend: `streamlit run frontend/home.py`
        
        ### Configuration
        - Set API keys in environment variables or `.env` file
        - Configure Alpaca for paper trading
        - Customize analysis parameters as needed
        """)
    
    # Disclaimer
    st.header("⚠️ Important Disclaimers")
    
    disclaimer_col1, disclaimer_col2 = st.columns(2)
    
    with disclaimer_col1:
        st.error("""
        **Investment Risk Warning**
        
        - All investments carry risk of loss
        - Past performance doesn't guarantee future results
        - Conduct your own research
        - Consult qualified financial advisors
        - Only invest what you can afford to lose
        """)
    
    with disclaimer_col2:
        st.warning("""
        **Halal Compliance Notice**
        
        - This platform aims to facilitate Sharia-compliant trading
        - Verify halal status with qualified Islamic scholars
        - Investment decisions are your responsibility
        - Platform provides tools, not religious guidance
        - Seek Islamic finance expertise for complex matters
        """)
    
    # Contact
    st.header("📞 Contact & Support")
    st.write("""
    For questions, support, or contributions:
    
    - **GitHub**: Check the repository for issues and contributions
    - **Documentation**: Refer to README.md and code comments
    - **Community**: Join discussions in the issues section
    - **Islamic Finance**: Consult qualified scholars for religious guidance
    """)
    
    # Footer
    st.markdown("---")
    st.caption("Halal Money Platform • Open Source • Built with ❤️ for the Muslim Community")

if __name__ == "__main__":
    main()
