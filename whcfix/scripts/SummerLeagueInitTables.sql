CREATE TABLE venues (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(250), 
	PRIMARY KEY (id)
);

CREATE TABLE tournaments (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(250), 
	PRIMARY KEY (id)
);


CREATE TABLE divisions (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(250), 
	tournament_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(tournament_id) REFERENCES tournaments (id)
);

CREATE TABLE teams (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(250), 
	division_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(division_id) REFERENCES divisions (id)
);


CREATE TABLE fixtures (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	push_back DATETIME, 
	home_team_id INTEGER, 
	away_team_id INTEGER, 
	venue_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(home_team_id) REFERENCES teams (id), 
	FOREIGN KEY(away_team_id) REFERENCES teams (id), 
	FOREIGN KEY(venue_id) REFERENCES venues (id)
);


CREATE TABLE results (
	fixture_id INTEGER NOT NULL, 
	home_goals INTEGER, 
	away_goals INTEGER, 
	PRIMARY KEY (fixture_id), 
	FOREIGN KEY(fixture_id) REFERENCES fixtures (id)
);
