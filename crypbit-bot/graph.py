import plotly.graph_objects as go
import pandas_datareader as pdr
from datetime import datetime, timedelta

def plotGraph(tickerName, chartFile):
    now = datetime.now()
    start = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    end = now.strftime("%Y-%m-%d")
    data = pdr.get_data_yahoo(f"{tickerName}-{'USD'}", start, end)
    
    fig = go.Figure(
        data=[
            go.Candlestick(
                x = data.index,
                open=data.Open,
                high=data.High,
                low=data.Low,
                close=data.Close
            )
        ]
    )
    fig.update_layout(
        title=f"Statistics of {tickerName} over past 1 year",
        xaxis_title="Date",
        yaxis_title=f"Value of {tickerName}",
        xaxis_rangeslider_visible=False,
        title_x=0.5
    )
    fig.update_yaxes(tickprefix='$')
    fig.write_image(chartFile)
