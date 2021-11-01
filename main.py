# Imports all the modules and libraries required
# dash will be used in order to create the app, and output the graphs
import dash

# The following 3 imports are used in order to create the layout, divisions, graphs and headings and also to add the authentication to the dashboard
import dash_auth
from dash import html
from dash import dcc
from dash import dash_table

# Input and Output are used in order to facilitate the callbacks to update the graphs
from dash.dependencies import Input, Output

# imports the classes JiraInfo and StockInfo which has all the data  required to make the graphs
from StockInfo import StockInfo
from JiraInfo import JiraInfo

# The imported classes are then turned into objects
stock = StockInfo()
jira = JiraInfo()

# An external file sheet called Style.css is in the Directory in a folder called assets and this is automatically called by the dash module

# This creates the app using Dash
# It also sets the app title, it is shown in the tab name
app = dash.Dash(title="Jira Dashboard")

# This is used in order to ensure authenticaion is required before accesing the data
VALID_USERNAME_PASSWORD_PAIRS = {
    stock.username: stock.password,
}
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

# The layout contains all the content which will be output in the dashboard
# I have created a div for each module, and these are all within the 'outercontainer' div
app.layout = html.Div(
    id="outercontainer",
    children=[
        # The dcc.Interval components specify when each graph should update
        # These set the jira graphs to update each minute, and the stock ones to update every 3 minutes
        dcc.Interval(
            id="jirainterval", interval=60 * 1000, n_intervals=0  # in milliseconds
        ),
        dcc.Interval(
            id="stockinterval", interval=180 * 1000, n_intervals=0  # in milliseconds
        ),
        # Each module is contained within its own division in order to make styling easier
        # This is the title div which contains the title, Jira Dashboard, which is shown at the top
        html.Div(
            id="Title",
            children=[
                html.H1(
                    children=["Jira Dashboard"],
                )
            ],
        ),
        # This div contains the stock price which is a html h1 heading
        html.Div(
            id="StockPrice",
            children=[
                html.H1(
                    children=["StockPrice"],
                ),
                html.H1(id="PriceText", children=[stock.price]),
            ],
        ),
        # This div contains the assigneetable which is a table created by dash
        html.Div(
            id="AssigneeTable",
            children=[
                html.H1(
                    children=["AssigneeTable"],
                ),
                dash_table.DataTable(
                    id="AssigneeDataTable",
                    columns=[{"name": i, "id": i} for i in jira.assignee_columns],
                    data=jira.assignee_data,
                    style_cell={"color": "white", "text_align": "center"},
                ),
            ],
        ),
        # This div contains the issuetypebargraph which is a graph created by dash
        html.Div(
            id="IssueTypeBarGraph",
            children=[
                dcc.Graph(
                    id="IssueTypeGraph",
                    figure=jira.issuetype_figure,
                ),
            ],
        ),
        # This div contains the stockgraph which is a graph created by dash
        html.Div(
            id="StockGraph",
            children=[
                dcc.Graph(
                    id="StocksGraph",
                    figure=stock.stockgraph_figure,
                ),
            ],
        ),
        # This div contains the ProgressPieChart which is a graph created by plotly
        html.Div(
            id="ProgressPieChart",
            children=[
                dcc.Graph(
                    id="StatusPieChart",
                    figure=jira.piechart_figure,
                ),
            ],
        ),
    ],
)

# These are all the callbacks which allow the graphs to be updated
# Each callback takes the intervals as input, and updates the part of the graphs which contain data
@app.callback(Output("IssueTypeGraph", "figure"), Input("jirainterval", "n_intervals"))
def update_issuetype_bargraph(n_intervals):
    jira_update = JiraInfo()
    return jira_update.issuetype_figure


@app.callback(Output("StatusPieChart", "figure"), Input("jirainterval", "n_intervals"))
def update_progress_piechart(n_intervals):
    jira_update = JiraInfo()
    return jira_update.piechart_figure


@app.callback(Output("AssigneeDataTable", "data"), Input("jirainterval", "n_intervals"))
def update_assignee_datatable(n_intervals):
    jira_update = JiraInfo()
    return jira_update.assignee_data


@app.callback(Output("PriceText", "children"), Input("stockinterval", "n_intervals"))
def update_stock_price(n_intervals):
    stock_update = StockInfo()
    return stock_update.price


@app.callback(Output("StocksGraph", "figure"), [Input("stockinterval", "n_intervals")])
def update_data(n_intervals):
    stock_update = StockInfo()
    return stock_update.stockgraph_figure


# This final line is used in order to run the server which hosts the Dashboard
# It is run locally, on the page https
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)
