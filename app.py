from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio


import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app = Dash(external_stylesheets=[dbc.themes.DARKLY])

pio.templates.default = "plotly_dark"

app.layout = html.Div(children=[
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    ),

    html.Br(),
    html.Div(children=[
        html.H1(children='Header1'),
        html.Label('Text Box:'),
        html.Div(children=[
            dcc.Input(id='test-input', value='placeholder'),
            html.Div(id='output-text')
        ])]
    )
])


@app.callback(
    Output('output-text', 'children'),
    Input('test-input', 'value'))
def update_placeholder_text(new_text):
    return new_text.upper()


@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run(debug=True)
