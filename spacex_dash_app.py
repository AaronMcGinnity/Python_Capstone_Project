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
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site_dropdown',
                                options=[{'label':'All Sites', 'value':'ALL'},
                                {'label': 'CCAFS LC-40','value': 'CCAFS LC-40'},
                                {'label': 'CCAFS SLC-40','value': 'CCAFS SLC-40'},
                                {'label': 'KSC LC-39A','value': 'KSC LC-39A'},
                                {'label': 'VAFB SLC-4E','value': 'VAFB SLC-4E'}],
                                value='ALL',
                                placeholder='Select launch site',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success_pie_chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',
                                min=0, max=10000, step=1000, value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success_payload_scatter_chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success_pie_chart', component_property='figure'),
    Input(component_id='site_dropdown', component_property='value')
)

# Create a fuction to generate the pie chart.
def generate_pie_chart (site_dropdown):
    # Define the dataframe within the function
    filtered_df = spacex_df
    # Set up condition based on whether dropdown is set to All sites or a particular site
    if site_dropdown == 'ALL':
        # If all, look at the distribution of total successfuly launches. First do this by
        # grouping the data by each launch site.
        #All_Sites_df = filtered_df[filtered_df['class'] == 1].groupby('Launch Site').size().reset_index(name='counts')
        # Create the pie chart using the row counts and launch site names.
        fig = px.pie(filtered_df,values='class', names='Launch Site',
        title='No. Successful Launches by Site')
        return fig

    # Now set up the pie generation for single launch sites
    else:
        # Filter the dataset to get only the specified launch site and split by the 
        # success and failures using the class field.
        One_Site_df = filtered_df[filtered_df['Launch Site'] == site_dropdown].groupby('class').size().reset_index(name='counts')
        fig =px.pie(One_Site_df,values='counts',names='class',
        title='Split by Success and Failures for Launch Site', color='class')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success_payload_scatter_chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value'), 
    Input(component_id="payload_slider", component_property='value')]
)

# Create function to generate scatterplots
def generate_scatter_plot (site_dropdown, payload_slider):
    # Copy in the dataframe
    filtered_df = spacex_df

    # Add in the slider to select payload range
    low, high = payload_slider

    # Create condition to select the scatter plot depending on whether all sites are
    # selected or just one site.
    if site_dropdown == 'ALL':

        # Collect the necessary data using the range.
        #scatter_range = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)

        # Create the figure
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',y='class',
        color='Booster Version Category')
        return fig

    else:
        # Collect the necessary data using the range and subsetting based on the 
        # selected launch site.
        launch_df = filtered_df[filtered_df['Launch Site'] == site_dropdown]
        scatter_range = (launch_df['Payload Mass (kg)'] > low) & (launch_df['Payload Mass (kg)'] < high)

        # Create the figure
        fig = px.scatter(launch_df[scatter_range], x='Payload Mass (kg)',y='class',
        color='Booster Version Category')
        return fig 


# Run the app
if __name__ == '__main__':
    app.run_server()
