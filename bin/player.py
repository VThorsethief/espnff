class Player(object):
    def __init__(self, player):
        self.pvoRank = float(self.__setStat(player,'pvoRank'))
        self.isDroppable = bool(player['player']['droppable'])
        self.percentStarted = float(player['player']['percentStarted'])
        self.jerseryNum = float(self.__setStat(player['player'],'jersey'))
        self.playerRatingSeason = float(self.__setStat(player['player'],'playerRatingSeason'))
        self.isIREligible = bool(player['player']['isIREligible'])
        self.draftRank = float(player['player']['draftRank'])
        self.firstName = player['player']['firstName']
        self.lastName = player['player']['lastName']
        self.healthStatus = int(player['player']['healthStatus'])
        self.percentOwned = float(player['player']['percentOwned'])
        try:
            self.proTeam_id = player['player']['proTeamId']
        except KeyError:
            self.proTeam_id = "Not Available From File"
        self.isActive = bool(player['player']['isActive'])
        self.player_id = int(player['player']['playerId'])
        self.percentChange = float(player['player']['percentChange'])
        self.defaultPositionId = int(player['player']['defaultPositionId'])
        self.__position = self.__setPosition()
        self.totalPoints = float(self.__setStat(player['player'],'totalPoints'))
        self.isOnWatchList = bool(player['watchList'])
        self.isTradeLocked = bool(player['isTradeLocked'])
        self.projectedPoints = float(self.__setStat(player['currentPeriodProjectedStats'],'appliedStatTotal'))
        self.scores = []
        self.NFLreference = None


    def __repr__(self):
        return self.firstName + " " + self.lastName

    def __setStat(self, dict, key):
        if dict.get(key, 0) == 0:
            return 0
        else:
            return dict[key]

    def __setPosition(self):
        positionAssignment = {
            1: "QB",
            2: "RB",
            3: "WR",
            4: "TE",
            5: "K",
            11: "LB",
            10: "EDR",
            12: "CB",
            13: "Safety",

        }
        return positionAssignment.get(self.defaultPositionId, self.defaultPositionId)

    def getPosition(self):
        return self.__position

    def return_player_array(self):
        return ["Team Player", self.getPosition(), self.jerseryNum, self.pvoRank, self.isDroppable, self.percentStarted,
                self.playerRatingSeason, self.isIREligible, self.draftRank, self.firstName, self.lastName,
                self.healthStatus, self.percentOwned, self.isActive, self.player_id, self.percentChange, self.defaultPositionId,
                self.totalPoints, self.isOnWatchList, self.isTradeLocked, self.projectedPoints]

    def set_scores(self, nfl_scores):
        self.scores = []
        if nfl_scores == 0:
            self.scores.append(0)
        elif len(nfl_scores) > 1:
            for entry in nfl_scores:
                self.scores.append(entry)
        else:
            self.scores.append(nfl_scores[0])
        self.scores.append(self.projectedPoints)

    def set_nfl_reference(self, nflPlayer):
        self.NFLreference = nflPlayer



