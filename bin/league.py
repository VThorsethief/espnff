import requests

from .utils import (two_step_dominance,
                    power_points, )
from .team import Team
from .settings import Settings
from .matchup import Matchup
from .exception import (PrivateLeagueException,
                        InvalidLeagueException,
                        UnknownLeagueException, )
import urllib.request as urllib2
# from bs4 import BeautifulSoup
from .leader import (OffensiveLeader, KickerLeader, DefensiveLeader)
import datetime
from bin import fileWriter as fw
from bin import jsonFormat
from bin import nflPlayer
import os


class League(object):
    #Generates a league instance using the year and cookies SWID and espn2 from the user's browser
    def __init__(self, year, espn_s2=None, swid=None, new_request = None):
        # self.league_id = league_id
        self.year = year
        self.ENDPOINT = "http://games.espn.com/ffl/api/v2/"
        self.teams = []
        self.espn_s2 = espn_s2
        self.swid = swid
        self.new_request = new_request
        self.max_stats = {}

        self._fetch_league()
        if self.new_record:
            fw.writeToFile(self, "tests", "testRecord")


    def __repr__(self):
        return 'League(%s, %s)' % (self.league_id, self.year, )

    # Method for obtaining the league data through a json request or reading it from file.
    # -Checks to see if the date written at the top of the record matches today's date. If the date is different from
    # today, then makes a new json request. If the date is the same as today, then the league data is taken from a text
    # file.
    def _fetch_league(self):
        # Sets the new Record value thats used throughout the league object. The idea is that if a request was already
        # made to ESPN, then the program will read the data from file rather than make a new request. This is
        # Particularly useful during debuging to prevent multiple requests and getting your IP locked. Can be overwritten
        # by passing an argument to the League Constructor
        if (self._get_date_from_file("tests", "testRecord") == str(datetime.date.today())) or not self.new_request:
            self.new_record = False
        else:
            self.new_record = True
        params = {
            # 'leagueId': self.league_id,  #this value can be added in if the browser cookies are no longer needed.
            'seasonId': self.year
        }
        cookies = None
        # If cookies are given, uses them to sign into a private league.
        if self.espn_s2 and self.swid:
            cookies = {
                'espn_s2': self.espn_s2,
                'SWID': self.swid
            }
        if self.new_record:
            r = requests.get('%sleagueSettings' % (self.ENDPOINT,), params=params, cookies=cookies)
            self.status = r.status_code
            data = r.json()
            if self.status == 401:
                raise PrivateLeagueException(data['error'][0]['message'])
            elif self.status == 404:
                raise InvalidLeagueException(data['error'][0]['message'])
            elif self.status != 200:
                raise UnknownLeagueException('Unknown %s Error' % self.status)
        else:
            data = fw.process_file_list()
        self.league_id = data['metadata']['leagueId']
        self._fetch_teams(data)
        self._fetch_settings(data)
        # self.leaders = self._fetch_leader_pool()    # This line was ommitted, there might be some use for the leader
        # pool in the future, but for now finding the "pooled player" leaders will suffice
        self.pooledPlayers = self.fetch_pooled_players(self.year, "weekStats", self.current_week)




    # Fetches the teams for the league. Reads through the data and for every team entry will create a new Team object
    def _fetch_teams(self, data):
        # Fetch teams in a league and uses that to find the current week in the season
        if self.new_record:
            teams = data['leaguesettings']['teams']
        else:
            teams = fw.archive_teams() #Will read teams from record
        for team in teams:
            self.teams.append(
                Team(teams[team], data['metadata']['leagueId'], data['metadata']['seasonId'], self.espn_s2,
                    self.swid, self.new_record))
        # replace opponentIds in schedule with team instances
        for team in self.teams:
            for week, matchup in enumerate(team.schedule):
                for opponent in self.teams:
                    if matchup == opponent.team_id:
                        team.schedule[week] = opponent

        # calculate margin of victory
        for team in self.teams:
            for week, opponent in enumerate(team.schedule):
                mov = team.scores[week] - opponent.scores[week]
                team.mov.append(mov)

        # sort by team ID
        self.teams = sorted(self.teams, key=lambda x: x.team_id, reverse=False)

        # Gets the current week for making a request through the NFL API
        self.current_week = self.get_current_week()

    # Sets the current week for making NFL API requests, uses the scores from the first team in the league to find the
    # "index" at which the score is zero. The theory is that the chance of a fantasy team scoring zero points in a week
    # is very small.
    def get_current_week(self):
        index = 0
        for score in self.teams[0].scores:
            if score == 0 and index == 0:
                return 0
            elif score == 0:
                return index
            index += 1

    #For genertating a Settings object for the league
    def _fetch_settings(self, data):
        self.settings = Settings(data, self.new_record)

    # For generating power rankings
    def power_rankings(self, week):
        '''Return power rankings for any week'''

        # calculate win for every week
        win_matrix = []
        teams_sorted = sorted(self.teams, key=lambda x: x.team_id,
                              reverse=False)

        for team in teams_sorted:
            wins = [0]*32
            for mov, opponent in zip(team.mov[:week], team.schedule[:week]):
                opp = int(opponent.team_id)-1
                if mov > 0:
                    wins[opp] += 1
            win_matrix.append(wins)
        dominance_matrix = two_step_dominance(win_matrix)
        power_rank = power_points(dominance_matrix, teams_sorted, week)
        return power_rank


    def scoreboard(self, week=None):
        '''Returns list of matchups for a given week'''
        params = {
            'leagueId': self.league_id,
            'seasonId': self.year
        }
        if week is not None:
            params['matchupPeriodId'] = week

        r = requests.get('%sscoreboard' % (self.ENDPOINT, ), params=params)
        self.status = r.status_code
        data = r.json()

        if self.status == 401:
            raise PrivateLeagueException(data['error'][0]['message'])

        elif self.status == 404:
            raise InvalidLeagueException(data['error'][0]['message'])

        elif self.status != 200:
            raise UnknownLeagueException('Unknown %s Error' % self.status)

        matchups = data['scoreboard']['matchups']
        result = [Matchup(matchup) for matchup in matchups]

        for team in self.teams:
            for matchup in result:
                if matchup.home_team == team.team_id:
                    matchup.home_team = team
                if matchup.away_team == team.team_id:
                    matchup.away_team = team

        return result

    #This method retreives the "Leaders" outlined in the table on espn.com leaderboard. Reteives the information by
    # webscraping.
    def _fetch_leader_pool(self):
        leaders = []
        if self.new_record:
            page = urllib2.urlopen('http://games.espn.com/ffl/leaders')
            soup = BeautifulSoup(page, 'html.parser')
            rows = soup.find_all('tr', attrs={'class': 'pncPlayerRow'})
            for player in rows:
                stats = player.contents
                position_break = stats[0].contents[1].split(" ")
                if len(position_break) == 2:
                    position_break = position_break[1].split("\xa0")
                    position = position_break[1]
                elif len(position_break) == 1:
                    position = position_break[0][-4:]
                else:
                    position = position_break[2]
                if position.find("K") != -1:
                    leaders.append(KickerLeader(stats, position, new_record=self.new_record))
                elif position.find("D") != -1:
                    leaders.append(DefensiveLeader(stats, position, self.new_record))
                else:
                    leaders.append(OffensiveLeader(stats, position, self.new_record))
        else:
            leaders = fw.get_leaders_from_file(self.new_record)
        return leaders

    # Retrieves the date of the file was written. Looks at the first line of the document,parses out the date and
    # returns it.
    def _get_date_from_file(self, file_path, file_name):
        try:
            file = open(file_path + "\\" + file_name + ".txt")
            first_line = file.readline().rstrip()
            date = str(first_line.split(" ")[0])
            file.close()
        except FileNotFoundError:
            file = open(os.path.dirname(os.getcwd()) + "\\" + file_path + "\\" + file_name + ".txt", "r")
            first_line = file.readline().rstrip()
            date = str(first_line.split(" ")[0])
            file.close()
        finally:

            return date

    # Uses the NFL API to retrieve player data for the given year. can retrieve either season stats or weekstats. If
    # using weekstats, can specify the week, defaults to 1.
    def fetch_pooled_players(self, year, statType, week):
        formatter = jsonFormat.generate_dict()
        names_array = []
        # Generates an array of all the names in the fantasy league
        for y in range(len(self.teams)):
            names_array.append([])
            for x in range(len(self.teams[y].roster)):
                names_array[y].append(self.teams[y].roster[x].firstName.lower() + " " + self.teams[y].roster[x].lastName.lower())
        # Makes a request if there's a "new record"
        if self.new_record:
            url = "http://api.fantasy.nfl.com/v1/players/stats?statType=" + statType +"&week=" + str(week) + "&season=" + str(year) + "&format=json"
            data = requests.get(url)
            week_requests = []
            week_num = 1
            # Makes multiple requests to generate the scores each week for the players
            while week_num <= week:
                temp_url = "http://api.fantasy.nfl.com/v1/players/stats?statType=" + statType +"&week=" + str(week_num) + "&season=" + str(year) + "&format=json"
                temp_request = requests.get(temp_url)
                week_requests.append(temp_request.json()['players'])
                week_num +=1
            merged_week_points = self.merge_week_points(week_requests)
            # To notify if theres an error in the request
            if data.reason != "OK":
                print(data.reason)
            data = data.json()
            players = data['players']
            # Attaches the week scores to players in the league
            for player in players:
                for stat in formatter:
                    if player["stats"].get(str(stat), "Entry Not Found") != "Entry Not Found":
                        player[formatter[stat]["abbr"]] = player["stats"][str(stat)]
                    else:
                        player[formatter[stat]["abbr"]] = 0
                del player["stats"]
                try:
                    player['weekScores'] = merged_week_points[player['name']]
                except KeyError:
                    player['weekScores'] = 0
                for x in range(len(names_array)):
                    try:
                        finder = names_array[x].index(player['name'].lower())
                        self.teams[x].roster[finder].set_scores(player['weekScores'])
                    except ValueError:
                        continue
        # For reading the pooled data from file.
        else:
            players = fw.get_nflPlayers_from_file()
            for player in players:
                for x in range(len(names_array)):
                    try:
                        finder = names_array[x].index(player['name'].lower())
                        self.teams[x].roster[finder].set_scores(player['weekScores'])
                    except ValueError:
                        continue
        final_player_list = []
        index = 0
        # Ties the NFL reference to the fantasy player.
        for player in players:
            final_player_list.append(nflPlayer.NFLPlayer(player))
            for x in range(len(names_array)):
                try:
                    finder = names_array[x].index(player['name'].lower())
                    self.teams[x].roster[finder].set_nfl_reference(final_player_list[index])
                except ValueError:
                    continue
            index += 1

        return final_player_list

    # Merges the scores for subsequent weeks to generate a vector of scores for each player, with each item being that
    # weeks scores.
    def merge_week_points(self, requests):
        merged = {}
        for i in range(len(requests)):
            for k in requests[i]:
                try:
                    if len(merged[k['name']]) == 0:
                        merged[k['name']] = [k['weekPts']]
                    else:
                        merged[k['name']].append(k['weekPts'])
                except KeyError:
                    merged[k['name']] = [k['weekPts']]
                    continue
        return merged

# Returns a list of the team owners
    def get_owners(self):
        owners = []
        for team in self.teams:
            owners.append(team.owner)
        return owners

# generates a list of the teams "offensive power" within the league.
    def get_offensive_power(self):
        power = []
        for team in self.teams:
            power.append(team.offensivePower)
        return power

# generates a list of defensive power within the league.
    def get_defensive_power(self):
        power = []
        for team in self.teams:
            power.append(team.defensivePower)
        return power

    def merge_team_player_scores(self):
        for team in self.teams:
            for player in team.roster:
                index = self.pooledPlayers.index(player.firstName + " " + player.lastName)
                player.set_scores(self.pooledPlayers[index].scores)

    def set_max_stats(self, player):
        defensive_positions = ["DEF", "LB", "EDR", "Safety"]
        if self.max_stats['passing'] is None:
            self.max_stats['passing'] = player.pvoRank
        elif player.position == 'QB' and player.pvoRank > self.max_stats['passing']:
            self.max_stats['passing'] = player.pvoRank
        elif player.position == 'RB' and player.pvoRank > self.max_stats['rushing']:
            self.max_stats['rushing'] = player.pvoRank
        elif (player.position == 'WR' or player.position == 'TE') and player.pvoRank > self.max_stats['receiving']:
            self.max_stats['receiving'] = player.pvoRank
        elif player.position in defensive_positions and player.pvoRank > self.max_stats['defense']:
            self.max_stats['defense'] = player.pvoRank
        elif player.position == 'K' and player.pvoRank > self.max_stats['kicking']:
            self.max_stats['kicking'] = player.pvoRank













