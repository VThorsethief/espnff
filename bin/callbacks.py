from dash.dependencies import (Input, Output)
# from .instance import app
# from .data import myLeague, board
#
# app.layout = board.main_page
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from .startup import app
import json

@app.callback(
    Output(component_id='leagueDash', component_property='style'),
    [Input(component_id='dashSelector', component_property='value')]
)
def update_league_summary(input_value):
    if input_value != "League Summary":
        return {'display': 'none'}

#
@app.callback(
    Output(component_id='mainSub', component_property='children'),
    [Input(component_id='dashSelector', component_property='value'),
     Input(component_id='teamData', component_property='children')]

)
def show_team_layout(input_value, team_data):
    all_teams = dict(json.loads(team_data))
    selected_team = json.loads(all_teams[input_value])
    scatter_list = []
    for player in selected_team['player_scatter']:
        scatter_list.append(go.Scatter(
            x = player['x'],
            y = player['y'],
            name = player['name'],
            mode = player['mode']
        ))
    layout =  html.Div(
        id = "teamPanel",
        children=[
                html.H1(
                    id = 'teamHeader',
                    children = selected_team['owner'],
                    className = 'twelve columns'
                ),
                html.Div(
                    children=[
                        html.Div(dcc.Graph(
                            id="teamLine",
                            figure=go.Figure(
                                data =scatter_list,
                                layout=go.Layout(
                                    title="Player Score Progress over time",
                                    yaxis=dict(title="Team Scores")
                                )
                            )
                        )),
                        html.Div(dcc.Graph(
                            id="teamBar",
                            figure=go.Figure(
                                data=[
                                    {'x': ["Offensive Power", 'Defensive Power', 'Kicking power'],
                                     'y': [selected_team['offensive_power'], selected_team['defensive_power'],
                                           selected_team['kicking_power']],
                                     'type': 'bar',
                                     'name': selected_team['owner']}
                                ],
                                layout=go.Layout(
                                    title="Relative Team Strengths"
                                )
                            )
                        ))], className='four columns'),
                html.Div(
                    children=[
                        dcc.Graph(
                            id = "teamScatter",
                            figure = go.Figure(
                                data = [go.Scatter3d(
                                    x = selected_team['player_position'],
                                    y=selected_team['player_total_points'],
                                    z=selected_team['player_week_points'],
                                    text=selected_team['player_names'],
                                    mode="markers",

                                    marker=dict(
                                        sizemode='diameter',
                                        sizeref=2,
                                        size=selected_team['player_percent_owned'],
                                        color=selected_team['player_percent_started'],
                                        colorscale='Viridis',
                                        colorbar=dict(title='Percent<br>Started')),

                                )],
                                layout=go.Layout(
                                    height=1000,
                                    width=1000,
                                    title=selected_team['owner']
                                )
                            )
                        )
                    ],
                    className="four columns"

                )


            ]
        )
    return layout



# @app.callback(
#     Output(component_id='teamDash', component_property='style'),
#     [Input(component_id='dashSelector', component_property='value')]
# )
# def update_team_layout(input_value):
#     if input_value == "League Summary" or input_value == "League Bubble":
#         return {'display': 'none'}
#
# @app.callback(
#     Output(component_id='teamScatter', component_property='figure'),
#     [Input(component_id='dashSelector', component_property='value')]
# )
# def update_team_data(input_value):
#     if input_value != "League Summary" and input_value != "League Bubble":
#         i = board.index_list.index(input_value)
#         player_total_points = []
#         player_week_points = []
#         player_percent_started = []
#         player_percent_owned = []
#         player_names = []
#         player_position = []
#         for player in myLeague.teams[i].roster:
#             try:
#                 player_total_points.append(player.totalPoints)
#                 player_percent_started.append(player.percentStarted)
#                 player_percent_owned.append(player.percentOwned)
#                 player_names.append(player.firstName + " " + player.lastName)
#                 player_position.append(player.getPosition())
#                 player_week_points.append(player.NFLreference.weekPts)
#             except AttributeError:
#                 player_week_points.append(0)
#                 continue
#         data = [dict(
#             x=player_position,
#             y=player_total_points,
#             z=player_week_points,
#             text=player_names,
#             mode="markers",
#             type='scatter3d',
#
#             marker=dict(
#                 sizemode='diameter',
#                 sizeref=2,
#                 size=player_percent_owned,
#                 color=player_percent_started,
#                 colorscale='Viridis',
#                 colorbar=dict(title='Percent<br>Started')))]
#
#         layout = dict(
#             height=1000,
#             width=1000,
#             title=myLeague.teams[i].owner,
#             scene=dict(
#                 xaxis=dict(
#                     title='Player Position'
#                 ),
#                 yaxis=dict(
#                     title='Total Season Points'
#                 ),
#                 zaxis=dict(
#                     title="Week Points"
#                 )
#             )
#
#         )
#
#         return dict(
#             data=data,
#             layout=layout
#         )
#
# @app.callback(
#     Output(component_id='teamLine', component_property='figure'),
#     [Input(component_id='dashSelector', component_property='value')]
# )
# def update_team_line(input_value):
#     if input_value != "League Summary" and input_value != "League Bubble":
#         i = board.index_list.index(input_value)
#         scatter_list = []
#         for player in myLeague.teams[i].roster:
#             scatter_list.append(
#                 dict(
#                     x=board.week_list,
#                     y=player.scores,
#                     name=player.__repr__(),
#                     mode='lines+markers',
#                     type='scatter'
#                 )
#             )
#         layout = dict(
#             title="Individual Player Progress"
#         )
#         return dict(
#             data=scatter_list,
#             layout=layout
#         )
#
# @app.callback(
#     Output(component_id='teamBar', component_property='figure'),
#     [Input(component_id='dashSelector', component_property='value')]
# )
# def update_team_line(input_value):
#     if input_value != "League Summary" and input_value != "League Bubble":
#         i = board.index_list.index(input_value)
#         barData = [dict(
#             x=["Offensive Power", 'Defensive Power', 'Kicking power'],
#             y=[myLeague.teams[i].offensivePower, myLeague.teams[i].defensivePower,
#                myLeague.teams[i].kicking_power],
#             type='bar',
#             name=myLeague.teams[i].owner
#         )]
#         layout = dict(
#             title="Distribution of player Scores"
#         )
#         return dict(
#             data=barData,
#             layout=layout
#         )
#
# @app.callback(
#     Output(component_id='teamHeader', component_property='children'),
#     [Input(component_id='dashSelector', component_property='value')]
# )
# def update_team_header(input_value):
#     if input_value != "League Summary" and input_value != "League Bubble":
#         i = board.index_list.index(input_value)
#         return myLeague.teams[i].owner
#


## !!!!!  This is where the signin happens, we need to have functioality to import the league and the board
## upon instance of the callback, and returs the board main page when the league is built and the board is generated.
## The sign in will be the original layout.

# Changing the value of the selection for the main drop down menu.
