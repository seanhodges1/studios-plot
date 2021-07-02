# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np
import requests
import sys
import web_service as ws    
from datetime import datetime
import datetime as dt
import pytz
import urllib.parse

#pytz.all_timezones

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
    from_date = start_date(7)
    to_date = get_now()
    df = ws.get_data_basic(base_url,hts,site,measurement,from_date,to_date)
    # columns=['Site', 'Measurement', 'Parameter', 'DateTime', 'Value'])
    return df

def get_all_stage_data():
    base_url = 'http://tsdata.horizons.govt.nz/'
    hts = 'boo.hts'
    collection = 'River Level'
    from_date = start_date(3)
    to_date = get_now()
    df = ws.get_datatable(base_url, hts, collection, from_date=from_date, to_date=to_date)
    return df



#site = "Makino at Rata Street"
#data = get_data(site)
#data["T"] = pd.to_datetime(data["T"],infer_datetime_format=True)
##data['I1'] is type "str"
#data["Value"] = pd.to_numeric(data["I1"])/1000.0


#data = data.query("SiteName == 'Manawatu at Teachers College'")


# Create an instance of the dash class
app = dash.Dash(__name__)
# --- This line added for deployment to heroku
server = app.server
# ---

app.layout = html.Div([
                # represents the URL bar, doesn't render anything
                 dcc.Location(id='url', refresh=False),
#             
#                 dcc.Link('Navigate to "Makino at Rata Street"', href='/Makino%20at%20Rata%20Street'),
#                 html.Br(),
#                 dcc.Link('Navigate to "Manawatu at Hopelands"', href='/Manawatu%20at%20Hopelands'),
#             
# =============================================================================
                # content will be rendered in this element
#                html.Div(id='page-content') ,
#                         #hidden=True),
                dcc.Graph(
                    id="riverlevel-chart",
                    config={
                        'displayModeBar': False,
                    },
                ),
            ])   

@app.callback([
    Output("riverlevel-chart", "figure"),
    Output('page-content', 'children')
], [Input('url', 'pathname')])
    
def display_page(pathname):
    site = urllib.parse.unquote(pathname)[1:]
    data = get_data(urllib.parse.unquote(pathname)[1:])
    data["T"] = pd.to_datetime(data["T"],infer_datetime_format=True)
    #data['I1'] is type "str"
    data["Value"] = pd.to_numeric(data["I1"])/1000.0
    wl_figure = figure={
                         "data": [
                                 {
                                 "x": data["T"], 
                                 "y": data["Value"],
                                 "type": "lines",
                                 },
                        ],
                        "layout": {
                            "margin": {
                                    "l" : 80,
                                    "r" : 80,
                                    "t" : 20,
                                    "b" : 40},
                        "height" : 200,
                        'xaxis':{
                                'title':site
                             },
                        'yaxis':{
                                'title':'River level (m)'
                             }
                        },
                    }
    return wl_figure #, html.Div([

#        html.H3('You are on page {}'.format(site))
#    ])

    
if __name__ == "__main__":
    app.run_server(debug=True)
