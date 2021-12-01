# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()



# Create a dash application
app = dash.Dash(__name__)

# Create an app layout

sites=spacex_df['Launch Site'].unique().tolist()
sites.insert(0,'All Sites')




app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                   id='site-dropdown',
                                   options=[
                                    {'label': i, 'value': i} for i in sites],
                                    placeholder="Select a Launch Site here",
                                    value='All Sites',
                                    searchable=True),
                            
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0,
                                max=10000,
                                step=1000,
                                value=[min_payload,max_payload],
                                marks={
                                0: '0 kg',
                                2500: '2500',
                                5000: '5000',
                                7500: '7500',
                                10000: '10000'
                                }),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value')
)
def get_pie(value):
    filtered_df = spacex_df
    if value == 'All Sites':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == value].groupby(['Launch Site', 'class']). \
        size().reset_index(name='class count')
        title = f"Total Success Launches for site {value}"
        fig = px.pie(filtered_df,values='class count', names='class', title=title)
        return fig

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
Output(component_id='success-payload-scatter-chart', component_property='figure'),
[Input(component_id='site-dropdown', component_property='value'),
Input(component_id='payload-slider', component_property='value')]
)

def get_scatter(value1,value2):
    filtered_df2_1=spacex_df[(spacex_df['Payload Mass (kg)'] > value2[0]) & (spacex_df['Payload Mass (kg)'] < value2[1])]

    if value1=='All Sites':
        fig= px.scatter(filtered_df2_1,x="Payload Mass (kg)",y="class",color="Booster Version Category",\
        title="Correlation between Payload and Success for All sites")
        return fig
    else :
        filtered_df2_2=filtered_df2_1[filtered_df2_1['Launch Site']==value1]
        fig= px.scatter(filtered_df2_2,x="Payload Mass (kg)",y="class",color="Booster Version Category",\
        title=f"Correlation between Payload and Success for site {value1}")
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()