class Team:
    def __init__(self, id, abbrev, name):
        self.id = id
        self.abbrev = abbrev
        self.name = name


class TeamScore(Team):
    def __init__(self, id, abbrev, name, goals=0, sog=0, powerplay=False, num_skaters=0, pulled_goalie=False, goal_plays = []):
        super().__init__(id, abbrev, name)
        self.goals = goals
        self.goal_plays = goal_plays
        self.shot_on_goal = sog
        self.powerplay = powerplay
        self.num_skaters = num_skaters
        self.pulled_goalie = pulled_goalie


class SeriesTeam(Team):
    def __init__(self, matchupTeam, abbrev):
        super().__init__(matchupTeam.team.id, abbrev, matchupTeam.team.name)
        self.isTop = matchupTeam.seed.isTop
        self.rank = matchupTeam.seed.rank
        self.series_wins = matchupTeam.seriesRecord.wins
        self.series_losses = matchupTeam.seriesRecord.losses