import csv
from datetime import datetime
from whcfix.data.database import get_db
from whcfix.data.models import Tournament, Division, Team, Fixture

with get_db() as db:
    teams = db.query(Team).all()
    with open('whcfix/summerleaguefixtures1.csv', 'r') as csvf:
        reader = csv.reader(csvf)
        for x, line in enumerate(reader):
            y, m, d, h, n, s, venue, home, away = line
            y, m, d, h, n, s = map(int, (y, m, d, h, n, s))
            push_back = datetime(y, m, d, h, n, s)
            home_team_id = filter(lambda t: t.name.strip() == home.strip(), teams)[0].id
            division_id = filter(lambda t: t.name.strip() == home.strip(), teams)[0].division.id
            away_team_id = filter(lambda t: t.name.strip() == away.strip(), teams)[0].id
            fixture = Fixture(home_team_id=home_team_id,
                              away_team_id=away_team_id,
                              division_id=division_id,
                              push_back=push_back)
            db.add(fixture)
    db.commit()
