import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np
import sys
sys.path.append("/Users/shodges/Documents/GitHub/hilltop-py/hilltoppy/")
import web_service as ws    
from datetime import datetime
import datetime as dt
import pytz
pytz.all_timezones

def get_now():
    tz_NZ = pytz.timezone('Pacific/Auckland') 
    datetime_NZ = datetime.now(tz_NZ)
    return datetime_NZ.strftime("%Y-%m-%d %H:%M")

def start_date(daysBeforeNow=7):
    tz_NZ = pytz.timezone('Pacific/Auckland') 
    datetime_NZ = datetime.now(tz_NZ)
    day_delta = dt.timedelta(days=daysBeforeNow)
    from_date = datetime_NZ - day_delta
    return from_date.strftime("%Y-%m-%d %H:%M")


def get_data(site):
    
    ### Parameters
    base_url = 'http://tsdata.horizons.govt.nz/'
    hts = 'boo.hts'
    measurement = 'Stage [Water Level]'
    from_date = start_date(1)
    to_date = get_now()
    #dtl_method = 'trend'
    
    df = ws.get_data(base_url,hts,site,measurement,from_date,to_date)
    # columns=['Site', 'Measurement', 'Parameter', 'DateTime', 'Value'])

    return df


def get_all_stage_data():
    base_url = 'http://tsdata.horizons.govt.nz/'
    hts = 'boo.hts'
    collection = 'River Level'
    from_date = start_date(1)
    to_date = get_now()
    df = ws.get_datatable(base_url, hts, collection, from_date=from_date, to_date=to_date)
    return df

#site = 'Manawatu at Teachers College'
#data = get_data(site)


# tidy up dataframe - index contains site, measurement, and datetime; Value is the only column
#l = data.index.tolist()
#df = pd.DataFrame(l)
#data = data.reset_index(drop=True)
#df = df.reset_index(drop=True)
#result = pd.concat([df, data], axis=1)
#result.columns = ["Site","Measurement","DateTime","Value"]
#result["Site"]='Manawatū at Teachers College'
##data = data.query("type == 'conventional' and region == 'Albany'")
#result["DateTime"] = pd.to_datetime(result["DateTime"], infer_datetime_format=True) #, format="%Y-%m-%d %H:%M:%S")
#result.sort_values("DateTime", inplace=True)

data = get_all_stage_data()
data["Time"] = pd.to_datetime(data["Time"],infer_datetime_format=True)
#data = data.query("SiteName == 'Manawatu at Teachers College'")


# Create an instance of the dash class
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
#        html.H1(children="River levels",),
#        html.P(
#                children="Changing river levels"
#            " over the last 7 days",
#        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Site name", className="menu-title"),
                        dcc.Dropdown(
                            id="sitename-filter",
                            options=[
                                {"label": site, "value": site}
                                for site in np.sort(data.SiteName.unique())
                            ],
                            value="Manawatu at Teachers College",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="riverlevel-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        """
        html.Div(
            dcc.Graph(
                id="riverlevel-chart",
                figure={
                    "data": [
                        {
                            "x": result["DateTime"],
                            "y": result["Value"],
                            "type": "lines",
                        },
                    ],
                    "layout": {"title": result["Site"][0]},
                },
            ),
        ),
        """
    ]
)
    
    

@app.callback(
    [Output("riverlevel-chart", "figure")],
    [
        Input("sitename-filter", "value"),
        """
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        """
    ],
)
def update_charts(sitename): #avocado_type, start_date, end_date):
    mask = (
        (data.SiteName == sitename)
    )
    filtered_data = data.loc[mask, :]
    riverlevel-chart-figure = {
        "data": [
            {
                "x": filtered_data["Time"],
                "y": filtered_data["M1"],
                "type": "lines",
                #"hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "River level plot",
                "x": 0.05,
                "xanchor": "left",
            },
            #"xaxis": {"fixedrange": True},
            #"yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return riverlevel-chart-figure


    
    
if __name__ == "__main__":
    app.run_server(debug=True)
