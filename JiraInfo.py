# Imports used within the class JiraInfo
# Requests is used in order to perform the HTTP GET Request to Jira
import requests

# JSON is used in order to convert the returned json text into a dictionary
import json

# Pie is used in order to create the pie chart in the progress figure
from plotly.graph_objects import Pie


# JiraInfo Class Creation
class JiraInfo:
    def __init__(self) -> None:
        self.data = self.get_data()
        self.issuetype_x_values = self.issuetype_and_progress_values("issuetype", "x")
        self.issuetype_y_values = self.issuetype_and_progress_values("issuetype", "y")
        self.status_x_values = self.issuetype_and_progress_values("status", "x")
        self.status_y_values = self.issuetype_and_progress_values("status", "y")
        self.assignee_data = self.assignee_datatable()
        self.assignee_columns = ["name", "count", "percentage"]
        self.issuetype_figure = self.issuetype_figure()
        self.piechart_figure = self.piechart_figure()

    # Function used to get the request the data from my mock Jira website
    # The URL uses the rest api built into jira, this is where the request needs to be sent
    # The headers are put with the request, this specifies the data type and includes the basic auth
    # The basic auth code is required to authenticate the request
    # Requests uses its GET function in order to perform a HTTP GET request
    # This function will return the data in json format
    def get_data(self) -> dict:
        url = "https://deven-dattani.atlassian.net/rest/api/2/search"
        headers = {
            "Accept": "application/json",
            "Authorization": "Basic ZGV2emkxMDFAZ21haWwuY29tOlRkTXVRdUV3N2pxY3dlU1lXeWRYQjQ2NQ==",
        }
        response = requests.get(url, headers=headers)
        self.responsecode = response.status_code
        return json.loads(response.text)

    # This function takes two parameters, issuetype or status which has to be either 'issuetype' or 'status'
    # It also takes in axis, which should be either 'x' or 'y'
    # Firstly, the dictionary is created, this will contain the category, and the amount of issues in this category
    # Then it filters through each issue within the data and extracts the name of the issuetype or status
    # These names are all added to the dictionary as keys
    # They are also counted and these values go into the dictionary as values
    # They are then returned in list form
    def issuetype_and_progress_values(
        self, issuetype_or_status: str, axis: chr
    ) -> list:
        name_and_count = {}
        for issueIndex in range(self.data["total"]):
            name = self.data["issues"][issueIndex]["fields"][issuetype_or_status][
                "name"
            ]
            if name not in name_and_count:
                name_and_count[name] = 0
            name_and_count[name] = name_and_count[name] + 1
        if axis == "x":
            return list(name_and_count.keys())
        elif axis == "y":
            return list(name_and_count.values())

    # This function is used to return the figure used to create the graph in the main file
    # This is used in the initial creation of graphs and also the callback
    def issuetype_figure(self):
        return {
            "data": [
                {
                    "x": self.issuetype_x_values,
                    "y": self.issuetype_y_values,
                    "type": "bar",
                    "marker": {
                        "color": [
                            "lightslategray",
                            "crimson",
                            "orange",
                            "green",
                            "silver",
                            "red",
                        ]
                        * 30
                    },
                },
            ],
            "layout": {
                "title": "IssueTypeBarGraph",
                "showlegend": False,
            },
        }

    # This function is used to return the figure used to create the graph in the main file
    # This is used in the initial creation of graphs and also the callback
    def piechart_figure(self):
        return {
            "data": [
                Pie(
                    labels=self.status_x_values,
                    values=self.status_y_values,
                    textinfo="label+value",
                ),
            ],
            "layout": {
                "title": "ProgressPieChart",
                "showlegend": False,
            },
        }

    # First, I create the dictionary where the assignee name will be the key, and the number of issues assigned to them will be the value
    # Then the program goes through each issue, and finds the assignee names and values
    # It then places these in the dictionary.
    # Then, the name, count and percentages are added to a separate dictionary, which in turn is added to a list
    # This list is the format necessary for Dash, and needs to be output
    def assignee_datatable(self) -> list:
        assignees, tabledata = {}, []
        for issueIndex in range(0, self.data["total"]):
            if (self.data["issues"][issueIndex]["fields"]["assignee"]) is None:
                name = "unassigned"
            else:
                name = self.data["issues"][issueIndex]["fields"]["assignee"][
                    "displayName"
                ]
            if name not in assignees:
                assignees[name] = 0
            assignees[name] = assignees[name] + 1
        for name in assignees:
            assignee = {
                "name": name,
                "count": assignees[name],
                "percentage": str(round((assignees[name]) / self.data["total"], 2))
                + "%",
            }
            tabledata.append(assignee)
        return tabledata
