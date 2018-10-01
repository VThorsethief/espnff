class Leader(object):
    def __init__(self, stats, pos, newRecord):
        if newRecord:
            self.name = stats[0].contents[0].text
        else:
            self.name = stats[2]
        self.__position = pos

    def __repr__(self):
        return self.name

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    def assignStat(self, value):
        if value == "--":
            return None
        else:
            return float(value)

    def return_player_array(self):
        return[]

class NonDefensive(Leader):
    def __init__(self, stats, pos, newRecord):
        super().__init__(stats, pos, newRecord)
        if newRecord:
            self.team = stats[0].contents[1].split(" ")[1].split(" ")[0][:3]
        else:
            self.team = stats[15]

class OffensiveLeader(NonDefensive):
    def __init__(self, stats, pos, newRecord):
        super().__init__(stats, pos, newRecord)
        if newRecord:
            self.passCompletions = self.assignStat(stats[5].text.split("/")[0])
            print(self.name)
            try:
                self.passAttempts = self.assignStat(stats[5].text.split("/")[1])
            except IndexError:
                print(stats[5].text)

            self.passingYards = self.assignStat(stats[6].text)
            self.passingTD = self.assignStat(stats[8].text)
            self.rushingAttempts = self.assignStat(stats[10].text)
            self.rushingYards = self.assignStat(stats[11].text)
            self.rushingTD = self.assignStat(stats[12].text)
            self.receptions = self.assignStat(stats[14].text)
            self.recYards = self.assignStat(stats[15].text)
            self.receivingTD = self.assignStat(stats[16].text)
            self.totalPoints = self.assignStat(stats[23].text)
        else:
            self.passAttempts = float(stats[3])
            self.passCompletions = float(stats[4])
            self.passingTD = float(stats[5])
            self.passingYards = float(stats[6])
            self.recYards = float(stats[8])
            self.receivingTD = float(stats[9])
            self.receptions = float(stats[10])
            self.rushingAttempts = float(stats[11])
            self.rushingTD = float(stats[12])
            self.rushingYards = float(stats[13])
            self.team = stats[14]
            self.totalPoints = float(stats[15])

    def return_player_array(self):
        return [self.name, self.team, self.position, self.passCompletions, self.passAttempts]


class KickerLeader(NonDefensive):
    def __init__(self, stats, pos, newRecord):
        super().__init__(stats, pos, newRecord)
        if newRecord:
            self.sub40YardCompletions = self.assignStat(stats[2].text.split("/")[0])
            self.sub40YardAttempts = self.assignStat(stats[2].text.split("/")[1])
            self.fortySubFiftyCompletions = self.assignStat(stats[3].text.split("/")[0])
            self.fortySubFiftyAttempts = self.assignStat(stats[3].text.split("/")[1])
            self.fiftyPlusCompletions = self.assignStat(stats[4].text.split("/")[0])
            self.fiftyPlusAttempts = self.assignStat(stats[4].text.split("/")[1])
            self.totalCompletions = self.assignStat(stats[5].text.split("/")[0])
            self.totalAttempts = self.assignStat(stats[5].text.split("/")[1])
            self.xpCompletions = self.assignStat(stats[6].text.split("/")[0])
            self.xpAttempts = self.assignStat(stats[6].text.split("/")[1])
            self.totalPoints = self.assignStat(stats[8].text)
        else:
            self.fiftyPlusAttempts = self.assignStat(stats[3])
            self.fiftyPlusCompletions = self.assignStat(stats[4])
            self.fortySubFiftyAttempts = self.assignStat(stats[5])
            self.fortySubFiftyCompletions = self.assignStat(stats[6])
            self.sub40YardAttempts = self.assignStat(stats[8])
            self.sub40YardCompletions = self.assignStat(stats[9])
            self.team = stats[10]
            self.totalAttempts = self.assignStat(stats[11])
            self.totalCompletions = self.assignStat(stats[12])
            self.totalPoints = self.assignStat(stats[13])
            self.xpAttempts = self.assignStat(stats[14])
            self.xpCompletions = self.assignStat(stats[15])

    def assignStat(self, value):
        if value == 'None' or value == "--":
            return None
        else:
            return float(value)

class DefensiveLeader(Leader):
    def __init__(self, stats, pos, newRecord):
        super().__init__(stats, pos, newRecord)
        if newRecord:
            self.team = self.name.split(" ")[0]
            self.returnTD = self.assignStat(stats[2].text)
            self.intercept = self.assignStat(stats[3].text)
            self.fumbleRecoveries = self.assignStat(stats[4].text)
            self.sacks = self.assignStat(stats[5].text)
            self.safeties = self.assignStat(stats[6].text)
            self.blockedKick = self.assignStat(stats[7].text)
            self.pointsAllowed = self.assignStat(stats[8].text)
            self.totalPoints = self.assignStat(stats[10].text)
        else:
            self.blockedKick = self.assignStat(float(stats[3]))
            self.fumbleRecoveries = self.assignStat(float(stats[4]))
            self.intercept = self.assignStat(float(stats[5]))
            self.pointsAllowed = self.assignStat(float(stats[6]))
            self.returnTD = self.assignStat(float(stats[8]))
            self.sacks = self.assignStat(float(stats[9]))
            self.safeties = self.assignStat(float(stats[10]))
            self.totalPoints = self.assignStat(float(stats[11]))