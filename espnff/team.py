import requests
from .exception import UnknownLeagueException
from .player import Player
class Team(object):
    '''Teams are part of the league'''
    def __init__(self, data, leagueId, seasonId):
        self.team_id = data['teamId']
        self.league_id = leagueId
        self.season_id = seasonId
        self.team_abbrev = data['teamAbbrev']
        self.team_name = "%s %s" % (data['teamLocation'], data['teamNickname'])
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
        self._fetch_schedule(data)
        self.roster = self.get_roster()


    def __repr__(self):
        return 'Team(%s)' % (self.team_name, )

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
            'espn_s2': "AEAiHk9BLrd3k24bECp7EdRWKIUMi7blgeQCRyDeHpVMtz1AKSQQhXAaymmp2JMoDQ941uS6R6opM4lu%2FblNkgsFS3MSVqPgVWZEAKH0EsQTq15LP0eP2YKOM%2BtEAuDXwQmifpLHRpjSrNPUDqp%2BXQatuQ0eKnrePlG50Vr%2Ft01nPXoo0%2BgpmD1LVFmRnKCX3J%2FKb%2BdDQZifeI3El4%2FV7gPlpgWDIGQ023RzUod0tpUJkZjMQQjaTmRqG88fypDR9Q2paczm%2Fqj3kwmXiaRdKnSp",
            'SWID': "{F09B888C-9941-4A01-9B88-8C99417A0114}"
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
