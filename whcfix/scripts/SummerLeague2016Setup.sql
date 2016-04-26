INSERT INTO tournaments 
    (name) 
VALUES 
    ('Summer League 2016');

INSERT INTO divisions 
    (name, tournament_id) 
VALUES 
    ('Division 1', 1),
    ('Division 2', 1),
    ('Division 3', 1),
    ('Division 4', 1);

INSERT INTO teams
    (name, division_id)
VALUES
    ('Wakefield 1', 1),
    ('Bradford', 1),
    ('Slazengers 1', 1),
    ('York 3', 1),

    ('Wakefield 3/4', 2),
    ('Sneaky Reapers A', 2),
    ('Acomb', 2),
    ('York 4', 2),

    ('Wakefield 4/5', 3),
    ('Team Minibus', 3),
    ('Sneaky Reapers B', 3),
    ('Barnsley', 3),

    ('Slazengers 3', 4),
    ('Wakefield 6', 4),
    ('Team Spartan', 4),
    ('Team Centurian', 4);

INSERT INTO venues
    (name) 
VALUES 
    ('Green 1'),
    ('Green 2'),
    ('Blue 1'),
    ('Blue 2');

INSERT INTO fixtures
    (push_back, home_team_id, away_team_id, venue_id)
VALUES
    ('2016-04-28T19:00:00', 11    ,  9, 3),
    ('2016-04-28T19:00:00', 2    ,  1, 4),
    ('2016-04-28T20:00:00', 4  ,  3, 3),
    ('2016-04-28T20:00:00', 14 ,  15, 4),
    ('2016-04-28T21:00:00', 7   ,  8, 3),
    ('2016-04-28T21:00:00', 13    ,  16, 4),
    ('2016-04-28T21:00:00', 6    ,  5, 1),
    ('2016-04-28T21:00:00', 10    ,  12, 2),
    ('2016-05-12T19:00:00', 11    ,  10, 3),
    ('2016-05-12T19:00:00', 16  ,  14, 4),
    ('2016-05-12T20:00:00', 5   ,  8, 3),
    ('2016-05-12T20:00:00', 7   ,  6 , 4),
    ('2016-05-12T21:00:00', 4  ,  2, 3),
    ('2016-05-12T21:00:00', 3    ,  1, 4),
    ('2016-05-12T21:00:00', 9   ,  12, 1),
    ('2016-05-12T21:00:00', 15    ,  13, 2),
    ('2016-05-26T19:00:00', 12    ,  11, 3),
    ('2016-05-26T19:00:00', 16  ,  15, 4),
    ('2016-05-26T20:00:00', 13    ,  14, 3),
    ('2016-05-26T20:00:00', 6    ,  8, 4),
    ('2016-05-26T21:00:00', 5   ,  7, 3),
    ('2016-05-26T21:00:00', 3    ,  2, 4),
    ('2016-05-26T21:00:00', 10    ,  9, 1),
    ('2016-05-26T21:00:00', 4  ,  1, 2)
