import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import datetime  # Add this import statement
from plotly import graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly
import time
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

def add_meta_tag():
    meta_tag = """
        <head>
            <meta name="google-site-verification" content="QBiAoAo1GAkCBe1QoWq-dQ1RjtPHeFPyzkqJqsrqW-s" />
        </head>
    """
    st.markdown(meta_tag, unsafe_allow_html=True)

# Main code
add_meta_tag()

# Sidebar Section Starts Here
today = date.today()  # today's date
st.write('''# Financial Companion ''')  # title
st.sidebar.image("Images/image.png", width=250,
                 use_column_width=False)  # logo
st.sidebar.write('''# Financial Companion''')

with st.sidebar: 
        selected = option_menu("Utilities", ["Stocks Performance Comparison", "Real-Time Stock Price", "Stock Prediction", 'About'])

start = st.sidebar.date_input('Start', datetime.date(2022, 1, 1))  # start date input
end = st.sidebar.date_input('End', today)  # end date input
# Sidebar Section Ends Here

# read csv file
stock_df = pd.read_csv("StockStreamTickersData.csv")

# Stock Performance Comparison Section Starts Here
if(selected == 'Stocks Performance Comparison'):  # if user selects 'Stocks Performance Comparison'
    st.subheader("Stocks Performance Comparison")
    tickers = stock_df["Company Name"]
    # dropdown for selecting assets
    dropdown = st.multiselect('Pick your assets', tickers)

    with st.spinner('Loading...'):  # spinner while loading
        time.sleep(2)

    dict_csv = stock_df.set_index("Company Name").T.to_dict("records")[0]  # read csv file
    symb_list = [dict_csv[i] for i in dropdown if i in dict_csv]  # list for storing symbols

    def relativeret(df):  # function for calculating relative return
        rel = df.pct_change()  # calculate relative return
        cumret = (1+rel).cumprod() - 1  # calculate cumulative return
        cumret = cumret.fillna(0)  # fill NaN values with 0
        return cumret  # return cumulative return

    if len(dropdown) > 0:  # if user selects at least one asset
        data = yf.download(symb_list, start=start, end=end)
        df = relativeret(data)['Adj Close']  # calculate relative returns
        raw_df = relativeret(data)
        raw_df.reset_index(inplace=True)  # reset index

        closingPrice = data['Adj Close']
        volume = data['Volume']

        st.subheader('Raw Data {}'.format(dropdown))
        st.write(raw_df)  # display raw data
        chart = ('Line Chart', 'Area Chart', 'Bar Chart')  # chart types
        dropdown1 = st.selectbox('Pick your chart', chart)

        with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

        st.subheader('Relative Returns {}'.format(dropdown))

        if dropdown1 == 'Line Chart':
            st.line_chart(df)
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)

        elif dropdown1 == 'Area Chart':
            st.area_chart(df)
            st.write("### Closing Price of {}".format(dropdown))
            st.area_chart(closingPrice)
            st.write("### Volume of {}".format(dropdown))
            st.area_chart(volume)

        elif dropdown1 == 'Bar Chart':
            st.bar_chart(df)
            st.write("### Closing Price of {}".format(dropdown))
            st.bar_chart(closingPrice)
            st.write("### Volume of {}".format(dropdown))
            st.bar_chart(volume)

        else:
            st.line_chart(df)
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)

    else:  # if user doesn't select any asset
        st.write('Please select at least one asset')  # display message
# Stock Performance Comparison Section Ends Here

# Real-Time Stock Price Section Starts Here
elif(selected == 'Real-Time Stock Price'):
    st.subheader("Real-Time Stock Price")
    tickers = stock_df["Company Name"]  # get company names from csv file
    a = st.selectbox('Pick a Company', tickers)

    with st.spinner('Loading...'):  # spinner while loading
        time.sleep(2)

    dict_csv = stock_df.set_index("Company Name").T.to_dict("records")[0]  # read csv file
    symb_list = [dict_csv[a]] if a in dict_csv else []  # get symbol from csv file

    if "button_clicked" not in st.session_state:  # if button is not clicked
        st.session_state.button_clicked = False  # set button clicked to false

    def callback():
        st.session_state.button_clicked = True

    if st.button("Search", on_click=callback) or st.session_state.button_clicked:
        if not a:
            st.write("Click Search to Search for a Company")
            with st.spinner('Loading...'):
                time.sleep(2)
        else:
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)
            st.subheader('Raw Data of {}'.format(a))
            st.write(data)

            def plot_raw_data():
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
                fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
                fig.layout.update(title_text='Line Chart of {}'.format(a), xaxis_rangeslider_visible=True)
                st.plotly_chart(fig)

            def plot_candle_data():
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'],
                                             low=data['Low'], close=data['Close'], name='market data'))
                fig.update_layout(title='Candlestick Chart of {}'.format(a), yaxis_title='Stock Price', xaxis_title='Date')
                st.plotly_chart(fig)

            chart = ('Candle Stick', 'Line Chart')
            dropdown1 = st.selectbox('Pick your chart', chart)

            with st.spinner('Loading...'):
                time.sleep(2)
            if dropdown1 == 'Candle Stick':
                plot_candle_data()
            elif dropdown1 == 'Line Chart':
                plot_raw_data()
            else:
                plot_candle_data()
# Real-Time Stock Price Section Ends Here

# Stock Price Prediction Section Starts Here
elif(selected == 'Stock Prediction'):
    st.subheader("Stock Prediction")

    tickers = stock_df["Company Name"]
    a = st.selectbox('Pick a Company', tickers)

    with st.spinner('Loading...'):
        time.sleep(2)

    dict_csv = stock_df.set_index("Company Name").T.to_dict("records")[0]
    symb_list = [dict_csv[a]] if a in dict_csv else []

    if not a:
        st.write("Enter a Stock Name")
    else:
        data = yf.download(symb_list, start=start, end=end)
        data.reset_index(inplace=True)
       
        # Continue with the stock prediction code...
        df_train = data[['Date','Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)

        future = m.make_future_dataframe(periods=365)
        forecast = m.predict(future)

        st.subheader('Forecast Data')
        st.write(forecast.tail())

        st.write(f'Forecast plot for {a}')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        st.write("Forecast components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)

# About Section Starts Here
elif(selected == 'About'):
    st.write("""
    ## StockStream Application
    This application allows you to visualize and predict stock market data.
    
    ### Utilities Provided:
    - **Stocks Performance Comparison:** Compare the performance of multiple stocks over a selected time period.
    - **Real-Time Stock Price:** View the real-time stock prices and historical data for a selected stock.
    - **Stock Prediction:** Predict future stock prices using the Prophet forecasting tool.

    ### Developers:
    - Developer 1: Aditi
    - Developer 2: [Your Name]
    """)
# About Section Ends Here
