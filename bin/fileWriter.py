import datetime
from .leader import (Leader, NonDefensive, OffensiveLeader, KickerLeader, DefensiveLeader)
import os

#Master Function for writing the league object to file. This restricts the user from having to make too many requests
# and getting their IP locked out.
#Requires: A League object, a filepath to store and the file name. Sotres the information as a text document.
def writeToFile(league, filePath, fileName):
    try:
        file = open(filePath + "\\" + fileName + ".txt", "w")
    except FileNotFoundError:
        file = open(os.path.dirname(os.getcwd()) + "\\" + "tests" + "\\" + "offlineRecord.txt", "w")
    file.write(str(datetime.datetime.today()))
    file.write(str(league.league_id) + "\n")
    file.write(str(league.year) + "\n")
    file.write(str(league.settings.final_season_count) + '\n')
    settings = league.settings
    settings_string = [
        league.league_id,
        league.year,
        '--LeagueSettings--',
        settings.final_season_count,
        settings.keeper_count,
        settings.name,
        settings.playoff_seed_tie_rule,
        settings.playoff_team_count,
        settings.reg_season_count,
        settings.status,
        settings.team_count,
        settings.tie_rule,
        settings.trade_deadline,
        settings.undroppable_list,
        settings.veto_votes_required,
        settings.id,
        '-- Slot Category Items --'
    ]
    settings_string = convert_list_to_string(settings_string)
    file.writelines(settings_string)
    settings_roster = []
    for position in settings.roster:
        settings_roster.append(str(position) +
                               ":" + str(settings.roster[position]) + "\n")
    file.writelines(settings_roster)
    for team in league.teams:
        team_string = [
            "-- New Team --",
            team.division_id,
            team.division_name,
            team.mov,
            team.owner,
            team.points_against,
            team.points_for,
            team.scores,
            team.team_abbrev,
            team.team_name,
            team.wins,
            team.team_id,
            team.losses,
            "roster:"
            ]
        file.writelines(convert_list_to_string(team_string))
        for player in team.roster:
            player_string = [
                player.getPosition(),
                player.defaultPositionId,
                player.draftRank,
                player.firstName,
                player.healthStatus,
                player.isActive,
                player.isDroppable,
                player.isIREligible,
                player.isOnWatchList,
                player.isTradeLocked,
                player.jerseryNum,
                player.lastName,
                player.percentChange,
                player.percentOwned,
                player.percentStarted,
                player.playerRatingSeason,
                player.player_id,
                player.projectedPoints,
                player.pvoRank,
                player.totalPoints
            ]
            file.write(str(player_string) + "\n")
        opponent_schedule = []
        for opponent in team.schedule:
            opponent_schedule.append(opponent.team_id)
        file.write(str(opponent_schedule) + "\n")
        file.write(str(team.scores) + "\n")
    nflPlayers = write_nflPlayers_to_file(league.pooledPlayers)
    for entry in nflPlayers:
        file.write(str(entry) + '\n')
    file.close()

# This is for writing the league leaders to file. Takes the Leader objects, iterates them and writes them to text. The
# "Leaders" header is required, as it allows for the
def write_leaders_to_file(leaders):
    leader_list = ["Leaders:"]
    for leader in leaders:
        if isinstance(leader, OffensiveLeader):
            instance_list = [
                "Offensive Leader:",
                leader.position,
                leader.name,
                leader.passAttempts,
                leader.passCompletions,
                leader.passingTD,
                leader.passingYards,
                leader.position,
                leader.recYards,
                leader.receivingTD,
                leader.receptions,
                leader.rushingAttempts,
                leader.rushingTD,
                leader.rushingYards,
                leader.team,
                leader.totalPoints
            ]
        elif isinstance(leader, KickerLeader):
            instance_list = [
                "Kicker Leader:",
                leader.position,
                leader.name,
                leader.fiftyPlusAttempts,
                leader.fiftyPlusCompletions,
                leader.fortySubFiftyAttempts,
                leader.fortySubFiftyCompletions,
                leader.position,
                leader.sub40YardAttempts,
                leader.sub40YardCompletions,
                leader.team,
                leader.totalAttempts,
                leader.totalCompletions,
                leader.totalPoints,
                leader.xpAttempts,
                leader.xpCompletions
            ]
        elif isinstance(leader, DefensiveLeader):
            instance_list = [
                "Defensive Leader:",
                leader.position,
                leader.name,
                leader.blockedKick,
                leader.fumbleRecoveries,
                leader.intercept,
                leader.pointsAllowed,
                leader.position,
                leader.returnTD,
                leader.sacks,
                leader.safeties,
                leader.totalPoints
            ]
        leader_list.append(instance_list)
    return leader_list


# For writing the pooled NFL Players to file, assigning each attribute to a list and appending to a 2d list. The list is
# then written to a text file. Takes a list of NFL Player objects and returns a 2D list of all the attribute for writing
def write_nflPlayers_to_file(players):
    players_to_file = ["NFL Active Players"]
    for player in players:
        instance_list = [
            player.id,
            player.esbid,
            player.gsisPlayerId,
            player.name,
            player.position,
            player.teamAbbrev,
            player.seasonPts,
            player.seasonProjPts,
            player.weekPts,
            player.weekProjectedPts,
            player.gP,
            player.att,
            player.comp,
            player.inc,
            player.yds,
            player.tD,
            player.int,
            player.sacked,
            player.n300to399,
            player.n400Plus,
            player.n40PlusTD,
            player.n50PlusTD,
            player.n100to199,
            player.n200Plus,
            player.rect,
            player.fumTD,
            player.lost,
            player.fum,
            player.n2PT,
            player.made,
            player.miss,
            player.n0to19,
            player.n20to29,
            player.n30to39,
            player.n40to49,
            player.n50Plus,
            player.sack,
            player.fumRec,
            player.fumF,
            player.saf,
            player.block,
            player.ptsAllow,
            player.ptsAllowed,
            player.ydsAllow,
            player.n0to99Yds,
            player.n100to199Yds,
            player.n200to299Yds,
            player.n300to399Yds,
            player.n400to449Yds,
            player.n450to499Yds,
            player.n500PlusYds,
            player.tot,
            player.ast,
            player.sck,
            player.frcFum,
            player.intTD,
            player.blkTD,
            player.blk,
            player.pDef,
            player.intYds,
            player.fumYds,
            player.tFL,
            player.qBHit,
            player.sckYds,
            player.n10PlusTackles,
            player.n2PlusSacks,
            player.n3PlusPassesDefended,
            player.n50PlusYardINTReturnTD,
            player.n50PlusYardFumbleReturnTD,
            player.scores
        ]
        players_to_file.append(instance_list)
    return players_to_file


#Converts a whole list item to a string, take any term and returns a string. Included more for organization purposes.
# def convert_to_string(term):
#     term = str(term)
#     return term


#Iterates through each term in a list and converts to a string. Returns a list of string values.
def convert_list_to_string(target_list):
    for term in target_list:
        if not isinstance(term, str):
            target_list[target_list.index(term)] = str(term) + "\n"
        else:
            target_list[target_list.index(term)] = term + "\n"
    return target_list



def read_record_from_file():
    try:
        file = open(r"tests\offlineRecord.txt", "r")
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip("\n")
        file.close()
        return lines
    except FileNotFoundError:
        file = open(os.path.dirname(os.getcwd()) + "\\" + "tests" + "\\" + "offlineRecord.txt", "r")
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip("\n")
        file.close()
        return lines


def process_file_list():
    lines = read_record_from_file()
    metadata, leaguesettings = process_settings(lines)
    data = {
        'recordDate': lines[0],
        'metadata': metadata,
        'leaguesettings': leaguesettings
    }
    return data

def process_settings(lines):
    metadata = {
        'year_id': lines[1],
        'leagueId': lines[3],
        'seasonId': lines[4],
        'status': lines[12],
    }

    leaguesettings = {
        'finalMatchupPeriodId': int(lines[6]),
        'futureKeeperCount': int(lines[7]),
        'name': lines[8],
        'playoffSeedingTieRuleRawStatId': playoff_seed_tie_rule_reverser(lines[9]),
        'playoffTeamCount': int(lines[10]),
        'finalRegularSeasonMatchupPeriodId': int(lines[11]),
        'size': int(lines[13]),
        'tieRule': reverse_tie_rule(lines[14]),
        'tradeDeadline': lines[15],
        'usingUndroppableList': bool(lines[16]),
        'vetoVotesRequired': int(lines[17]),
        'id': int(lines[18]),
        'slotCategoryItems': get_roster_settings(lines)
    }
    return metadata, leaguesettings

def playoff_seed_tie_rule_reverser(indicator):
    playoff_tie_map = {
        'Head to Head Record': 1,
        'Total Points For': 0,
        'Intra Division Record': 1,
        'Total Points Against': 2
    }
    return playoff_tie_map[indicator]

def reverse_tie_rule(item):
    tie_map = {
        'None': 0,
        'Home Team Wins': 1,
        'Most Bench Points': 2,
        'Most QB Points': 3,
        'Most RB Points': 4
    }
    actual = tie_map[item]
    return actual

def get_roster_settings(lines):
    temp_index = lines.index('-- Slot Category Items --') + 1
    line = lines[temp_index]
    temp_slots = []
    while line != "-- New Team --":
        line_split = line.split(":")
        temp_dict = {
            'slotCategoryId': reverse_slot_items(line_split[0]),
            'num': int(line_split[1])
        }
        # temp_dict[line_split[0]] = line_split[1]
        temp_slots.append(temp_dict)
        temp_index = temp_index + 1
        line = lines[temp_index]
    return temp_slots

def reverse_slot_items(term):
    roster_map = {
        'QB': 0,
        'TQB': 1,
        'RB': 2,
        'RB/WR': 3,
        'WR': 4,
        'WR/TE': 5,
        'TE': 6,
        'OP': 7,
        'DT': 8,
        'DE': 9,
        'LB': 10,
        'DL': 11,
        'CB': 12,
        'S': 13,
        'DB': 14,
        'DP': 15,
        'D/ST': 16,
        'K': 17,
        'P': 18,
        'HC': 19,
        'BE': 20,
        'IR': 21,
        '': 22,
        'RB/WR/TE': 23,
        '': 24
    }
    return roster_map[term]


def archive_teams():
    file_list = read_record_from_file()
    teams = {}
    prime = file_list.index("-- New Team --")
    while prime != "End of Teams":
        team_builder = {
            'division': {
                'divisionId': file_list[prime + 1],
                'divisionName': file_list[prime + 2]
            },
            'owners': [
                {
                    'firstName': file_list[prime + 4].split(" ")[0],
                    'lastName': file_list[prime + 4].split(" ")[1]
                }
            ],
            'record': {
              "pointsAgainst": file_list[prime + 5],
              'pointsFor': file_list[prime + 6],
              'scores': file_list[prime + 7],
              'overallWins': file_list[prime + 10],
              'overallLosses': file_list[prime + 12]
            },
            'teamAbbrev': file_list[prime + 8],
            'teamName2': file_list[prime + 9],
            'teamId': file_list[prime + 11]
        }
        prime = prime + 13
        roster_start = prime
        file_list = file_list[prime:]
        try:
            prime = file_list.index("-- New Team --")
            team_builder['scores'] = process_scores(file_list[prime - 1])
            if prime > roster_start:
                roster = get_roster_from_file(file_list[roster_start: prime])
                team_builder['roster'] = roster
        except ValueError:
            prime = "End of Teams"
            team_builder['scores'] = process_scores(file_list[file_list.index("NFL Active Players") - 1])
        finally:
            teams[team_builder['teamId']] = team_builder
    return teams


def process_scores(scores_string):
    scores = []
    scores_string = scores_string.lstrip("[").rstrip("]").split(", ")
    for i in range(len(scores_string)):
        scores.append(float(scores_string[i]))
    return scores


def get_roster_from_file(team_abbrev):
    lines = read_record_from_file()
    temp_index = lines.index(team_abbrev)
    lines_subset = lines[temp_index:]
    try:
        end_index = lines_subset.index("-- New Team --") - 2
    except ValueError:
        end_index = lines_subset.index("NFL Active Players") - 2
    finally:
        team_lines = lines_subset[lines_subset.index("roster:") + 1:end_index]
        player_list = []
        for line in team_lines:
            line = line.lstrip("[").rstrip("]")
            line = line.split(", ")
            player_dict = {
                'player': {
                    'defaultPositionId': int(line[1]),
                    'draftRank': float(line[2]),
                    'firstName': line[3].rstrip("'").lstrip("'"),
                    'healthStatus': int(line[4]),
                    'isActive': bool(line[5]),
                    'droppable': bool(line[6]),
                    'isIREligible': bool(line[7]),
                    'jersey': line[10],
                    'lastName': line[11].rstrip("'").lstrip("'"),
                    'percentChange': line[12],
                    'percentOwned': line[13],
                    'percentStarted': line[14],
                    'playerRatingSeason': line[15],
                    'playerId': line[16],
                    'totalPoints': line[19]
                },
                'watchList': bool(line[8]),
                'isTradeLocked': bool(line[9]),
                'currentPeriodProjectedStats': {
                    'appliedStatTotal': line[17]
                },
                'pvoRank': line[18],
            }
            player_list.append(player_dict)
        return player_list


def reverse_position(position):
    positionAssignment = {
        "QB": 1,
        "RB": 1,
        "WR": 3,
        "TE": 4,
        "K": 5,
        "LB": 11,
        "EDR": 10,
        "CB": 12,
        "Safety": 13
    }
    return positionAssignment[position]

def get_leaders_from_file(new_record):
    record = read_record_from_file()
    startNum = record.index("Leaders:")
    record = record[startNum:]
    leaders = []
    for line in record:
        line = line.lstrip("[").rstrip("]")
        line = line.split(", ")
        line[0] = line[0].lstrip("'").rstrip("'")
        if line[0] == 'Offensive Leader:':
            leaders.append(OffensiveLeader(line, line[1], new_record))
        elif line[0] == 'Defensive Leader:':
            leaders.append(DefensiveLeader(line, line[1], new_record))
        elif line[0] == 'Kicker Leader:':
            leaders.append(KickerLeader(line, line[1], new_record))
    return leaders

def get_nflPlayers_from_file():
    players = []
    record = read_record_from_file()
    index = record.index("NFL Active Players")
    record = record[index + 1:]
    for entry in record:
        temp_dict = {}
        entry = entry.lstrip("[").rstrip("]")
        entry = entry.split("[")
        if len(entry) > 1:
            scores = entry[1]
            scores = scores.rstrip("]")
            scores = scores.split(",")
        else:
            scores = [0]
        entry = entry[0].rstrip(",")
        entry = entry.split(", ")
        temp = {
            'id': entry[0],
            'esbid': entry[1],
            'gsisPlayerId': entry[2],
            'name': entry[3],
            'position': entry[4],
            'teamAbbr': entry[5],
            "seasonPts": entry[6],
            'seasonProjectedPts': entry[7],
            'weekPts': entry[8],
            'weekProjectedPts': entry[9],
            'GP': entry[10],
            'Att': entry[11],
            'Comp': entry[12],
            'Inc': entry[13],
            'Yds': entry[14],
            'TD': entry[15],
            'Int': entry[16],
            'Sacked': entry[17],
            "300-399": entry[18],
            '400+': entry[19],
            '40+ TD': entry[20],
            '50+ TD': entry[21],
            '100-199': entry[22],
            '200+': entry[23],
            'Rect': entry[24],
            'Fum TD': entry[25],
            'Lost': entry[26],
            'Fum': entry[27],
            '2PT': entry[28],
            'Made': entry[29],
            'Miss': entry[30],
            '0-19': entry[31],
            '20-29': entry[32],
            '30-39': entry[33],
            '40-49': entry[34],
            '50+': entry[35],
            'Sack': entry[36],
            "Fum Rec": entry[37],
            'Fum F': entry[38],
            'Saf': entry[39],
            'Block': entry[40],
            'Pts Allow': entry[41],
            'Pts Allowed': entry[42],
            'Yds Allow': entry[43],
            '0-99 Yds': entry[44],
            '100-199 Yds': entry[45],
            '200-299 Yds': entry[46],
            '300-399 Yds': entry[47],
            '400-449 Yds': entry[48],
            '450-499 Yds': entry[49],
            '500+ Yds': entry[50],
            'Tot': entry[51],
            'Ast': entry[52],
            'Sck': entry[53],
            'Frc Fum': entry[54],
            'Int TD': entry[55],
            'Blk TD': entry[56],
            'Blk': entry[57],
            'PDef': entry[58],
            'Int Yds': entry[59],
            'Fum Yds': entry[60],
            'TFL': entry[61],
            'QB Hit': entry[62],
            'Sck Yds': entry[63],
            '10+ Tackles': entry[64],
            '2+ Sacks': entry[65],
            '3+ Passes Defended': entry[66],
            '50+ Yard INT Return TD': entry[67],
            '50+ Yard Fumble Return TD': entry[68],
            'weekScores': scores
        }
        for entry2 in temp:
            if isinstance(temp[entry2], str):
                temp[entry2] = temp[entry2].replace("'", "")
        players.append(temp)
    return players

