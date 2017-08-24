import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd

# https://plot.ly/dash/dash-core-components
# ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b150_GRCh37p13/VCF/

all_studies = [
    {'label': 'Hemoglobin A1(C) Levels', 'value': 'HbA1c'},
    {'label': '2hr Glucose Response', 'value': '2hrG'}
]

app = dash.Dash()

app.layout = html.Div([
    html.H1(children="Disease-Associated Genomic Variation", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='disease-select',
        clearable=False,
        placeholder="Select a Disease/Study...",
        options=all_studies
    ),
    html.H3(children='Study Description'),
    dcc.Markdown(id="desc"),
    html.Hr(),
    dcc.Graph(id="manhattan-plot", animate=True),
    html.Div([
        html.Label('SNP Type'),
        dcc.Dropdown(
            id = 'type-select',
            options=[
                {'label': 'Indel', 'value': 'indel'},
                {'label': 'Transition', 'value': 'transition'},
                {'label': 'Transversion', 'value': 'transversion'}
            ],
            value=['indel', 'transition', 'transversion'],
            multi=True
        ),
        html.Label('SNP Effect'),
        dcc.Dropdown(
            id='effect-select',
            options=[
                {'label': 'Missense', 'value': 'missense'},
                {'label': 'Nonsense', 'value': 'nonsense'},
                {'label': 'Unknown', 'value': 'unknown'}
            ],
            value=['missense', 'nonsense'],
            multi=True
        )],
        style={'columnCount': 2}
    ),
    html.Br(),
    html.Div([
        html.Label('Filter by Significance'),
        dcc.RangeSlider(
            min=0, max=100, step=0.5, value=[70, 100]
        )
    ])
])

@app.callback(
    Output(component_id='desc', component_property='children'),
    [Input(component_id='disease-select', component_property='value')]
)
def update_study_description(study):
    try:
        with open("data/{}_description.md".format(study), 'r') as d:
            current_description = d.readlines()
            #print(current_description)
            return ' '.join(current_description)
    except FileNotFoundError:
        return '''Sorry Partner, looks like the description for the study you\'ve requested is missing! 
        Someone really fucked this one up!'''
if __name__ == '__main__':
    app.run_server()