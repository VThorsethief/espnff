import dash
import dash_core_components as dcc
import dash_html_components as html
from .instance import app
from bin import (league, graphs)
from .data import year, swid, espn2

index = html.Div(
    id = 'main',
    children = [
        html.Div(
            id = 'signIn',
            children=[
                dcc.Input(
                    id='idInput',
                    placeholder="Enter League Id Here...",
                    type = 'text'
                ),
                html.Button('Submit',
                           id = 'submitButton',
                            className='button button-primary')
            ],
            style={'margin-left':'auto'}
        )
    ])
app.layout = index

myLeague = None
board = None


@app.callback(
    dash.dependencies.Output('main', 'children'),
    [dash.dependencies.Input(component_id='submitButton', component_property='n_clicks')],
        [dash.dependencies.State('idInput', 'value')])
def buildLeague(n_clicks, value):
    print(value)
    if value is not None and n_clicks > 0:
        myLeague = league.League(year= year,league_id=value, espn_s2=espn2,swid=swid)
        board = graphs.DashBoard(myLeague)
        from . import callbacks
        return board.main_page
    else:
        return html.Div(
            id = 'signIn',
            children=[
                dcc.Input(
                    id='idInput',
                    placeholder="Enter League Id Here...",
                    type = 'text'
                ),
                html.Button('Submit',
                           id = 'submitButton')
            ]
        )




