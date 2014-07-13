

class DivisionRow(object):

    def __init__(self, pos, team, is_promotion, is_relegation, played, won, 
                 drawn, lost, goals_for, goals_against, goals_difference, 
                 points, max_points):
        self.pos = pos
        self.team = team
        self.is_promotion = is_promotion
        self.is_relegation = is_relegation
        self.played = played
        self.won = won
        self.drawn = drawn
        self.lost = lost
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.goals_difference = goals_difference
        self.points = points
        self.max_points = max_points

class Division(object):

    def __init__(self, name, table_rows):
        self.name = name
        self.table_rows = table_rows
        
