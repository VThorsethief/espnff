import requests
from .exception import UnknownLeagueException
from .player import Player
from bin import fileWriter as fw
class Team(object):
    '''Teams are part of the league'''
    def __init__(self, data, leagueId, seasonId, espn_s2, swid, new_record):
        self.team_id = data['teamId']
        self.league_id = leagueId
        self.season_id = seasonId
        self.team_abbrev = data['teamAbbrev']

        #If there is a new record request, then a request is sent to espn for the team roster
        if new_record:
            self.team_name = "%s %s" % (data['teamLocation'], data['teamNickname'])
        else:
            self.team_name = data["teamName2"]

        self.division_id = data['division']['divisionId']
        self.division_name = data['division']['divisionName']
        self.wins = data['record']['overallWins']
        self.losses = data['record']['overallLosses']
        self.points_for = data['record']['pointsFor']
        self.points_against = data['record']['pointsAgainst']
        self.owner = "%s %s" % (data['owners'][0]['firstName'],
                                data['owners'][0]['lastName'])
        self.schedule = []
        self.scores = []
        self.mov = []
        self.espn_s2 = espn_s2
        self.swid = swid
        if new_record:
            self._fetch_schedule(data)
            self.roster = self.get_roster()
        else:
            self.roster = self.get_roster_from_file()
            self.scores = data['scores']
        self.offensivePower, self.defensivePower = self.generate_power_scores()
        self.passing_power, self.rushing_power, self.kicking_power = self.get_offensive_powers()


    #Representation is the name of the team
    def __repr__(self):
        return 'Team(%s)' % (self.team_name, )

    #The team Schedule
    def _fetch_schedule(self, data):
        '''Fetch schedule and scores for team'''
        matchups = data['scheduleItems']

        for matchup in matchups:
            if not matchup['matchups'][0]['isBye']:
                if matchup['matchups'][0]['awayTeamId'] == self.team_id:
                    score = matchup['matchups'][0]['awayTeamScores'][0]
                    opponentId = matchup['matchups'][0]['homeTeamId']
                else:
                    score = matchup['matchups'][0]['homeTeamScores'][0]
                    opponentId = matchup['matchups'][0]['awayTeamId']
            else:
                score = matchup['matchups'][0]['homeTeamScores'][0]
                opponentId = matchup['matchups'][0]['homeTeamId']

            self.scores.append(score)
            self.schedule.append(opponentId)


    def get_roster(self):
        '''Get roster for a given week'''
        params = {
            "leagueId": self.league_id,
            'seasonId': self.season_id,
            'teamId': self.team_id
        }

        cookies = {
            'espn_s2': self.espn_s2,
            'SWID': self.swid
        }
        newRequest = requests.get('http://games.espn.com/ffl/api/v2/boxscore', params=params, cookies = cookies)
        status = newRequest.status_code
        roster = []
        if status != 200:
            raise UnknownLeagueException('Unknown Error Getting roster for team ' + self.team_id % status)
        else:
            requestData = newRequest.json()
            for team in requestData['boxscore']['teams']:
                if team['teamId'] == self.team_id:
                    for player in team['slots']:
                        if player.get('player', 0) != 0:
                            roster.append(Player(player))
        return roster

    def get_roster_from_file(self):
        players_from_file = fw.get_roster_from_file(self.team_abbrev)
        roster = []
        for player in players_from_file:
            roster.append(Player(player))
        return roster

    def generate_power_scores(self):
        offensive_positions = ["QB", "RB", "WR", "TE", "K"]
        defensive_positions = ["DEF", "LB", "EDR", "Safety"]
        offensive_score = 0
        defensive_score = 0
        for player in self.roster:
            try:
                if offensive_positions.index(player.getPosition()):
                    offensive_score += float(player.projectedPoints)
                elif defensive_positions.index(player.getPosition()):
                    defensive_score += float(player.totalPoints)
            except ValueError:
                try:
                    if defensive_positions.index(player.getPosition()):
                        defensive_score += float(player.totalPoints)
                except ValueError:
                    continue
        return offensive_score, defensive_score

    def get_player_scores(self):
        scores = []
        for player in self.roster:
            scores.append(player.projectedPoints)
        return scores

    def get_player_names(self):
        names = []
        for player in self.roster:
            names.append(player.firstName + player.lastName + "")
        return names

    def get_offensive_powers(self):
        p_power = 0
        r_power = 0
        k_power = 0
        for player in self.roster:
            if player.getPosition() == "QB" or player.getPosition() == "WR" or player.getPosition() == "TE":
                p_power += player.pvoRank
            elif player.getPosition() == "RB":
                r_power += player.pvoRank
            elif player.getPosition() == "K":
                k_power += player.pvoRank
        return p_power, r_power, k_power
