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
