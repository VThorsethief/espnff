import dash
import dash_core_components as dcc
import dash_html_components as html
from .instance import app
from bin import (league, graphs)
from dash.dependencies import (Input, Output)
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

from . import callbacks


@app.callback(
    dash.dependencies.Output('main', 'children'),
    [dash.dependencies.Input(component_id='submitButton', component_property='n_clicks')],
        [dash.dependencies.State('idInput', 'value')])
def buildLeague(n_clicks, value):
    print(value)
    if value is not None and n_clicks > 0:
        global myLeague
        myLeague = league.League(year= year,league_id=value, espn_s2=espn2,swid=swid)
        global board
        board = graphs.DashBoard(myLeague)


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


@app.callback(
    Output(component_id='leagueDash', component_property='style'),
    [Input(component_id='dashSelector', component_property='value')]
)
def update_league_summary(input_value):
    if input_value != "League Summary":
        return {'display': 'none'}

#
@app.callback(
    Output(component_id='teamDash', component_property='style'),
    [Input(component_id='dashSelector', component_property='value')]
)
def update_team_layout(input_value):
    if input_value == "League Summary" or input_value == "League Bubble":
        return {'display': 'none'}

@app.callback(
    Output(component_id='teamScatter', component_property='figure'),
    [Input(component_id='dashSelector', component_property='value')]
)
def update_team_data(input_value):
    if input_value != "League Summary" and input_value != "League Bubble":
        i = board.index_list.index(input_value)
        player_total_points = []
        player_week_points = []
        player_percent_started = []
        player_percent_owned = []
        player_names = []
        player_position = []
        for player in myLeague.teams[i].roster:
            try:
                player_total_points.append(player.totalPoints)
                player_percent_started.append(player.percentStarted)
                player_percent_owned.append(player.percentOwned)
                player_names.append(player.firstName + " " + player.lastName)
                player_position.append(player.getPosition())
                player_week_points.append(player.NFLreference.weekPts)
            except AttributeError:
                player_week_points.append(0)
                continue
        data = [dict(
            x=player_position,
            y=player_total_points,
            z=player_week_points,
            text=player_names,
            mode="markers",
            type='scatter3d',

            marker=dict(
                sizemode='diameter',
                sizeref=2,
                size=player_percent_owned,
                color=player_percent_started,
                colorscale='Viridis',
                colorbar=dict(title='Percent<br>Started')))]

        layout = dict(
            height=1000,
            width=1000,
            title=myLeague.teams[i].owner,
            scene=dict(
                xaxis=dict(
                    title='Player Position'
                ),
                yaxis=dict(
                    title='Total Season Points'
                ),
                zaxis=dict(
                    title="Week Points"
                )
            )

        )

        return dict(
            data=data,
            layout=layout
        )

@app.callback(
    Output(component_id='teamLine', component_property='figure'),
    [Input(component_id='dashSelector', component_property='value')]
)
def update_team_line(input_value):
    if input_value != "League Summary" and input_value != "League Bubble":
        i = board.index_list.index(input_value)
        scatter_list = []
        for player in myLeague.teams[i].roster:
            scatter_list.append(
                dict(
                    x=board.week_list,
                    y=player.scores,
                    name=player.__repr__(),
                    mode='lines+markers',
                    type='scatter'
                )
            )
        layout = dict(
            title="Individual Player Progress"
        )
        return dict(
            data=scatter_list,
            layout=layout
        )

@app.callback(
    Output(component_id='teamBar', component_property='figure'),
    [Input(component_id='dashSelector', component_property='value')]
)
def update_team_line(input_value):
    if input_value != "League Summary" and input_value != "League Bubble":
        i = board.index_list.index(input_value)
        barData = [dict(
            x=["Offensive Power", 'Defensive Power', 'Kicking power'],
            y=[myLeague.teams[i].offensivePower, myLeague.teams[i].defensivePower,
               myLeague.teams[i].kicking_power],
            type='bar',
            name=myLeague.teams[i].owner
        )]
        layout = dict(
            title="Distribution of player Scores"
        )
        return dict(
            data=barData,
            layout=layout
        )

@app.callback(
    Output(component_id='teamHeader', component_property='children'),
    [Input(component_id='dashSelector', component_property='value')]
)
def update_team_header(input_value):
    if input_value != "League Summary" and input_value != "League Bubble":
        i = board.index_list.index(input_value)
        return myLeague.teams[i].owner


