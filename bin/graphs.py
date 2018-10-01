import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

class DashBoard(object):
    def __init__(self, league):
        self.league = league
        self.week_list = self.generate_week_list()
        self.radar_list, self.scatter_lines, self.team_names, self.drop_down_options,\
            self.index_list = self.generate_team_lists()
        self.pooled_season_points, self.pooled_week_points, self.pooled_proj_week_points, self.pooled_names, \
            self.pooled_position = self.generate_pooled_player_lists()
        self.drop_down_struct = self.generate_drop_down_list()
        self.league_panel_title = self.generate_league_panel_title()
        self.league_bubble = self.generate_league_bubble()
        self.league_page = self.generate_league_page()
        # self.league_bubble_title = self.generate_league_bubble_title
        self.team_layout = self.generate_team_layout(0)
        self.current_setting = "League Summary"
        self.main_page = self.generate_main_page()

    def generate_week_list(self):
        week_list = []
        for w in range(13):
            week_list.append("Week " + str(w + 1))
        return week_list

    def generate_team_lists(self):
        radar_list = []
        scatter_lines = []
        team_layout_list = []
        team_names = []
        index_list = []
        drop_down_options = [{'label': "League Summary", 'value' : 'League Summary'},
        {'label' : "League Bubble", 'value' : 'League Bubble'}]
        for team in self.league.teams:
            radar_list.append(go.Scatterpolar(
                r=[team.passing_power, team.rushing_power,
                   team.kicking_power, team.defensivePower],
                theta=["Passing", "Rushing", "Kicking", "Defense"],
                # fill='toself',
                name=team.owner
            ))
            scatter_lines.append(
                go.Scatter(
                    x=self.week_list,
                    y=team.scores,
                    name=team.owner,
                    mode='lines+markers'
                )
            )
            team_names.append(team.owner)
            temp = {
                'label': team.owner,
                'value': team.owner
            }
            drop_down_options.append(temp)
            index_list.append(team.owner)
        return radar_list, scatter_lines, team_names, drop_down_options, index_list

    def generate_pooled_player_lists(self):
        pooled_season_pts = []
        pooled_week_points = []
        pooled_proj_week_pts = []
        pooled_names = []
        pooled_position = []
        for player in self.league.pooledPlayers:
            pooled_season_pts.append(player.seasonPts)
            pooled_week_points.append(player.weekPts)
            pooled_proj_week_pts.append(player.weekProjectedPts)
            pooled_names.append(player.name)
            pooled_position.append(player.position)
        return pooled_season_pts, pooled_week_points, \
               pooled_proj_week_pts, pooled_names, pooled_position

    def generate_drop_down_list(self):
        return html.Div(
            dcc.Dropdown(
                id = "dashSelector",
                options = self.drop_down_options,
                value = 'League Summary'
                # value = 'League Bubble'
            ),
            style = {'width': '20%'},
            className= "five columns"
        )

    def change_drop_down_list(self, input_value):
        drop_down = html.Div(
            dcc.Dropdown(
                id = "dashSelector",
                options = self.drop_down_options,
                value = input_value
            ),
            style = {'width': '20%'}
        )
        return drop_down

    def generate_league_page(self):
        return html.Div(
            id = "leagueDash",
            children = [
                html.Div(
                    children=[
                        dcc.Graph(
                            id="leagueLine",
                            figure=go.Figure(
                                data=self.scatter_lines,
                                layout=go.Layout(
                                    title="Scores Over Time",
                                    yaxis=dict(title="Team Score")
                                )
                            )
                        ),

                        dcc.Graph(
                            id='Offensive Power',
                            figure={
                                'data': [
                                    {'x': self.league.get_owners(), 'y': self.league.get_offensive_power(), 'type': 'bar',
                                     'name': 'Offensive'},
                                    {'x': self.league.get_owners(), 'y': self.league.get_defensive_power(), 'type': 'bar',
                                     'name': 'Defensive'},
                                ],
                                'layout': {
                                    'title': 'Offensive vs. Defensive Power'
                                }
                            }
                        )

                    ],
                    className = "six columns",
                    style={'margin-left': '1%'}

                ),
                html.Div(
                    children= [
                            dcc.Graph(
                                id= "leagueRadar",
                                figure = go.Figure(
                                    data=self.radar_list,
                                    layout =
                                    go.Layout(
                                        polar = dict(
                                            radialaxis = dict(
                                                visible = True,
                                                range = [0,250]
                                            )
                                        ), showlegend= True,
                                        title= "Strengths across all teams"
                                    )

                                )

                            ),
                            self.league_bubble
                    ],
                    className="six columns",
                    style={'margin-left': '1%', 'margin-top': 'auto'})])


    def generate_league_panel_title(self):
        return html.H2(
            children = "Across League"
        )

    def generate_league_bubble(self):
        return dcc.Graph(
                    id="leagueScatter",
                    figure=go.Figure(
                        data=[go.Scatter3d(
                            x=self.pooled_position,
                            y=self.pooled_season_points,
                            z=self.pooled_week_points,
                            text=self.pooled_names,
                            mode="markers",

                            marker=dict(
                                sizemode='diameter',
                                sizeref=1,
                                size=self.pooled_proj_week_points,
                                color=self.pooled_proj_week_points,
                                colorscale='Viridis',
                                # colorbar=dict(title='None')),

                            ))],
                        layout=go.Layout(
                            height=500,
                            width=1000,
                            title="Bubble Plot for All Players"
                        )
                    )
                )

    # def generate_team_bubble(self, index):



    # def generate_league_bubble_title(self):

    def generate_main_page(self):
        main =  html.Div(
            id = 'main',
            children=[
                html.Div(
                    id = 'header',
                    children=[
                        html.H1(
                            id='title',
                            children="Fantasy Analyst: " + self.league.settings.name,
                            className='seven columns'
                        ),

                        self.drop_down_struct
                    ]
                ),

                html.Div(
                    id = 'mainSub',
                    children=[
                        self.league_page,
                        # self.league_bubble,
                        self.team_layout
                    ]
                )

                ]

        )
        return main
    def generate_team_layout(self, i):
        player_scatter = []
        player_total_points = []
        player_week_points = []
        player_percent_started = []
        player_percent_owned = []
        player_names = []
        player_position = []
        for player in self.league.teams[i].roster:
            player_scatter.append(
                go.Scatter(
                    x=self.week_list,
                    y=player.scores,
                    name=player.__repr__(),
                    mode='lines+markers'
                )
            )
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

        team_layout = html.Div(
            id="teamDash",
            children=[
                html.H1(id = 'teamHeader',
                        children=self.league.teams[i].owner,
                        className="twelve columns"),
                html.Div(
                    children=[
                        html.Div(dcc.Graph(
                            id="teamLine",
                            figure=go.Figure(
                                data=player_scatter,
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
                                     'y': [self.league.teams[i].offensivePower, self.league.teams[i].defensivePower,
                                           self.league.teams[i].kicking_power],
                                     'type': 'bar',
                                     'name': self.league.teams[i].owner}
                                ],
                                layout = go.Layout(
                                    title = "Relative Team Strengths"
                                )
                            )
                        ))], className='four columns'),
                html.Div(
                    children=[
                        dcc.Graph(
                            id="teamScatter",
                            figure=go.Figure(
                                data=[go.Scatter3d(
                                    x=player_position,
                                    y=player_total_points,
                                    z=player_week_points,
                                    text=player_names,
                                    mode="markers",

                                    marker=dict(
                                        sizemode='diameter',
                                        sizeref=2,
                                        size=player_percent_owned,
                                        color=player_percent_started,
                                        colorscale='Viridis',
                                        colorbar=dict(title='Percent<br>Started')),

                                )],
                                layout=go.Layout(
                                    height=1000,
                                    width=1000,
                                    title=self.league.teams[i].owner
                                )
                            )
                        )
                    ],
                    className="four columns"

                )

            ]
        )
        return team_layout


    def update_dash_board(self, input_value):
        self.drop_down_struct = self.change_drop_down_list(input_value)
        if input_value == "League Summary":
            return [self.league_panel_title, self.drop_down_struct, self.league_page]
        elif input_value == 'League Bubble':
            return[self.drop_down_struct, self.league_bubble]
        else:
            i = self.index_list.index(input_value)
            self.team_layout = self.generate_team_layout(i)
            return [self.drop_down_struct, self.team_layout]

    def update_setting(self, new_setting):
        if new_setting != self.current_setting:
            print("new selection")
            self.current_setting = new_setting
