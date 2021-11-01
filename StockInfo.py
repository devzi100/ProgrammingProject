# Imports used within the class JiraInfo
# Requests is used in order to perform the HTTP GET Request to Alpha Vantage
import requests

# JSON is used in order to convert the returned json text into a dictionary
import json

# Datetime is used in order to extract the times from the json file returned
from datetime import datetime

# StockInfo Class Creation
class StockInfo:
    def __init__(self) -> None:
        self.url = "https://www.alphavantage.co/query?"
        self.stock_data = self.get_stock_data()
        self.price = self.price_text()
        self.stockgraph_figure = self.stock_figure()
        self.username = 'admin'
        self.password = 'admin'

    # This takes the url in the init file, and uses the parameters specified to start a get request
    # This returns the price per minute of the 8x8 stock
    # Json will convert this data into the dictionary, which is returned
    def get_stock_data(self) -> dict:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "interval": "1min",
            "apikey": "W7SYSVIXB4FZZC77",
            "symbol": "eght",
        }
        response = requests.get(self.url, params=params)
        print(response.status_code)
        return json.loads(response.text)

    # This first creates a dictionary to store the times and prices in
    # It then iterates through each time within the data, and finds the corresponding price
    # The times are added to the dictionary as the keys, and the prices are added as values
    # If the x axis values are required, a list of the keys, in reverse order, is returned
    # If the y axis values are required, a list of the values, in reverse order, is returned
    def stock_line_graph(self, axis: chr) -> list:
        time_and_price = {}
        for value in self.stock_data["Time Series (1min)"]:
            time = str(datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
            time_and_price[time] = self.stock_data["Time Series (1min)"][value][
                "4. close"
            ]
        if axis == "x":
            return list(reversed(time_and_price.keys()))
        elif axis == "y":
            return list(reversed(time_and_price.values()))

    # This returns the current value of the 8x8 stock price, but just rounded
    def price_text(self) -> str:
        try:
            stock_y_values = self.stock_line_graph("y")
            return "$" + str(round(float(stock_y_values[-1]), 2))
        except:
            return "Loading..."

    # This function is used to return the figure used to create the graph in the main file
    # This is used in the initial creation of graphs and also the callback
    def stock_figure(self):
        try:
            stock_x_values = self.stock_line_graph("x")
            stock_y_values = self.stock_line_graph("y")
            return {
                "data": [
                    {
                        "x": stock_x_values,
                        "y": stock_y_values,
                        "type": "line",
                    },
                ],
                "layout": {
                    "title": "StocksGraph",
                    "showlegend": False,
                },
            }
        except:
            return {
                "layout": {
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                    "annotations": [
                        {
                            "text": "Loading...",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {"size": 28},
                        }
                    ],
                }
            }
