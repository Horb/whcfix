from datetime import datetime

import tweepy

from twitfix.credentials import *
from whcfix.logic.matches import Matches


def get_tweets(the_datetime, interval_minutes):
    interval_in_seconds = interval_minutes * 60

    for current_match in Matches().listOfMatches:
        if 'Wakefield' in current_match.home:
            if current_match._time is None:
                continue

            full_date = datetime(
                                current_match._date.year,
                                current_match._date.month,
                                current_match._date.day,
                                current_match._time.hour,
                                current_match._time.minute,
                                current_match._time.second)

            td = full_date - the_datetime

            if 0 < td.total_seconds() <= interval_in_seconds:
                if current_match.note == "":
                    current_tweets.append("Next Up: %s vs. %s, %s push back #MatchDayBot"
                        % (current_match.home, current_match.away, current_match.time))
                else:
                    current_tweets.append("Next Up: %s vs. %s on the %s %s push back #MatchDayBot"
                        % (current_match.home, current_match.away, current_match.note.lower(), current_match.time))


def send_tweets(collected_tweets):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    for tweet in collected_tweets:
        if 0 < len(tweet) <= 140:
            api.update_status(status=tweet)


if __name__ == '__main__':
    current_tweets = []
    get_tweets(datetime.now(), 30)
    send_tweets(current_tweets)
