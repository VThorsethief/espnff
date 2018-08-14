class Player(object):
    def __init__(self, player):
        self.pvoRank = self.__setStat(player,'pvoRank')
        self.isDroppable = player['player']['droppable']
        self.percentStarted = player['player']['percentStarted']
        self.jerseryNum = self.__setStat(player['player'],'jersey')
        self.playerRatingSeason = self.__setStat(player['player'],'playerRatingSeason')
        self.isIREligible = player['player']['isIREligible']
        self.draftRank = player['player']['draftRank']
        self.firstName = player['player']['firstName']
        self.lastName = player['player']['lastName']
        self.healthStatus = player['player']['healthStatus']
        self.percentOwned = player['player']['percentOwned']
        self.proTeam_id = player['player']['proTeamId']
        self.isActive = player['player']['isActive']
        self.player_id = player['player']['playerId']
        self.percentChange = player['player']['percentChange']
        self.defaultPositionId = player['player']['defaultPositionId']
        self.__position = self.__setPosition()
        self.totalPoints = self.__setStat(player['player'],'totalPoints')
        self.isOnWatchList = player['watchList']
        self.isTradeLocked = player['isTradeLocked']
        self.projectedPoints = self.__setStat(player['currentPeriodProjectedStats'],'appliedStatTotal')

    def __repr__(self):
        return self.firstName + " " + self.lastName

    def __setStat(self, dict, key):
        if dict.get(key, 0) == 0:
            return None
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
