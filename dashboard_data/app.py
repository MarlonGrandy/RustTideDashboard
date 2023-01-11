import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output
import numpy as np
from datetime import date
from datetime import datetime as dt

df = pd.read_csv('dashbaord/data/dahsboard_data.csv',
                 index_col=0, parse_dates=True).dropna()
df.index = pd.to_datetime(df['Date'])


# Initialise the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
                                  html.H2(
                                      'Narragansett Bay Rust Tide Data'),
                                  html.P(
                                      'Pick a week to view from the dropdown below.'),
                                  html.Div(
                                      className='div-for-dropdown',
                                      style={'color': '#1E1E1E'}),
                                  html.Div(
                                      className="div-for-dropdown",
                                      children=[
                                          dcc.DatePickerSingle(
                                              id='date-picker',
                                              min_date_allowed=date(
                                                  2016, 8, 29),
                                              max_date_allowed=date(
                                                  2023, 1, 1),
                                              initial_visible_month=date(
                                                  2015, 12, 27),
                                              date=dt(2016, 8, 29).date(),
                                          )
                                      ],
                                  ),
                              ]
                              ),
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  dcc.Graph(id='timeseries',
                                            config={'displayModeBar': False},
                                            animate=True,
                                            ),


                              ])
                 ])
    ]

)


@ app.callback(Output('timeseries', 'figure'),
               [Input('date-picker', 'date')])
def update_timeseries(selected_week):

    df_sub = df.dropna().loc[dt.strptime(selected_week, "%Y-%m-%d")]

    # trace.append(px.scatter_mapbox(df_sub.loc[selected_week], lat='Lat', lon='Long',
    # hover_data='Margalefidinium polykrikoides (Cells/L)'))

    return go.Figure(
        data=[
            Scattermapbox(lat=np.array(df_sub['Lat']),
                          lon=np.array(df_sub['Long']),
                          mode="markers",
                          hoverinfo='lon'
                          ),
        ],
        layout=Layout(
            mapbox_style="open-street-map",
            autosize=True,
            mapbox=dict(
                style="dark",
                center=dict(lat=41.57, lon=-71.39),
                zoom=9,
            ),
        )
    )


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
