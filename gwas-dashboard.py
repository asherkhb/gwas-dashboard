import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff

import gzip
import pandas as pd

# https://plot.ly/dash/dash-core-components
# two

# Utility Functions.

def str_to_unique_list(df, col):
    return list(set([item for sublist in [s.split(',') for s in df[col].unique()] for item in sublist]))


def check_effect(row, effect):
    split_effects = row['func'].split(',')
    if effect in split_effects:
        return True
    else:
        return False


def build_description(study_key):
    try:
        with open("data/{}_description.md".format(study_key), 'r') as d:
            current_description = d.readlines()
            return ' '.join(current_description)
    except FileNotFoundError:
        return '''Sorry Partner, looks like the description for the study you\'ve requested is missing! 
        Someone really fucked this one up!'''


def read_data(study_key):
    print("Reading data for {}".format(study_key))
    df = pd.read_table('data/{}.tsv.merged.gz'.format(study_key), compression='gzip', sep='\t') #compression='gzip',sep='\x01' \t
    effects = str_to_unique_list(df, 'func')
    # TODO: Replace this slow ass method.
    #for e in effects:
    #    df[e] = df.apply(check_effect, axis = 1, args = (e,))
    return df


def filter_by_id(df, id):
    return df.loc[df['id'] == id]


# Initialize Data.
all_studies = [
    {'label': 'Hemoglobin A1(C) Levels', 'value': 'HbA1c'},
    {'label': '2hr Glucose Response', 'value': '2hrG'}
]

base_data = {s['value']: read_data(s['value']) for s in all_studies}
base_desc = {s['value']: build_description(s['value']) for s in all_studies}
base_types = {s['value']: base_data[s['value']]['class'].unique() for s in all_studies}
base_effects = {s['value']: str_to_unique_list(base_data[s['value']], 'func') for s in all_studies}


# Dash App.
app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H1(children="Disease-Associated Genomic Variation", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='disease-select',
        clearable=False,
        placeholder="Select a Disease/Study...",
        options=all_studies,
        value='HbA1c'
    ),
    html.H3(children='Study Description'),
    dcc.Markdown(id="desc"),
    html.Hr(),
    dcc.Graph(id="manhattan-plot", animate=True),
    html.Div([
        html.Label('SNP Type'),
        dcc.Dropdown(
            id = 'type-select',
            multi=True
        ),
        html.Label('SNP Effect'),
        dcc.Dropdown(
            id='effect-select',
            multi=True
        )],
        style={'columnCount': 1}
    ),
    html.Br(),
    # html.Div([
    #     html.Label('Filter by Significance'),
    #     dcc.RangeSlider(
    #         min=0, max=100, step=0.5, value=[70, 100]
    #     )
    # ])
    dcc.Graph(id='hits-table')
])


@app.callback(
    Output(component_id='desc', component_property='children'),
    [Input(component_id='disease-select', component_property='value')]
)
def update_study_description(study):
    new_desc = base_desc[study]
    return new_desc
    # try:
    #     with open("data/{}_description.md".format(study), 'r') as d:
    #         current_description = d.readlines()
    #         return ' '.join(current_description)
    # except FileNotFoundError:
    #     return '''Sorry Partner, looks like the description for the study you\'ve requested is missing!
    #     Someone really fucked this one up!'''


@app.callback(
    Output(component_id='type-select', component_property='options'),
    [Input(component_id='disease-select', component_property='value')]
)
def update_type_select_opt(value):
    #my_data = filter_by_id(base_data, value)
    new_opts = [{'label': v, 'value': v} for v in base_types[value]]
    return new_opts

@app.callback(
    Output(component_id='type-select', component_property='value'),
    [Input(component_id='type-select', component_property='options')]
)
def update_type_select_val(opts):
    return [o['value'] for o in opts]


@app.callback(
    Output(component_id='effect-select', component_property='options'),
    [Input(component_id='disease-select', component_property='value')]
)
def update_effect_select_opt(value):
    new_opts = [{'label': v, 'value': v} for v in base_effects[value]]
    return new_opts

@app.callback(
    Output(component_id='effect-select', component_property='value'),
    [Input(component_id='effect-select', component_property='options')]
)
def update_effect_select_val(opts):
    return [o['value'] for o in opts]


@app.callback(
    Output(component_id='hits-table', component_property='figure'),
    [Input(component_id='disease-select', component_property='value')]
)
def update_hits_table(value):
    filtered_data = base_data[value].sort_values(by = "pvalue").head()
    #display_data = filtered_data.drop(base_effects[value], axis=1).sort_values(by = "pvalue").head()
    #study_data = filter_by_id(base_data, value).sort_values(by = "pvalue").head()
    return ff.create_table(filtered_data)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')