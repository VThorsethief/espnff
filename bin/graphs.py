import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import json

class DashBoard(object):
    def __init__(self, league):
        self.league = league
        self.team_layouts = {}
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
        self.current_setting = "League Summary"
        self.main_page = self.generate_main_page()

    # These are week labels for each week in the regular season, does not include the post-season
    def generate_week_list(self):
        week_list = []
        for w in range(13):
            week_list.append("Week " + str(w + 1))
        return week_list

    # This method generates the team info for the leagues, its more broad info like team names and owners, not specific
    # info like players.
    def generate_team_lists(self):
        radar_list = []
        scatter_lines = []
        team_names = []
        index_list = []
        # Initial drop down options for the layout input. These are the options that are general across the league,
        # not the individual teams
        drop_down_options = [{'label': "League Summary", 'value' : 'League Summary'},
        {'label' : "League Bubble", 'value' : 'League Bubble'}]
        # Populates the scatter lines, team names, and drop down options
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
        self.build_team_layouts()
        return radar_list, scatter_lines, team_names, drop_down_options, index_list

    # This organizes the data for the pooled players across the entire NFL League, not by fantasy team.
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

    # Builds the actual structure for the drop down list using the dash framework.
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

    # Changes the selected value for the drop down list.
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
            id = 'mainBuilt',
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
                        # self.team_layout
                    ]
                ),
                html.P(id = "teamData", children=self.team_layouts, style={'display': 'none'})
                ]

        )
        return main



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

    def build_team_layouts(self):
        for team in self.league.teams:
            temp = TeamBoard(team, self.week_list)
            self.team_layouts[team.owner] = json.dumps(temp.generate_team_list())
        self.team_layouts = json.dumps(self.team_layouts)

# The individual team Layout per team. This stores the data specific to the teams. Allows for better organization
class TeamBoard(object):
    def __init__(self, team, weeks):
        self.team = team
        self.player_scatter = []
        self.player_total_points = []
        self.player_week_points = []
        self.player_percent_started = []
        self.player_percent_owned = []
        self.player_names = []
        self.player_position = []
        self.weeks = weeks
        self.player_scatter_dict = {}
        for player in team.roster:
            self.player_scatter.append(
                go.Scatter(
                    x = weeks,
                    y = player.scores,
                    name = player.__repr__(),
                    mode = 'lines+markers'
                ))
            self.player_scatter_dict[player.__repr__()] = dict(
                x = weeks,
                y = player.scores,
                name = player.__repr__(),
                mode = 'lines+markers'

            )
            try:
                self.player_total_points.append(player.totalPoints)
                self.player_percent_started.append(player.percentStarted)
                self.player_percent_owned.append(player.percentOwned)
                self.player_names.append(player.firstName + " " + player.lastName)
                self.player_position.append(player.getPosition())
                self.player_week_points.append(player.NFLreference.weekPts)
            except AttributeError:
                self.player_week_points.append(0)
                continue
        self.team_layout = None
        # self.generate_team_layout()

    def generate_team_list(self):
        temp = dict(
            week_labels = self.weeks,
            player_total_points = self.player_total_points,
            player_week_points = self.player_week_points,
            player_percent_started = self.player_percent_started,
            player_percent_owned = self.player_percent_owned,
            player_names = self.player_names,
            player_position = self.player_position,
            player_scatter = self.player_scatter_dict,
            owner = self.team.owner
        )
        return temp

    # This generates the individual team layout and serializes the layout in json to the layout can be build later.
    def generate_team_layout(self):
        self.team_layout = html.Div(
            id = self.team.__repr__(),
            children = [
                html.H1(
                    id = 'teamHeader',
                    children = self.team.owner,
                    className = 'twelve columns'
                ),
                html.Div(
                    children=[
                        html.Div(dcc.Graph(
                            id="teamLine",
                            figure=go.Figure(
                                data =self.player_scatter,
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
                                     'y': [self.team.offensivePower, self.team.defensivePower,
                                           self.team.kicking_power],
                                     'type': 'bar',
                                     'name': self.team.owner}
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
                                    x = self.player_position,
                                    y=self.player_total_points,
                                    z=self.player_week_points,
                                    text=self.player_names,
                                    mode="markers",

                                    marker=dict(
                                        sizemode='diameter',
                                        sizeref=2,
                                        size=self.player_percent_owned,
                                        color=self.player_percent_started,
                                        colorscale='Viridis',
                                        colorbar=dict(title='Percent<br>Started')),

                                )],
                                layout=go.Layout(
                                    height=1000,
                                    width=1000,
                                    title=self.team.owner
                                )
                            )
                        )
                    ],
                    className="four columns"

                )


            ]
        )
        self.team_layout = json.dumps(self.team_layout)



