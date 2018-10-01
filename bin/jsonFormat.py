

def generate_dict():
  reponse_format = {
    "stats": [
      {
        "id": 1,
        "abbr": "GP",
        "name": "Games Played",
        "shortName": "GP"
      },
      {
        "id": 2,
        "abbr": "Att",
        "name": "Passing Attempts",
        "shortName": "Pass Att"
      },
      {
        "id": 3,
        "abbr": "Comp",
        "name": "Passing Completions",
        "shortName": "Pass Comp"
      },
      {
        "id": 4,
        "abbr": "Inc",
        "name": "Incomplete Passes",
        "shortName": "Pass Inc"
      },
      {
        "id": 5,
        "abbr": "Yds",
        "name": "Passing Yards",
        "shortName": "Pass Yds"
      },
      {
        "id": 6,
        "abbr": "TD",
        "name": "Passing Touchdowns",
        "shortName": "Pass TD"
      },
      {
        "id": 7,
        "abbr": "Int",
        "name": "Interceptions Thrown",
        "shortName": "Pass Int"
      },
      {
        "id": 8,
        "abbr": "Sacked",
        "name": "Every Time Sacked",
        "shortName": "Sacked"
      },
      {
        "id": 9,
        "abbr": "300-399",
        "name": "300-399 Passing Yards Bonus",
        "shortName": "300-399 Pass Yds"
      },
      {
        "id": 10,
        "abbr": "400+",
        "name": "400+ Passing Yards Bonus",
        "shortName": "400+ Pass Yds"
      },
      {
        "id": 11,
        "abbr": "40+ TD",
        "name": "40+ Passing Yard TD Bonus",
        "shortName": "40+ Pass TD"
      },
      {
        "id": 12,
        "abbr": "50+ TD",
        "name": "50+ Passing Yards TD Bonus",
        "shortName": "50+ Pass TD"
      },
      {
        "id": 13,
        "abbr": "Att",
        "name": "Rushing Attempts",
        "shortName": "Rush Att"
      },
      {
        "id": 14,
        "abbr": "Yds",
        "name": "Rushing Yards",
        "shortName": "Rush Yds"
      },
      {
        "id": 15,
        "abbr": "TD",
        "name": "Rushing Touchdowns",
        "shortName": "Rush TD"
      },
      {
        "id": 16,
        "abbr": "40+ TD",
        "name": "40+ Rushing Yard TD Bonus",
        "shortName": "40+ Rush TD"
      },
      {
        "id": 17,
        "abbr": "50+ TD",
        "name": "50+ Rushing Yard TD Bonus",
        "shortName": "50+ Rush TD"
      },
      {
        "id": 18,
        "abbr": "100-199",
        "name": "100-199 Rushing Yards Bonus",
        "shortName": "100-199 Rush Yds"
      },
      {
        "id": 19,
        "abbr": "200+",
        "name": "200+ Rushing Yards Bonus",
        "shortName": "200+ Rush Yds"
      },
      {
        "id": 20,
        "abbr": "Rect",
        "name": "Receptions",
        "shortName": "Receptions"
      },
      {
        "id": 21,
        "abbr": "Yds",
        "name": "Receiving Yards",
        "shortName": "Rec Yds"
      },
      {
        "id": 22,
        "abbr": "TD",
        "name": "Receiving Touchdowns",
        "shortName": "Rec TD"
      },
      {
        "id": 23,
        "abbr": "40+ TD",
        "name": "40+ Receiving Yard TD Bonus",
        "shortName": "40+ Rec TD"
      },
      {
        "id": 24,
        "abbr": "50+ TD",
        "name": "50+ Receiving Yard TD Bonus",
        "shortName": "50+ Rec TD"
      },
      {
        "id": 25,
        "abbr": "100-199",
        "name": "100-199 Receiving Yards Bonus",
        "shortName": "100-199 Rec Yds"
      },
      {
        "id": 26,
        "abbr": "200+",
        "name": "200+ Receiving Yards Bonus",
        "shortName": "200+ Rec Yds"
      },
      {
        "id": 27,
        "abbr": "Yds",
        "name": "Kickoff and Punt Return Yards",
        "shortName": "Return Yds"
      },
      {
        "id": 28,
        "abbr": "TD",
        "name": "Kickoff and Punt Return Touchdowns",
        "shortName": "Return TD"
      },
      {
        "id": 29,
        "abbr": "Fum TD",
        "name": "Fumble Recovered for TD",
        "shortName": "Fum TD"
      },
      {
        "id": 30,
        "abbr": "Lost",
        "name": "Fumbles Lost",
        "shortName": "Fum Lost"
      },
      {
        "id": 31,
        "abbr": "Fum",
        "name": "Fumble",
        "shortName": "Fum"
      },
      {
        "id": 32,
        "abbr": "2PT",
        "name": "2-Point Conversions",
        "shortName": "2PT"
      },
      {
        "id": 33,
        "abbr": "Made",
        "name": "PAT Made",
        "shortName": "PAT Made"
      },
      {
        "id": 34,
        "abbr": "Miss",
        "name": "PAT Missed",
        "shortName": "PAT Miss"
      },
      {
        "id": 35,
        "abbr": "0-19",
        "name": "FG Made 0-19",
        "shortName": "FG 0-19"
      },
      {
        "id": 36,
        "abbr": "20-29",
        "name": "FG Made 20-29",
        "shortName": "FG 20-29"
      },
      {
        "id": 37,
        "abbr": "30-39",
        "name": "FG Made 30-39",
        "shortName": "FG 30-39"
      },
      {
        "id": 38,
        "abbr": "40-49",
        "name": "FG Made 40-49",
        "shortName": "FG 40-49"
      },
      {
        "id": 39,
        "abbr": "50+",
        "name": "FG Made 50+",
        "shortName": "FG 50+"
      },
      {
        "id": 40,
        "abbr": "0-19",
        "name": "FG Missed 0-19",
        "shortName": "FG Miss 0-19"
      },
      {
        "id": 41,
        "abbr": "20-29",
        "name": "FG Missed 20-29",
        "shortName": "FG Miss 20-29"
      },
      {
        "id": 42,
        "abbr": "30-39",
        "name": "FG Missed 30-39",
        "shortName": "FG Miss 30-39"
      },
      {
        "id": 43,
        "abbr": "40-49",
        "name": "FG Missed 40-49",
        "shortName": "FG Miss 40-49"
      },
      {
        "id": 44,
        "abbr": "50+",
        "name": "FG Missed 50+",
        "shortName": "FG Miss 50+"
      },
      {
        "id": 45,
        "abbr": "Sack",
        "name": "Sacks",
        "shortName": "Sack"
      },
      {
        "id": 46,
        "abbr": "Int",
        "name": "Interceptions",
        "shortName": "Int"
      },
      {
        "id": 47,
        "abbr": "Fum Rec",
        "name": "Fumbles Recovered",
        "shortName": "Fum Rec"
      },
      {
        "id": 48,
        "abbr": "Fum F",
        "name": "Fumbles Forced",
        "shortName": "Fum Forc"
      },
      {
        "id": 49,
        "abbr": "Saf",
        "name": "Safeties",
        "shortName": "Saf"
      },
      {
        "id": 50,
        "abbr": "TD",
        "name": "Touchdowns",
        "shortName": "TD"
      },
      {
        "id": 51,
        "abbr": "Block",
        "name": "Blocked Kicks",
        "shortName": "Block"
      },
      {
        "id": 52,
        "abbr": "Yds",
        "name": "Kickoff and Punt Return Yards",
        "shortName": "Return Yds"
      },
      {
        "id": 53,
        "abbr": "TD",
        "name": "Kickoff and Punt Return Touchdowns",
        "shortName": "Return TD"
      },
      {
        "id": 54,
        "abbr": "Pts Allow",
        "name": "Points Allowed",
        "shortName": "Pts Allow"
      },
      {
        "id": 55,
        "abbr": "Pts Allow",
        "name": "Points Allowed 0",
        "shortName": "Pts Allow 0"
      },
      {
        "id": 56,
        "abbr": "Pts Allow",
        "name": "Points Allowed 1-6",
        "shortName": "Pts Allow 1-6"
      },
      {
        "id": 57,
        "abbr": "Pts Allow",
        "name": "Points Allowed 7-13",
        "shortName": "Pts Allow 7-13"
      },
      {
        "id": 58,
        "abbr": "Pts Allow",
        "name": "Points Allowed 14-20",
        "shortName": "Pts Allow 14-20"
      },
      {
        "id": 59,
        "abbr": "Pts Allow",
        "name": "Points Allowed 21-27",
        "shortName": "Pts Allow 21-27"
      },
      {
        "id": 60,
        "abbr": "Pts Allow",
        "name": "Points Allowed 28-34",
        "shortName": "Pts Allow 28-34"
      },
      {
        "id": 61,
        "abbr": "Pts Allowed",
        "name": "Points Allowed 35+",
        "shortName": "Pts Allowed 35+"
      },
      {
        "id": 62,
        "abbr": "Yds Allow",
        "name": "Yards Allowed",
        "shortName": "Yds Allow"
      },
      {
        "id": 63,
        "abbr": "0-99 Yds",
        "name": "Less than 100 Total Yards Allowed",
        "shortName": "Less 100 Yds Allowed"
      },
      {
        "id": 64,
        "abbr": "100-199 Yds",
        "name": "100-199 Yards Allowed",
        "shortName": "100-199 Yds Allow"
      },
      {
        "id": 65,
        "abbr": "200-299 Yds",
        "name": "200-299 Yards Allowed",
        "shortName": "200-299 Yds Allow"
      },
      {
        "id": 66,
        "abbr": "300-399 Yds",
        "name": "300-399 Yards Allowed",
        "shortName": "300-399 Yds Allow"
      },
      {
        "id": 67,
        "abbr": "400-449 Yds",
        "name": "400-449 Yards Allowed",
        "shortName": "400-449 Yds Allow"
      },
      {
        "id": 68,
        "abbr": "450-499 Yds",
        "name": "450-499 Yards Allowed",
        "shortName": "450-499 Yds Allow"
      },
      {
        "id": 69,
        "abbr": "500+ Yds",
        "name": "500+ Yards Allowed",
        "shortName": "500+ Yds Allow"
      },
      {
        "id": 70,
        "abbr": "Tot",
        "name": "Tackle",
        "shortName": "Tack"
      },
      {
        "id": 71,
        "abbr": "Ast",
        "name": "Assisted Tackles",
        "shortName": "Ast"
      },
      {
        "id": 72,
        "abbr": "Sck",
        "name": "Sack",
        "shortName": "Sack"
      },
      {
        "id": 73,
        "abbr": "Int",
        "name": "Defense Interception",
        "shortName": "Int"
      },
      {
        "id": 74,
        "abbr": "Frc Fum",
        "name": "Forced Fumble",
        "shortName": "Frc Fum"
      },
      {
        "id": 75,
        "abbr": "Fum Rec",
        "name": "Fumbles Recovery",
        "shortName": "Fum Rec"
      },
      {
        "id": 76,
        "abbr": "Int TD",
        "name": "Touchdown (Interception return)",
        "shortName": "Int TD"
      },
      {
        "id": 77,
        "abbr": "Fum TD",
        "name": "Touchdown (Fumble return)",
        "shortName": "Fum TD"
      },
      {
        "id": 78,
        "abbr": "Blk TD",
        "name": "Touchdown (Blocked kick)",
        "shortName": "Blk TD"
      },
      {
        "id": 79,
        "abbr": "Blk",
        "name": "Blocked Kick (punt, FG, PAT)",
        "shortName": "Blk"
      },
      {
        "id": 80,
        "abbr": "Saf",
        "name": "Safety",
        "shortName": "Saf"
      },
      {
        "id": 81,
        "abbr": "PDef",
        "name": "Pass Defended",
        "shortName": "Pass Def"
      },
      {
        "id": 82,
        "abbr": "Int Yds",
        "name": "Interception Return Yards",
        "shortName": "Int Yds"
      },
      {
        "id": 83,
        "abbr": "Fum Yds",
        "name": "Fumble Return Yards",
        "shortName": "Fum Yds"
      },
      {
        "id": 84,
        "abbr": "TFL",
        "name": "Tackles for Loss Bonus",
        "shortName": "TFL"
      },
      {
        "id": 85,
        "abbr": "QB Hit",
        "name": "QB Hit",
        "shortName": "QB Hit"
      },
      {
        "id": 86,
        "abbr": "Sck Yds",
        "name": "Sack Yards",
        "shortName": "Sck Yds"
      },
      {
        "id": 87,
        "abbr": "10+ Tackles",
        "name": "10+ Tackles Bonus",
        "shortName": "10+ Tack"
      },
      {
        "id": 88,
        "abbr": "2+ Sacks",
        "name": "2+ Sacks Bonus",
        "shortName": "2+ Sck"
      },
      {
        "id": 89,
        "abbr": "3+ Passes Defended",
        "name": "3+ Passes Defended Bonus",
        "shortName": "3+ Pas Def"
      },
      {
        "id": 90,
        "abbr": "50+ Yard INT Return TD",
        "name": "50+ Yard INT Return TD Bonus",
        "shortName": "50+ Yard INT TD"
      },
      {
        "id": 91,
        "abbr": "50+ Yard Fumble Return TD",
        "name": "50+ Yard Fumble Return TD Bonus",
        "shortName": "50+ Yard Fum Ret TD"
      }
    ]
  }
  new_dict = {}
  for entry in reponse_format["stats"]:
    new_dict[entry["id"]] = entry
  return new_dict