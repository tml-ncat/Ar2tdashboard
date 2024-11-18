import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import json
import numpy as np
import os



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'])
server = app.server

# Get the directory where app.py is located (the src folder)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to NC_data.gpkg relative to the src folder
data_file_path = os.path.join(script_dir, 'data/NC_data.gpkg')

# Load the data
census_tracts = gpd.read_file(data_file_path)

# Ensure 'GEOID' exists or create it from existing columns
if 'GEOID' not in census_tracts.columns:
    census_tracts['GEOID'] = census_tracts['FIPS'].astype(str)

# Get list of counties for dropdown
counties = sorted(census_tracts['COUNTY'].unique())

# Default weights
default_weights = {'PI': 0.6, 'DI': 0.3, 'SVI': 0.1}

# Default average metrics
average_metrics = {
    'Physical Infrastructure': census_tracts['S_PI'].mean(),
    'Digital Infrastructure': census_tracts['S_DI'].mean(),
    'Social Vulnerability Index': census_tracts['S_SVI'].mean()
}

# Layout: Tabs for Map View, Comparison view and Documentation
app.layout = html.Div([
    html.Div([

    # Full-page container for the entire screen layout
     html.Div([

        # Header section (Logo on the right, Text on the left)
        html.Div([
            html.Div([  # Left-side: logo
                html.Img(src='assets/logo.png', className='logo'),
            ], className='header-left'),

            html.Div([  # Right-side: Logo2
                html.Img(src='assets/CR2C2 logo transparent.png', className='logo2'),
            ], className='header-right'),
        ], className='header'),

        # Add the horizontal line below the logos
        html.Hr(className='divider'),  # Divider line

        

        # Tabs go here, after the logo and header
        dcc.Tabs([

            # Add this as a new first tab in your dcc.Tabs section
            dcc.Tab(label='Welcome', className='tab-style1', children=[
                html.Div([
                    # Welcome header
                    html.Div([
                        html.H1('Welcome to the Rural Autonomous Vehicle Readiness Assessment Tool', 
                            className='text-center', 
                            style={'fontSize': '2.2rem', 'marginBottom': '1rem', 'color': 'white'}),
                        html.P('Evaluate your community\'s readiness for autonomous vehicle deployment',
                            className='text-center',
                            style={'fontSize': '1.2rem', 'color': '#d1d1d1', 'marginBottom': '2rem'})
                    ], className='welcome-header'),

                    # Main content grid
                    html.Div([
                        # Left Column
                        html.Div([
                            # About the Tool Card
                            html.Div([
                                html.H2('About This Tool', 
                                    style={'fontSize': '1.5rem', 'marginBottom': '1rem', 'color': 'white'}),
                                html.P('This tool assesses rural North Carolina communities\' readiness for autonomous vehicle deployment using three key dimensions:',
                                    style={'marginBottom': '1rem', 'color': '#d1d1d1'}),
                                html.Ul([
                                    html.Li([
                                        html.Span(['Physical Infrastructure (', html.I('w'), html.Sub('1'), '=0.6)'], style={'color': '#FFA500'}),
                                        ': Includes unpaved road percentage, road improvement efforts, bridge conditions, and pavement marking retroreflectivity'
                                    ]),
                                    html.Li([
                                        html.Span(['Digital Infrastructure (', html.I('w'), html.Sub('2'), '=0.3)'], style={'color': '#90EE90'}),
                                        ': Measures network latency, download speeds, and upload speeds relative to AV operational requirements'
                                    ]),
                                    html.Li([
                                        html.Span(['Social Vulnerability (', html.I('w'), html.Sub('3'), '=0.1)'], style={'color': '#87CEEB'}),
                                        ': Considers percentage of households without vehicles and population aged 65+'
                                    ]),
                                    html.Li([
                                        html.I('w'), html.Sub('1'), ' + ', 
                                        html.I('w'), html.Sub('2'), ' + ',
                                        html.I('w'), html.Sub('3'), ' = 1'
                                    ], style={'fontStyle': 'normal', 'marginTop': '0.5rem'})
                                ], style={'listStyleType': 'disc', 'paddingLeft': '2rem', 'color': '#d1d1d1'})
                            ], className='welcome-card'),

                            # Input Metrics Card
                            html.Div([
                                html.H2('Key Input Metrics', 
                                    style={'fontSize': '1.5rem', 'marginBottom': '1rem', 'color': 'white'}),
                                html.Ul([
                                    html.Li([
                                        html.Span('Unpaved Road Percentage', style={'color': '#FFA500'}),
                                        ': Proportion of unpaved roads relative to the total road network length within each census tract'
                                    ]),
                                    html.Li([
                                        html.Span('Road Improvement Percentage', style={'color': '#FFA500'}),
                                        ': Length of planned road improvements compared to total road length, with scores based on road condition and improvement effort'
                                    ]),
                                    html.Li([
                                        html.Span('Retroreflectivity Score', style={'color': '#FFA500'}),
                                        ': Percentage of roads meeting the nighttime visibility safety standard (Avg_RL ≥ 100), combined with road condition data'
                                    ]),
                                    html.Li([
                                        html.Span('Bridge Condition Percentage', style={'color': '#FFA500'}),
                                        ': Percentage of bridges classified in good condition within each area'
                                    ]),
                                    html.Li([
                                        html.Span('Broadband Network Performance', style={'color': '#90EE90'}),
                                        ': Maximum upload/download speeds (benchmark: 1000 Mbps) and minimum latency (benchmark: 10 ms) as percentages for each tract'
                                    ]),
                                    html.Li([
                                        html.Span('Social Vulnerability Index', style={'color': '#87CEEB'}),
                                        ': Combined percentage of households without a vehicle and individuals aged 65 or older in each census tract'
                                    ])
                                ], style={'listStyleType': 'disc', 'paddingLeft': '2rem'})

                            ], className='welcome-card')
                            
                        ], className='welcome-column'),

                        # Right Column
                        html.Div([
                            # How to Use Card
                            html.Div([
                                html.H2('How to Use This Tool', 
                                    style={'fontSize': '1.5rem', 'marginBottom': '1rem', 'color': 'white'}),
                                html.Div([
                                    html.H4('1. Map View', style={'color': '#87CEEB', 'marginBottom': '0.5rem', 'fontWeight': 'bold'}),
                                    html.Ul([
                                        html.Li(['Customize weights for each dimension (', 
                                        html.I('w'), html.Sub('1'), ' + ', 
                                        html.I('w'), html.Sub('2'), ' + ',
                                        html.I('w'), html.Sub('3'), ' = 1)']
                                        ),
                                        html.Li('Select granularity (county or census tract level)'),
                                        html.Li('Select counties for detailed analysis and visualize specific metrics')
                                    ], style={'listStyleType': 'disc', 'paddingLeft': '2rem', 'color': '#d1d1d1', 'marginBottom': '1rem'})
                                ]),
                                html.Div([
                                    html.H4('2. Comparison View', style={'color': '#87CEEB', 'marginBottom': '0.5rem', 'fontWeight': 'bold'}),
                                    html.Ul([
                                        html.Li('Compare readiness between different counties or against the statewide average'),
                                        html.Li('Analyze detailed metrics through radar charts'),
                                        html.Li('View comprehensive readiness insights')
                                    ], style={'listStyleType': 'disc', 'paddingLeft': '2rem', 'color': '#d1d1d1'})
                                ])
                            ], className='welcome-card'),

                            # Readiness Levels Card
                            html.Div([
                                html.H2('Understanding Readiness', 
                                    style={'fontSize': '1.5rem', 'marginBottom': '1rem', 'color': 'white'}),
                                html.Div([
                                    html.P('100% Readiness:', style={'color': '#90EE90', 'display': 'inline'}),
                                    html.P(' All roads paved, good bridge conditions, optimal retroreflectivity (≥100), excellent broadband coverage (relative to 1000 Mbps speeds and 10ms latency), and high transportation access',
                                        style={'color': '#d1d1d1', 'display': 'inline'})
                                ], style={'marginBottom': '1rem'}),
                                html.Div([
                                    html.P('0% Readiness:', style={'color': '#FF6B6B', 'display': 'inline'}),
                                    html.P(' Unpaved roads, poor infrastructure conditions, inadequate broadband, and limited transportation access',
                                        style={'color': '#d1d1d1', 'display': 'inline'})
                                ])
                            ], className='welcome-card')
                        ], className='welcome-column')
                    ], className='welcome-grid'),

                    # Acknowledgements Footer (outside the grid)
                    html.Div([
                        html.Hr(style={'margin': '1rem 0', 'border-color': '#333'}),
                        html.Div([
                            html.P([
                                'This research was supported by the ',
                                html.A('Center for Rural and Regional Connected Communities', 
                                    href='https://www.cr2c2.com/',
                                    target='_blank',
                                    style={'color': '#87CEEB', 'textDecoration': 'underline'}),
                                ' (CR2C2), a Regional University Transportation Center funded by the United States Department of Transportation (USDOT). The primary design for the tool was developed by Oladimeji Basit Alaka, and refined by the inputs from the project 1-1 team.'
                            ], style={'fontSize': '0.9rem', 'color': '#d1d1d1', 'marginBottom': '0.3rem'}),
                            html.P([
                                'Project 1-1 Team: ',
                                html.Br(),
                                'Principal Investigators: Dr. Jerry Everett (Lead PI), University of Tennessee, Knoxville; Dr. Asad Khattak, University of Tennessee, Knoxville; Dr. Sudhagar Nagarajan, Florida Atlantic University; Dr. Venktesh Pandey, North Carolina Agricultural and Technical State University',
                                html.Br(),
                                'Graduate Students: Oladimeji Basit Alaka (NCA&T), Sheikh Muhammad Usman (UTK), Soheila Saedi (FAU)'
                            ], style={'fontSize': '0.9rem', 'color': '#d1d1d1', 'marginBottom': '0.3rem', 'marginLeft': '0.5rem'}),
                            html.P([
                                'Disclaimer: The views and accuracy of the information presented belong to the authors alone. The United States Department of Transportation assumes no liability for the contents or use thereof.'
                            ], style={
                                'fontSize': '0.9rem', 
                                'color': '#a3a3a3', 
                                'fontStyle': 'italic',
                                'marginTop': '0.3rem',
                                'paddingTop': '0.3rem',
                                'borderTop': '1px solid #444'
                            })
                        ], className='acknowledgements')
                    ], className='acknowledgements-footer')
                ], className='welcome-container')
            ]),
            
            # First Tab: Map View
            dcc.Tab(label='Map View', className='tab-style1', children=[
                html.Div([
                    # Main content container with input box and map
                    html.Div([

                        # Left Section: Input Box
                        html.Div([
                                html.Label('Enter weights for three criteria', className='mainsidebar-label'),
                                html.Div([
                                    dbc.InputGroup([
                                        dbc.InputGroupText("Physical Infrastructure w1", className='sidebar-label'),  # Label part
                                        dcc.Input(id='pi_weight', type='number', value=default_weights['PI'], min=0, max=1, step=0.05, className='input-field')  # Input part
                                    ], className='input-row'),

                                    dbc.InputGroup([
                                        dbc.InputGroupText("Digital Infrastructure w2", className='sidebar-label'),
                                        dcc.Input(id='di_weight', type='number', value=default_weights['DI'], min=0, max=1, step=0.05, className='input-field')
                                    ], className='input-row'),

                                    dbc.InputGroup([
                                        dbc.InputGroupText("Social Vulnerability Index w3", className='sidebar-label'),
                                        dcc.Input(id='svi_weight', type='number', value=default_weights['SVI'], min=0, max=1, step=0.05, className='input-field')
                                    ], className='input-row'),

                                    html.P("Note: w1 + w2 + w3 = 1", style={'fontSize': '0.9rem', 'color': '#666'})
                                ], className='input-container'),
                             # Submit button and error message
                            html.Button('Submit', id='submit_button', n_clicks=0, className='submit-button'),
                            html.Div(id='weight_error_message', style={'color': 'red', 'margin-top': '10px'}),

                            html.Label('Select Granularity', className='sidebar-label2'),
                            dcc.Dropdown(id='granularity', options=[
                                {'label': 'Census Tract Level', 'value': 'tract'},
                                {'label': 'County Level', 'value': 'county'}
                            ], value='tract', className='custom-dropdown'),

                            html.Label('Select Score', className='sidebar-label2'),
                            dcc.Dropdown(id='score_type', options=[
                                {'label': 'Overall Readiness Score', 'value': 'readiness_score'},
                                {'label': 'Physical Infrastructure', 'value': 'S_PI'},
                                {'label': 'Digital Infrastructure', 'value': 'S_DI'},
                                {'label': 'Social Vulnerability Index', 'value': 'S_SVI'}
                            ], value='readiness_score', className='custom-dropdown'),

                            html.Label('Select County', className='sidebar-label2'),
                            dcc.Dropdown(id='county_select', options=[
                                {'label': county, 'value': county} for county in counties
                            ], placeholder="Select a county", className='custom-dropdown'),

                           

                            # Readiness score box (yellow background)
                            html.Div(id='readiness_score_box', className='readiness-box'),

                        ], className='sidebar'),  # End of left section (Input Box)

                        # Middle Section: Map
                        html.Div([
                            dcc.Graph(id='choropleth_map', style={'height': '100%', 'width': '100%'}),
                        ], className='map-area'),  

                        # Right Section: Input Metrics
                       html.Div(id='metrics_container', className='metrics-list-container', children=[
                            html.H3("INPUT DATA"),  # Title for Input Data
                            html.Div(id='metrics_container_content'),  # Div to update with dynamic metric elements
                            html.Hr(style={'border': '1px solid #444444'}),  # Separator line
                            html.Div(id='pi_di_svi_metrics', className='metrics-list')  # Div to display PI, DI, SVI values dynamically
                        ])



                    ], className='content-container'),  # End of content container for Map View
                ])
            ]),

                        
            # Second Tab: Comparison View
            # Modify just the radar charts section in the original layout
            dcc.Tab(label='Comparison View', className='tab-style2', children=[
                html.Div([
                    # Main container for the comparison layout
                    html.Div([
                        # Left Box: Now contains both radar charts vertically stacked
                        html.Div([
                            # Dropdowns for baseline and comparison counties
                            html.Div([
                                dcc.Dropdown(
                                    id='baseline_county',
                                    options=[
                                        {'label': 'State Average', 'value': 'state level'}
                                    ] + [{'label': county, 'value': county} for county in counties],
                                    className='custom-dropdown',
                                    placeholder="Select a county or State Average"
                                ),
                                dcc.Dropdown(
                                    id='compare_county',
                                    options=[
                                        {'label': 'State Average', 'value': 'state level'}
                                    ] + [{'label': county, 'value': county} for county in counties],
                                    className='custom-dropdown',
                                    placeholder="Select a county or State Average"
                                ),
                            ], className='dropdown-container'),

                            # Radar charts container - now vertical
                            html.Div([
                                # Overview radar chart
                                html.Div([
                                    dcc.Graph(id='comparison_radar_chart', className='radar-chart'),
                                ], className='radar-chart-wrapper'),
                                
                                # Detailed metrics radar chart
                                html.Div([
                                    dcc.Graph(id='detailed_metrics_radar', className='radar-chart'),
                                ], className='radar-chart-wrapper'),
                            ], className='radar-charts-container'),

                        ], className='left-box'),  # Keep the original left-box class

                        # Right Box: Keeps the original comment section
                        html.Div([
                            html.Div(id='comparison_text', className='comment-box'),
                        ], className='right-box'),  # Keep the original right-box class

                    ], className='comparison-container'),  # Keep the original comparison-container class

                ]),
            ]),
       
        
          # Third Tab: Documentation
            dcc.Tab(label='Documentation', className='tab-style3', children=[ 
                html.Div([   
                    # Main content container for Documentation 
                    html.Div([   
                        # Box to embed the PDF in an iframe 
                        html.Div([   
                            html.Iframe( 
                                src="/assets/readiness_app_documentation.pdf",  # Path to your PDF in the assets folder 
                                style={ 
                                    'width': '100%',  # Takes full width of the container 
                                    'height': '90%',  # Reduced to make room for contact info 
                                    'border': 'none'   # No borders around the iframe 
                                } 
                            ),
                            # Contact information section
                            html.Div([
                                html.P([
                                    "If you have questions or feedback, please contact Venktesh Pandey at ",
                                    html.Code("vpandey"),
                                    " at ",
                                    html.Code("ncat"),
                                    " dot ",
                                    html.Code("edu")
                                ], style={
                                    'textAlign': 'center',
                                    'padding': '15px',
                                    'fontSize': '14px',
                                    'color': '#ffffff',
                                    'borderTop': '1px solid #eee',
                                    'marginTop': '10px'
                                })
                            ]) 
                        ], className='custom-box')  # Styled container for the PDF 
                    ], className='content-container3'),  # Content container for the Documentation view 
                ]) 
            ])

        ], className='tabs-container')  # End of tabs container

    ], className='full-page-container')  # End of full-page container for both tabs
])
])



# To store weights
app.layout.children.insert(1, dcc.Store(id='hidden_weights', data=default_weights))


def generate_comparison_text(baseline_county, compare_county, baseline_values, compare_values, baseline_input_metrics, compare_input_metrics):
    strong_threshold = 80
    moderate_threshold = 50
    svi_high_threshold = 10  # SVI threshold

    # Helper function to discuss all input metrics once
    def discuss_inputs(county_name, category, input_metrics):
        input_discussions = []
        if category == "Digital Infrastructure":
            input_discussions.append(f"The network latency score is {input_metrics['Network Latency']:.2f}%, the download speed is {input_metrics['Download Speed']:.2f}%, and the upload speed is {input_metrics['Upload Speed']:.2f}% compared to the standard needed for the safe operation of AV shuttles. A general network improvement will be needed to get {county_name} ready for AV or shuttle deployment.")
        elif category == "Physical Infrastructure":
            input_discussions.append(f"The road improvement score is {input_metrics['Road Improvement Percentage']:.2f}%, the unpaved road percentage is {input_metrics['Unpaved Road Percentage']:.2f}%, the retroreflectivity score is {input_metrics['Retroreflectivity Score']:.2f}%, and the good bridge percentage is {input_metrics['Good Bridge Percentage']:.2f}%. To ensure safe and efficient operation of AV shuttles, improvements in road infrastructure are needed in {county_name}.")
        return " ".join(input_discussions)

    # Baseline County Analysis
    baseline_text = f"""
#### INSIGHT
##### {baseline_county}

The physical infrastructure at {baseline_county} is {"strong" if baseline_values['Physical Infrastructure'] >= strong_threshold else "moderate" if baseline_values['Physical Infrastructure'] >= moderate_threshold else "weak"}, with a score of {baseline_values['Physical Infrastructure']:.2f}%. {"It performs well in this area." if baseline_values['Physical Infrastructure'] >= strong_threshold else "It could benefit from targeted improvement." if baseline_values['Physical Infrastructure'] >= moderate_threshold else "Significant improvement is required."}
{"" if baseline_values['Physical Infrastructure'] >= strong_threshold else discuss_inputs(baseline_county, "Physical Infrastructure", {
    "Retroreflectivity Score": baseline_input_metrics['Retroreflectivity Score'],
    "Good Bridge Percentage": baseline_input_metrics['Good Bridge Percentage'],
    "Road Improvement Percentage": baseline_input_metrics['Road Improvement Percentage'],
    "Unpaved Road Percentage": baseline_input_metrics['Unpaved Road Percentage']
})}

The digital infrastructure at {baseline_county} is {"strong" if baseline_values['Digital Infrastructure'] >= strong_threshold else "moderate" if baseline_values['Digital Infrastructure'] >= moderate_threshold else "underperforming"}, with a score of {baseline_values['Digital Infrastructure']:.2f}%. {"It's contributing positively to overall readiness." if baseline_values['Digital Infrastructure'] >= strong_threshold else "It requires targeted improvements." if baseline_values['Digital Infrastructure'] >= moderate_threshold else "It requires significant upgrades."}
{"" if baseline_values['Digital Infrastructure'] >= strong_threshold else discuss_inputs(baseline_county, "Digital Infrastructure", {
    "Network Latency": baseline_input_metrics['Network Latency'],
    "Download Speed": baseline_input_metrics['Download Speed'],
    "Upload Speed": baseline_input_metrics['Upload Speed']
})}

The social vulnerability index (SVI) in {baseline_county} is {baseline_values['Social Vulnerability Index']:.2f}%, indicating {("higher vulnerability" if baseline_values['Social Vulnerability Index'] >= svi_high_threshold else "lower vulnerability")} in terms of transportation access.
"""

    # Comparison County Analysis
    comparison_text = f"""
##### {compare_county}

The physical infrastructure in {compare_county} is {"strong" if compare_values['Physical Infrastructure'] >= strong_threshold else "moderate" if compare_values['Physical Infrastructure'] >= moderate_threshold else "weak"}, with a score of {compare_values['Physical Infrastructure']:.2f}%. {"It performs well in this area." if compare_values['Physical Infrastructure'] >= strong_threshold else "It could benefit from targeted improvement." if compare_values['Physical Infrastructure'] >= moderate_threshold else "Significant improvement is required."}
{"" if compare_values['Physical Infrastructure'] >= strong_threshold else discuss_inputs(compare_county, "Physical Infrastructure", {
    "Retroreflectivity Score": compare_input_metrics['Retroreflectivity Score'],
    "Good Bridge Percentage": compare_input_metrics['Good Bridge Percentage'],
    "Road Improvement Percentage": compare_input_metrics['Road Improvement Percentage'],
    "Unpaved Road Percentage": compare_input_metrics['Unpaved Road Percentage']
})}

The digital infrastructure in {compare_county} is {"strong" if compare_values['Digital Infrastructure'] >= strong_threshold else "moderate" if compare_values['Digital Infrastructure'] >= moderate_threshold else "underperforming"}, with a score of {compare_values['Digital Infrastructure']:.2f}%. {"It's contributing positively to overall readiness." if compare_values['Digital Infrastructure'] >= strong_threshold else "It requires targeted improvements." if compare_values['Digital Infrastructure'] >= moderate_threshold else "It requires significant upgrades."}
{"" if compare_values['Digital Infrastructure'] >= strong_threshold else discuss_inputs(compare_county, "Digital Infrastructure", {
    "Network Latency": compare_input_metrics['Network Latency'],
    "Download Speed": compare_input_metrics['Download Speed'],
    "Upload Speed": compare_input_metrics['Upload Speed']
})}

The social vulnerability index (SVI) in {compare_county} is {compare_values['Social Vulnerability Index']:.2f}%, indicating {("higher vulnerability" if compare_values['Social Vulnerability Index'] >= svi_high_threshold else "lower vulnerability")} in terms of transportation access.
"""

    # Overall Comparison
    overall_comparison_text = f"""
##### Comparison of {baseline_county} and {compare_county}

Both counties have physical infrastructure scores of {baseline_values['Physical Infrastructure']:.2f}% for {baseline_county} and {compare_values['Physical Infrastructure']:.2f}% for {compare_county}. {baseline_county if baseline_values['Physical Infrastructure'] >= compare_values['Physical Infrastructure'] else compare_county} is stronger in terms of physical infrastructure.

In terms of digital infrastructure, {baseline_county} has a score of {baseline_values['Digital Infrastructure']:.2f}%, while {compare_county} has {compare_values['Digital Infrastructure']:.2f}%. {baseline_county if baseline_values['Digital Infrastructure'] >= compare_values['Digital Infrastructure'] else compare_county} leads in digital readiness.

For social vulnerability, {baseline_county} has an SVI of {baseline_values['Social Vulnerability Index']:.2f}%, while {compare_county} has an SVI of {compare_values['Social Vulnerability Index']:.2f}%, indicating {baseline_county if baseline_values['Social Vulnerability Index'] >= compare_values['Social Vulnerability Index'] else compare_county} has a higher share of vulnerable populations.
"""

    return baseline_text + comparison_text + overall_comparison_text






# Callbacks
    labels = ['Physical Infrastructure', 'Digital Infrastructure', 'Social Vulnerability Index']

    # If either county is not selected, return an empty radar chart and text
    if not baseline_county or not compare_county:
        # Return an empty figure and no text
        fig = go.Figure()
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True),
                bgcolor='#161928'  # Keep background color consistent
            ),
            showlegend=False,
            plot_bgcolor='#161928',
            paper_bgcolor='#161928',
            font=dict(color='white'),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        return fig, ""

    # Default input metrics
    default_input_metrics = {
        "Age 65+": census_tracts["EP_AGE65"].mean() * 100,
        "No Vehicle": census_tracts["EP_NOVEH"].mean() * 100,
        "Network Latency": census_tracts["B_latency_percent"].mean() * 100,
        "Download Speed": census_tracts["B_download_percent"].mean() * 100,
        "Upload Speed": census_tracts["B_upload_percent"].mean() * 100,
        "Retroreflectivity Score": census_tracts["RL_score_percentage"].mean() * 100,
        "Good Bridge Percentage": census_tracts["good_bridge_percentage"].mean() * 100,
        "Road Improvement Percentage": census_tracts["Final_Road_Improvement_Score_Percentage"].mean() * 100,
        "Unpaved Road Percentage": census_tracts["unpaved_percentage"].mean() * 100
    }

     # Calculate state-wide averages based on county-level aggregation using STCNTY
    county_means = census_tracts.groupby('COUNTY').agg({
        'county_SVI': 'mean',
        'county_SPI': 'mean',
        'county_SDI': 'mean',
        'county_SVI_scaled': 'mean',
        "EP_AGE65": 'mean',
        'EP_NOVEH': 'mean',
        'B_latency_percent':  'mean',
        'B_download_percent': 'mean',
        'B_upload_percent':  'mean',
        'RL_score_percentage':    'mean',
        'good_bridge_percentage': 'mean',
        'Final_Road_Improvement_Score_Percentage': 'mean',
        'unpaved_percentage': 'mean'
    }).reset_index() 

    print("Columns in county_means:", county_means.columns)

    average_metrics = {
        'Physical Infrastructure': county_means['county_SPI'].mean() * 100,
        'Digital Infrastructure': county_means['county_SDI'].mean() * 100,
        'Social Vulnerability Index': county_means['county_SVI_scaled'].mean() * 100
    }


    # Get baseline and comparison values
    if baseline_county == 'state level':
        baseline_values = average_metrics
        baseline_input_metrics = default_input_metrics
    else:
        baseline_data = county_means[county_means['COUNTY'] == baseline_county].iloc[0]
        baseline_values = {
            'Physical Infrastructure': baseline_data['county_SPI']*100,
            'Digital Infrastructure': baseline_data['county_SDI']*100,
            'Social Vulnerability Index': baseline_data['county_SVI_scaled']*100
        }
        baseline_input_metrics = {
            "Age 65+": baseline_data["EP_AGE65"]* 100,
            "No Vehicle": baseline_data["EP_NOVEH"] * 100,
            "Network Latency": baseline_data["B_latency_percent"]* 100,
            "Download Speed": baseline_data["B_download_percent"] * 100,
            "Upload Speed": baseline_data["B_upload_percent"]* 100,
            "Retroreflectivity Score": baseline_data["RL_score_percentage"]* 100,
            "Good Bridge Percentage": baseline_data["good_bridge_percentage"]* 100,
            "Road Improvement Percentage": baseline_data["Final_Road_Improvement_Score_Percentage"] * 100,
            "Unpaved Road Percentage": (baseline_data["unpaved_percentage"]* 100)
        }

    if compare_county == 'state level':
        compare_values = average_metrics
        compare_input_metrics = default_input_metrics
    else:
        compare_data = county_means[county_means['COUNTY'] == compare_county].iloc[0]
        compare_values = {
            'Physical Infrastructure': compare_data['county_SPI']*100,
            'Digital Infrastructure': compare_data['county_SDI']*100,
            'Social Vulnerability Index': compare_data['county_SVI_scaled']*100
        }
        compare_input_metrics = {
            "Age 65+": compare_data["EP_AGE65"]* 100,
            "No Vehicle": compare_data["EP_NOVEH"]* 100,
            "Network Latency": compare_data["B_latency_percent"]* 100,
            "Download Speed": compare_data["B_download_percent"]* 100,
            "Upload Speed": compare_data["B_upload_percent"]* 100,
            "Retroreflectivity Score": compare_data["RL_score_percentage"] * 100,
            "Good Bridge Percentage": compare_data["good_bridge_percentage"]* 100,
            "Road Improvement Percentage": compare_data["Final_Road_Improvement_Score_Percentage"] * 100,
            "Unpaved Road Percentage": (compare_data["unpaved_percentage"] * 100)
        }

    # Generate radar plot
    fig = go.Figure()

    # Baseline trace
    fig.add_trace(go.Scatterpolar(
        r=list(baseline_values.values()),
        theta=labels,
        fill='toself',
        name='Baseline' if baseline_county == 'average' else baseline_county
    ))

    # Compare trace
    fig.add_trace(go.Scatterpolar(
        r=list(compare_values.values()),
        theta=labels,
        fill='toself',
        name='Compare' if compare_county == 'average' else compare_county
    ))

    # Customize the radar plot
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
            bgcolor='#161928'  # Grey background for radar chart
        ),
        showlegend=True,
        plot_bgcolor='#161928',  # Background color of the entire plot area
        paper_bgcolor='#161928',  # Background color of the entire paper
        font=dict(color='white'),  # White font color
        margin=dict(t=20, b=20, l=20, r=20)
    )

    # Generate comparison text
    comparison_text = generate_comparison_text(
        baseline_county, compare_county, baseline_values, compare_values, baseline_input_metrics, compare_input_metrics
    )

    # Return figure and comparison text using dcc.Markdown
    return fig, dcc.Markdown(comparison_text)

@app.callback(
    [Output('comparison_radar_chart', 'figure'),
     Output('detailed_metrics_radar', 'figure'),
     Output('comparison_text', 'children')],
    [Input('baseline_county', 'value'),
     Input('compare_county', 'value')]
)
def update_comparison_charts(baseline_county, compare_county):
    labels = ['Physical Infrastructure', 'Digital Infrastructure', 'Social Vulnerability Index']
    
    detailed_labels = [
        'Road Improvement Percentage',
        'Unpaved Road Percentage',
        'Retroreflectivity Score',
        'Good Bridge Percentage',
        'Network Latency',
        'Download Speed',
        'Upload Speed',
        'No Vehicle'
    ]
    
    # If either county is not selected, return empty figures and text
    if not baseline_county or not compare_county:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=False,
            plot_bgcolor='#161928',
            paper_bgcolor='#161928',
            font=dict(color='white'),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        return empty_fig, empty_fig, ""

    # Get county means for calculations
    county_means = census_tracts.groupby('COUNTY').agg({
        'county_SVI': 'mean',
        'county_SPI': 'mean',
        'county_SDI': 'mean',
        'county_SVI_scaled': 'mean',
        "EP_AGE65": 'mean',
        'EP_NOVEH': 'mean',
        'B_latency_percent': 'mean',
        'B_download_percent': 'mean',
        'B_upload_percent': 'mean',
        'RL_score_percentage': 'mean',
        'good_bridge_percentage': 'mean',
        'Final_Road_Improvement_Score_Percentage': 'mean',
        'unpaved_percentage': 'mean'
    }).reset_index()
    
    # Calculate metrics for baseline county
    if baseline_county == 'state level':
        baseline_detailed_values = [
            county_means['Final_Road_Improvement_Score_Percentage'].mean() * 100,
            (county_means['unpaved_percentage'].mean() * 100),
            county_means['RL_score_percentage'].mean() * 100,
            county_means['good_bridge_percentage'].mean() * 100,
            county_means['B_latency_percent'].mean() * 100,
            county_means['B_download_percent'].mean() * 100,
            county_means['B_upload_percent'].mean() * 100,
            (county_means['EP_NOVEH'].mean() * 100)
        ]
        baseline_values = {
            'Physical Infrastructure': county_means['county_SPI'].mean() * 100,
            'Digital Infrastructure': county_means['county_SDI'].mean() * 100,
            'Social Vulnerability Index': county_means['county_SVI_scaled'].mean() * 100
        }
    else:
        baseline_data = county_means[county_means['COUNTY'] == baseline_county].iloc[0]
        baseline_detailed_values = [
            baseline_data['Final_Road_Improvement_Score_Percentage'] * 100,
            (baseline_data['unpaved_percentage'] * 100),
            baseline_data['RL_score_percentage'] * 100,
            baseline_data['good_bridge_percentage'] * 100,
            baseline_data['B_latency_percent'] * 100,
            baseline_data['B_download_percent'] * 100,
            baseline_data['B_upload_percent'] * 100,
            100 - (baseline_data['EP_NOVEH'] * 100)
        ]
        baseline_values = {
            'Physical Infrastructure': baseline_data['county_SPI'] * 100,
            'Digital Infrastructure': baseline_data['county_SDI'] * 100,
            'Social Vulnerability Index': baseline_data['county_SVI_scaled'] * 100
        }
    
    # Calculate metrics for comparison county
    if compare_county == 'state level':
        compare_detailed_values = [
            county_means['Final_Road_Improvement_Score_Percentage'].mean() * 100,
            (county_means['unpaved_percentage'].mean() * 100),
            county_means['RL_score_percentage'].mean() * 100,
            county_means['good_bridge_percentage'].mean() * 100,
            county_means['B_latency_percent'].mean() * 100,
            county_means['B_download_percent'].mean() * 100,
            county_means['B_upload_percent'].mean() * 100,
            100 - (county_means['EP_NOVEH'].mean() * 100)
        ]
        compare_values = {
            'Physical Infrastructure': county_means['county_SPI'].mean() * 100,
            'Digital Infrastructure': county_means['county_SDI'].mean() * 100,
            'Social Vulnerability Index': county_means['county_SVI_scaled'].mean() * 100
        }
    else:
        compare_data = county_means[county_means['COUNTY'] == compare_county].iloc[0]
        compare_detailed_values = [
            compare_data['Final_Road_Improvement_Score_Percentage'] * 100,
            (compare_data['unpaved_percentage'] * 100),
            compare_data['RL_score_percentage'] * 100,
            compare_data['good_bridge_percentage'] * 100,
            compare_data['B_latency_percent'] * 100,
            compare_data['B_download_percent'] * 100,
            compare_data['B_upload_percent'] * 100,
            100 - (compare_data['EP_NOVEH'] * 100)
        ]
        compare_values = {
            'Physical Infrastructure': compare_data['county_SPI'] * 100,
            'Digital Infrastructure': compare_data['county_SDI'] * 100,
            'Social Vulnerability Index': compare_data['county_SVI_scaled'] * 100
        }
    
    # Create original radar chart
    fig = go.Figure()
    
    # Add traces for original radar chart
    fig.add_trace(go.Scatterpolar(
        r=list(baseline_values.values()),
        theta=labels,
        fill='toself',
        name=baseline_county if baseline_county != 'state level' else 'State Average'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=list(compare_values.values()),
        theta=labels,
        fill='toself',
        name=compare_county if compare_county != 'state level' else 'State Average'
    ))
    
    # Create detailed metrics radar chart
    detailed_fig = go.Figure()

    revised_labels = [
        '% Planned Road Upgrades',       # Road Improvement
        '% Paved Roads',         # Paved Roads
        'Retroreflectivity Score %',   # Retroreflectivity
        '% Good Bridges',        # Good Bridges
        'Network Latency % (relative to 10 ms)',       # Network Latency
        'Download Speed % (relative to 1000 Mbps)', # Download Speed
        'Upload Speed % (relative to 1000 Mbps)',   # Upload Speed
        '% Population with Vehicles'     # Transport Access
    ]

    
    # Add traces for detailed radar chart
    detailed_fig.add_trace(go.Scatterpolar(
        r=baseline_detailed_values,
        theta=revised_labels,
        fill='toself',
        name=baseline_county if baseline_county != 'state level' else 'State Average'
    ))
    
    detailed_fig.add_trace(go.Scatterpolar(
        r=compare_detailed_values,
        theta=revised_labels,
        fill='toself',
        name=compare_county if compare_county != 'state level' else 'State Average'
    ))
    
    # Update layouts for both charts
    for chart in [fig, detailed_fig]:
        chart.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False
                ),
                bgcolor='#161928'
            ),
            showlegend=True,
            plot_bgcolor='#161928',
            paper_bgcolor='#161928',
            font=dict(color='white'),
            height=450,  # Fixed height
            margin=dict(t=30, b=30, l=30, r=30)  # Adjusted margins
        )
    
    # Generate comparison text
    comparison_text = generate_comparison_text(
        baseline_county, compare_county, baseline_values, compare_values,
        dict(zip(detailed_labels, baseline_detailed_values)),
        dict(zip(detailed_labels, compare_detailed_values))
    )
    # print(comparison_text)
    
    return fig, detailed_fig, dcc.Markdown(comparison_text)

@app.callback(
    Output('weight_error_message', 'children'),
    Output('hidden_weights', 'data'),
    Input('submit_button', 'n_clicks'),
    State('pi_weight', 'value'),
    State('di_weight', 'value'),
    State('svi_weight', 'value'),
)
def update_weights(n_clicks, pi_weight, di_weight, svi_weight):
    if n_clicks > 0:
        total_weight = (pi_weight or 0) + (di_weight or 0) + (svi_weight or 0)

       # Add tolerance to handle floating-point precision errors
        if abs(total_weight - 1.0) > 1e-6:
            return 'The sum of weights must equal 1.', dash.no_update
        else:
            return '', {'PI': pi_weight, 'DI': di_weight, 'SVI': svi_weight}
    else:
        # Return default weights if no button clicks
        return '', default_weights

def get_coords(geometry):
    if geometry.is_empty:
        return [], []
    elif geometry.geom_type == 'Polygon':
        x, y = geometry.exterior.coords.xy
        return list(y), list(x)  # Note: latitude (y), longitude (x)
    elif geometry.geom_type == 'MultiPolygon':
        x = []
        y = []
        for polygon in geometry.geoms:
            xi, yi = polygon.exterior.coords.xy
            x.extend(list(yi) + [None])  # Latitude
            y.extend(list(xi) + [None])  # Longitude
        return x, y
    else:
        return [], []

@app.callback(
    Output('choropleth_map', 'figure'),
    Output('readiness_score_box', 'children'),
    Input('granularity', 'value'),
    Input('score_type', 'value'),
    Input('county_select', 'value'),
    Input('hidden_weights', 'data')
)
def update_map(granularity, score_type, county_selected, weights):
    census_tracts = gpd.read_file(data_file_path)

    if 'GEOID' not in census_tracts.columns:
        census_tracts['GEOID'] = census_tracts['FIPS'].astype(str)

    pi_weight = weights['PI']
    di_weight = weights['DI']
    svi_weight = weights['SVI']

    # Compute readiness score and convert to percentage
    census_tracts["readiness_score"] = (
        pi_weight * census_tracts["S_PI"] +
        di_weight * census_tracts["S_DI"] +
        svi_weight * census_tracts["S_SVI"]
    ) * 100

    # Calculate percentages for PI, DI, and SVI
    county_metrics = census_tracts.groupby('COUNTY').agg({
        'readiness_score': 'mean',
        'S_PI': lambda x: x.mean() * 100,  # Convert to percentage
        'S_DI': lambda x: x.mean() * 100,  # Convert to percentage
        'S_SVI': lambda x: x.mean() * 100  # Convert to percentage
    }).reset_index()

    county_metrics.rename(columns={
        'S_PI': 'county_SPI',
        'S_DI': 'county_SDI',
        'S_SVI': 'county_SVI',
        'readiness_score': 'county_readiness_score'
    }, inplace=True)

    county_geometries = census_tracts[['COUNTY', 'geometry']].dissolve(by='COUNTY').reset_index()

    county_data = county_geometries.merge(county_metrics, on='COUNTY', how='left')

    census_tracts = census_tracts[~census_tracts.is_empty]
    census_tracts = census_tracts[census_tracts.is_valid]
    census_tracts = census_tracts.to_crs(epsg=4326)

    county_data = county_data[~county_data.is_empty]
    county_data = county_data[county_data.is_valid]
    county_data = county_data.to_crs(epsg=4326)

    readiness_score_text = ''

    if granularity == 'tract':
        data = census_tracts.copy()
        if score_type in ['readiness_score', 'S_PI', 'S_DI', 'S_SVI']:
            color_column = score_type
        else:
            color_column = 'readiness_score'

        hover_data = data[['COUNTY', 'S_PI', 'S_DI', 'S_SVI', 'readiness_score', 'GEOID']]
        data_json = json.loads(data.to_json())
        geojson = data_json

        fig = px.choropleth_mapbox(
            data,
            geojson=geojson,
            locations='GEOID',
            color=color_column,
            featureidkey="properties.GEOID",
            mapbox_style="carto-darkmatter",
            zoom=6,
            center={"lat": 35.7596, "lon": -79.0193},
            opacity=0.6,
            custom_data=hover_data,
            color_continuous_scale='Viridis'
        )

        fig.update_traces(hovertemplate=(
            "<b>%{customdata[0]}</b> (Tract: %{customdata[5]})<br><br>"
            "<span style='color: orange;'>⬤</span> <b>Physical Infrastructure</b>: %{customdata[1]:.2f}<br>"
            "<span style='color: green;'>⬤</span> <b>Digital Infrastructure</b>: %{customdata[2]:.2f}<br>"
            "<span style='color: lightblue;'>⬤</span> <b>Social Vulnerability Index</b>: %{customdata[3]:.2f}<br>"
            "<span style='color: darkblue;'>⬤</span> <b>Overall Readiness</b>: %{customdata[4]:.2f}%<br>"
            "<extra></extra>"
        ))

    elif granularity == 'county':
        data = county_data.copy()
        if score_type == 'readiness_score':
            color_column = 'county_readiness_score'
        elif score_type == 'S_PI':
            color_column = 'county_SPI'
        elif score_type == 'S_DI':
            color_column = 'county_SDI'
        elif score_type == 'S_SVI':
            color_column = 'county_SVI'
        else:
            color_column = 'county_readiness_score'

        hover_data = data[['COUNTY', 'county_SPI', 'county_SDI', 'county_SVI', 'county_readiness_score']]
        data_json = json.loads(data.to_json())
        geojson = data_json

        fig = px.choropleth_mapbox(
            data,
            geojson=geojson,
            locations='COUNTY',
            color=color_column,
            featureidkey="properties.COUNTY",
            mapbox_style="carto-darkmatter",
            zoom=6,
            center={"lat": 35.7596, "lon": -79.0193},
            opacity=0.6,
            custom_data=hover_data,
            color_continuous_scale='Viridis'
        )

        fig.update_traces(hovertemplate=(
            "<b>%{customdata[0]}</b><br><br>"
            "<span style='color: orange;'>⬤</span> <b>Physical Infrastructure</b>: %{customdata[1]:.2f}<br>"
            "<span style='color: green;'>⬤</span> <b>Digital Infrastructure</b>: %{customdata[2]:.2f}<br>"
            "<span style='color: lightblue;'>⬤</span> <b>Social Vulnerability Index</b>: %{customdata[3]:.2f}<br>"
            "<span style='color: darkblue;'>⬤</span> <b>Overall Readiness</b>: %{customdata[4]:.2f}%<br>"
            "<extra></extra>"
        ))

        # Add county names to the map
        data['rep_point'] = data['geometry'].representative_point()
        data['rep_lon'] = data.rep_point.x
        data['rep_lat'] = data.rep_point.y

        fig.add_trace(go.Scattermapbox(
            lon=data['rep_lon'],
            lat=data['rep_lat'],
            mode='text',
            text=data['COUNTY'],
            textfont=dict(color='white', size=12),
            hoverinfo='none',
            showlegend=False
        ))

    else:
        fig = go.Figure()

    # Text for readiness score box (for both tract and county levels)
    if county_selected:
        county_selected_geometry = county_data[county_data['COUNTY'] == county_selected]
        if not county_selected_geometry.empty:
            bounds = county_selected_geometry.total_bounds  # (minx, miny, maxx, maxy)
            center = {
                'lat': (bounds[1] + bounds[3]) / 2,
                'lon': (bounds[0] + bounds[2]) / 2
            }
            fig.update_layout(mapbox_center=center)
            fig.update_layout(mapbox_zoom=10)

            # Logic for both county and tract levels
            if granularity == 'tract':
                county_tracts = census_tracts[census_tracts['COUNTY'] == county_selected]
                if not county_tracts.empty:
                    score = county_tracts[score_type].mean() 
                    if score_type == 'S_PI':
                        readiness_score_text = f"Physical Infrastructure readiness for {county_selected} is {score:.2f}%"
                    elif score_type == 'S_DI':
                        readiness_score_text = f"Digital Infrastructure readiness for {county_selected} is {score:.2f}%"
                    elif score_type == 'S_SVI':
                        readiness_score_text = f"Social Vulnerability Index score for {county_selected} is {score:.2f}%"
                    else:
                        readiness_score_text = f"Overall Readiness score for {county_selected} is {score:.2f}%"
                else:
                    readiness_score_text = f"{county_selected} not found."
            
            # Logic for county level
            else:
                if score_type == 'S_PI':
                    score = county_metrics[county_metrics['COUNTY'] == county_selected]['county_SPI'].iloc[0] 
                    readiness_score_text = f"Physical Infrastructure readiness for {county_selected} is {score:.2f}%"
                elif score_type == 'S_DI':
                    score = county_metrics[county_metrics['COUNTY'] == county_selected]['county_SDI'].iloc[0] 
                    readiness_score_text = f"Digital Infrastructure readiness for {county_selected} is {score:.2f}%"
                elif score_type == 'S_SVI':
                    score = county_metrics[county_metrics['COUNTY'] == county_selected]['county_SVI'].iloc[0] 
                    readiness_score_text = f"Social Vulnerability Index score for {county_selected} is {score:.2f}%"
                else:
                    score = county_metrics[county_metrics['COUNTY'] == county_selected]['county_readiness_score'].iloc[0]
                    readiness_score_text = f"Overall Readiness score for {county_selected} is {score:.2f}%"

            # Highlight the selected county geometry
            selected_geometry = county_selected_geometry.geometry.iloc[0]
            lat_coords, lon_coords = get_coords(selected_geometry)

            fig.add_trace(go.Scattermapbox(
                lon=lon_coords,
                lat=lat_coords,
                mode='lines',
                line=dict(width=4, color='yellow'),
                hoverinfo='none',
                showlegend=False
            ))
        else:
            readiness_score_text = f"{county_selected} not found."
    else:
        readiness_score_text = ''


    # Update layout for the color axis
    fig.update_layout(
        coloraxis_colorbar=dict(
            orientation='h',
            yanchor='top',
            y=0.99,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(0,0,0,0)',  # Transparent background for color bar
            outlinecolor='rgba(0,0,0,0)',  # Remove the outline
            thickness=15,
            len=0.5,
            tickfont=dict(color='white'),
            title=dict(font=dict(color='white'), text='Score')
        )
    )

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    return fig, readiness_score_text




@app.callback(
    Output('pi_di_svi_metrics', 'children'),  # Output for PI, DI, SVI metrics
    [Input('county_select', 'value')]  # County selection triggers this callback
)
def update_pi_di_svi_metrics(county_selected):
    if county_selected:
        county_data = census_tracts[census_tracts['COUNTY'] == county_selected]

        # Metrics for Physical Infrastructure (PI), Digital Infrastructure (DI), and Social Vulnerability Index (SVI)
        metrics = {
            "Physical Infrastructure": county_data["S_PI"].mean() * 100,
            "Digital Infrastructure": county_data["S_DI"].mean() * 100,
            "Social Vulnerability Index": county_data["S_SVI"].mean() * 100
        }

        # Icons for the metrics
        icons = {
            "Physical Infrastructure": "fas fa-tools",
            "Digital Infrastructure": "fas fa-network-wired",
            "Social Vulnerability Index": "fas fa-users"
        }

        # Custom bar colors for PI, DI, and SVI
        custom_classes = {
            "Physical Infrastructure": "pi-bar",
            "Digital Infrastructure": "di-bar",
            "Social Vulnerability Index": "svi-bar"
        }

        # Create dynamic metric bars for PI, DI, SVI
        metric_elements = []
        for metric, value in metrics.items():
            icon_class = icons.get(metric, "fas fa-chart-bar")
            custom_class = custom_classes.get(metric, "")  # Get the custom class for each metric

            metric_elements.append(
                html.Div([
                    html.Div([
                        html.I(className=icon_class, style={'color': '#444444', 'margin-right': '10px'}),
                        html.Span(f"{metric}", style={'color': '#a3a3a3'}),
                        html.Span(f"{value:.2f}%", className="metric-value")
                    ], className='metric-label-row'),

                    # Grey background and colored foreground using the custom class for each metric
                    html.Div([
                        html.Div(className=f"metric-bar-foreground {custom_class}", style={'width': f'{value}%'})
                    ], className='metric-bar-background')
                ], style={'margin-bottom': '20px'})
            )

        return html.Div(metric_elements)

    return html.Div("Select a county to see metrics.", className='no-metrics')

@app.callback(
    Output('metrics_container_content', 'children'),
    [Input('county_select', 'value')]
)
def update_metrics(county_selected):
    if county_selected:
        county_data = census_tracts[census_tracts['COUNTY'] == county_selected]

        metrics = {
            "Age 65+": county_data["EP_AGE65"].mean() * 100,
            "No Vehicle": county_data["EP_NOVEH"].mean() * 100,
            "Network Latency": county_data["B_latency_percent"].mean() * 100,
            "Download Speed": county_data["B_download_percent"].mean() * 100,
            "Upload Speed": county_data["B_upload_percent"].mean() * 100,
            "Retroreflectivity Score": county_data["RL_score_percentage"].mean() * 100,
            "Good Bridge Percentage": county_data["good_bridge_percentage"].mean() * 100,
            "Road Improvement Percentage": county_data["Final_Road_Improvement_Score_Percentage"].mean() * 100,
            "Unpaved Road Percentage": 100- (county_data["unpaved_percentage"].mean() * 100)
        }

        # Associate icons with metrics
        icons = {
            "Age 65+": "fas fa-user-clock",
            "No Vehicle": "fas fa-ban",
            "Network Latency": "fas fa-wifi",
            "Download Speed": "fas fa-download",
            "Upload Speed": "fas fa-upload",
            "Retroreflectivity Score": "fas fa-road",
            "Good Bridge Percentage": "fas fa-archway",
            "Road Improvement Percentage": "fas fa-tools",
            "Unpaved Road Percentage": "fas fa-mountain"
        }

        # Custom bar colors for each metric
        custom_classes = {
            "Age 65+": "age-65-percent",
            "No Vehicle": "no-veh-percent",
            "Network Latency": "latency-percent",
            "Download Speed": "download-percent",
            "Upload Speed": "upload-percent",
            "Retroreflectivity Score": "rl-score-percent",
            "Good Bridge Percentage": "good-bridge-percent",
            "Road Improvement Percentage": "road-imp-percent",
            "Unpaved Road Percentage": "unpaved-percent"
        }

        # Create dynamic metric bars
        metric_elements = []
        for metric, value in metrics.items():
            icon_class = icons.get(metric, "fas fa-chart-bar")
            custom_class = custom_classes.get(metric, "")  # Get the custom class for bar color

            metric_elements.append(
                html.Div([
                    html.Div([
                        html.I(className=icon_class, style={'color': '#444444', 'margin-right': '10px'}),
                        html.Span(f"{metric}", style={'color': '#a3a3a3'}),
                        html.Span(f"{value:.2f}%", className="metric-value")
                    ], className='metric-label-row'),

                    # Grey background and colored foreground using the custom class for each metric
                    html.Div([
                        html.Div(className=f"metric-bar-foreground {custom_class}", style={'width': f'{value}%'})
                    ], className='metric-bar-background')
                ], style={'margin-bottom': '20px'})
            )

        return html.Div(metric_elements)

    return html.Div("Select a county to see metrics.", className='no-metrics')








if __name__ == '__main__':
    app.run_server(debug=True)
