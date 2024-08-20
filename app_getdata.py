import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc  # conda install conda-forge::dash-bootstrap-components
import pandas as pd
import numpy as np
import requests
import sys
import web_service as ws    
from datetime import datetime
import datetime as dt
import pytz
import dash_daq as daq

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
    base_url = 'https://extranet.trc.govt.nz/getdata/'
    hts = 'telemetry.hts'
    measurement = 'Stage [Water Level]'
    from_date = start_date(7)
    to_date = get_now()
    #dtl_method = 'trend'
    
    df = ws.get_data_basic(base_url,hts,site,measurement,from_date,to_date)
    # columns=['Site', 'Measurement', 'Parameter', 'DateTime', 'Value'])

    return df

def get_all_stage_data():
    base_url = 'http://tsdata.horizons.govt.nz/'
    hts = 'boo.hts'
    collection = 'River Level'
    base_url = 'https://extranet.trc.govt.nz/getdata/'
    hts = 'telemetry.hts'
    collection = 'WebRivers'
    from_date = start_date(3)
    to_date = get_now()
    df = ws.get_datatable(base_url, hts, collection, from_date=from_date, to_date=to_date)
    return df

def get_thresholds(site):
    # import threshold file
    df = pd.read_csv("thresholds.csv")
    df = df.query("SiteName == '"+site+"'")
    return df


site = "Makino at Rata Street"
site = "Manawatu at Teachers College"
data = get_data(site)
data["T"] = pd.to_datetime(data["T"],infer_datetime_format=True)
#data = data.query("SiteName == 'Manawatu at Teachers College'")
thresholds = get_thresholds(site)
#print(thresholds.head)
#print("Number of rows:"+str(len(thresholds.index)))
# Create an instance of the dash class
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# --- This line added for deployment to heroku
server = app.server
# ---

app.layout = html.Div(
    dbc.Row(
            [
                dbc.Col(html.Div([dcc.Graph(
                    id="riverlevel-chart",
                    figure={
                            "data": [
                                    {
                                    "x": data["T"], 
                                    "y": data["I1"],
                                    "type": "lines",
                                    }],
                        
                         "layout": {
                            "margin": {
                                    "l" : 80,
                                    "r" : 80,
                                    "t" : 20,
                                    "b" : 40},
                            "height" : 200}
                  })]), width=10),
                dbc.Col(html.Div(
                    daq.Tank(
                        value=3,
                        scale={'interval': 2, 'labelInterval': 2,
                            'custom': {'5': 'Set point'}},
                        style={'margin-left': '50px'}
                    )), width=2)
            ]))


    
if __name__ == "__main__":
    app.run_server(debug=True)
