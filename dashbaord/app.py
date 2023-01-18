# import statements
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output
from datetime import date
from datetime import datetime as dt

# reading in the data
df = pd.read_csv('data/dahsboard_data.csv',
                 index_col=0, parse_dates=True)
df = df.rename(columns={'MaxWSpd': 'Max Wind Speed (m/s)', 'WSpd': 'Average Wind Speed (m/s)',
               'TotPrcp': 'Total Precipitation (mm)', 'Temp': 'Average Sea Surface Temperature (°F)'})
df.index = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].astype(str)


# getting dropdown data for the sample map
def get_date_options():
    df_sub = df.dropna()
    dates = df_sub['Date'].unique()
    dict_list = []
    for i in dates:
        dict_list.append({'label': i, 'value': i})

    return dict_list


# getting dropdown data for the environmental timeseries data
def get_graph_options():
    graphs = ['Max Wind Speed (m/s)', 'Average Wind Speed (m/s)',
              'Average Sea Surface Temperature (°F)', 'Total Precipitation (mm)']
    dict_list = []
    for i in graphs:
        dict_list.append({'label': i, 'value': i})

    return dict_list


# getting dropdown data for the time period dropdown
def get_start_end_options():
    df_sub = df
    dates = df_sub['Date'].unique()
    dict_list = []
    for i in dates:
        dict_list.append({'label': i, 'value': i})

    return dict_list


# Initialise the app
app = dash.Dash(__name__)
server = app.server

# Define the app layout
app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
                                  html.H2(
                                      'Rhode Island Rust Tide Dashboard', style={'font-size': '20px'}),
                                  html.P(
                                      'Select infiormation to view from the dropdowns below:'),
                                  html.Div(
                                      className='div-for-dropdown',
                                      style={'color': '#1E1E1E'}),
                                  html.P(
                                      'Rust Tide Sample Date Dropdown', style={'font-size': '15px'}),
                                  html.Div(
                                      className="div-for-date-dropdown",
                                      children=[
                                          dcc.Dropdown(id='date-picker',
                                                       options=get_date_options(),
                                                       value='2016-08-29',
                                                       style={
                                                           'backgroundColor': '#1E1E1E'},
                                                       className='date-picker')
                                      ],

                                  ), html.P(
                                      'Environmnetal Condition Dropdown', style={"margin-top": "10px", 'font-size': '15px'}),
                                  html.Div(
                                      className="div-for-graph-dropdown",
                                      children=[
                                          dcc.Dropdown(id='graph-picker',
                                                       options=get_graph_options(),
                                                       value='Average Sea Surface Temperature (°F)',
                                                       style={
                                                           'backgroundColor': '#1E1E1E'},
                                                       className='graph-picker')

                                      ],
                                  ),
                                  html.Div(
                                      className="div-for-start-date",
                                      children=[
                                          dcc.Dropdown(id='start-picker',
                                                       options=get_start_end_options(),
                                                       value='2015-12-28',
                                                       style={
                                                           'backgroundColor': '#1E1E1E'},
                                                       className='start-picker')

                                      ],
                                  ),
                                  html.Div(
                                      className="div-for-end-date",
                                      children=[
                                          dcc.Dropdown(id='end-picker',
                                                       options=get_start_end_options(),
                                                       value='2022-12-19',
                                                       style={
                                                           'backgroundColor': '#1E1E1E'},
                                                       className='end-picker')

                                      ],
                                  ),
                                  html.H2('Project Information', style={
                                          "margin-top": "40px"}),
                                  html.P('This dashboard displays occurrences of the harmful algal bloom species Margalefidinium polykrikoides, also known as "rust tide". The dashboard features an interactive map showing the prevalence of rust tide in Narragansett Bay based on samples collected from three different sources.The goal of the dashboard is to create a foundational tool to gather all the data on "rust tide" in one location. Along with rust tide occurrences, the dashboard currently displays four environmental varaibles that may to contribute to rust tide occurrences. The data on "rust tide" is still limited as it is a relatively recent phenomenon. As more data becomes accessible, the dashboard will be updated.',
                                         style={'font-size': '14px'})
                              ]
                              ),
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  dcc.Graph(id='map',
                                            config={'displayModeBar': False},
                                          
                                            ),
                                  dcc.Graph(id='timeseries', config={
                                            'displayModeBar': False},
                                            )


                              ])
                 ])
    ]

)


# updating the scatter_mapbox plot with callbacks
@ app.callback(Output('map', 'figure'),
               [Input('date-picker', 'value')])
def update_map(selected_week):
    df_sub = df.dropna().loc[dt.strptime(
        selected_week, "%Y-%m-%d")].reset_index(drop=True)

    if len(df_sub) != 8:
        fig = px.scatter_mapbox(
            df_sub,
            lat='Lat',
            lon='Long',
            custom_data=['Margalefidinium polykrikoides (Cells/L)']
        ).update_layout(mapbox_style="carto-positron",
                        margin=dict(t=5, b=5, l=5, r=10), uirevision=True).update_traces(hovertemplate="longitude: %{lon}<br>" +
                                                                                         "latitude: %{lat}<br>" + "Margalefidinium polykrikoides (Cells/L): %{customdata[0]}<br>")

        return fig
    else:
        fig = px.scatter_mapbox(
            lat=df_sub.iloc[[2]],
            lon=df_sub.iloc[[3]],
            custom_data=[[df_sub.iloc[[4]]]],
        ).update_layout(mapbox_style="carto-positron",
                        margin=dict(t=5, b=5, l=5, r=10), uirevision=True).update_traces(hovertemplate="longitude: %{lon}<br>" +
                                                                                         "latitude: %{lat}<br>" + "Margalefidinium polykrikoides (Cells/L): %{customdata[0]}<br>")
        return fig


# updating the timeseries plot with callbacks
@ app.callback(Output('timeseries', 'figure'),
               Input('graph-picker', 'value'), Input('start-picker', 'value'), Input('end-picker', 'value'))
def update_timeseries(selected_graph, start_date, end_date):
    df_sub = df[(df['Date'] > start_date) & (df['Date'] < end_date)]
    df_sub = df_sub[[selected_graph, 'Date']]
    df_sub.dropna()

    fig = px.scatter(df_sub, x="Date", y=selected_graph,
                     template='plotly_dark').update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', },
                                                           margin=dict(t=5, b=5, l=5, r=10)).update_xaxes(showgrid=False).update_yaxes(showgrid=False)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
