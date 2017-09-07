
from whcfix.logic.matches import Matches
from datetime import datetime


def dump():
    for m in Matches().listOfMatches:
        print(m.date, m.time, m.home, m.away)

def get_tweets(the_datetime, interval_minutes):
    interval_in_seconds = interval_minutes * 60
    for m in Matches().listOfMatches:
        if m._time is None:
            continue

        fulldate = datetime(
                m._date.year,
                m._date.month,
                m._date.day,
                m._time.hour,
                m._time.minute,
                m._time.second)

        td = fulldate - the_datetime

        if 0 <= td.total_seconds() <= interval_in_seconds:
            yield "%s vs %s at %s, %s push back!" 
                    % (m.home, m.away, m.venue, m.time)


if __name__ == '__main__':
    tweeter(datetime(2017, 12, 9, 12, 0, 0), 30)
