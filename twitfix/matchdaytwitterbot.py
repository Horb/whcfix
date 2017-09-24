import tweepy
import random
from datetime import datetime, timedelta

from twitfix.credentials import *
from whcfix.logic.matches import Matches


def get_pitch_from_note(note):
    if "Blue Pitch." in note:
        return " on the Blue Pitch"
    if "Green Pitch." in note:
        return " on the Green Pitch"
    return ""

def get_opener():
    return random.choice([
        "Next Up",
        "Coming Up",
        "On Next",
        "Starting Soon",
        "Next Match",
        "Warming Up",
        "Next On"
        ])

def get_tweets(the_datetime, interval_minutes):
    interval_in_seconds = interval_minutes * 60

    for current_match in Matches().listOfMatches:
        if 'Wakefield' in current_match.home:
            if current_match._time is None:
                continue

            if current_match.isPostponed:
                continue

            full_date = datetime(
                                current_match._date.year,
                                current_match._date.month,
                                current_match._date.day,
                                current_match._time.hour,
                                current_match._time.minute,
                                current_match._time.second
                                )

            td = full_date - the_datetime

            if 0 < td.total_seconds() <= interval_in_seconds:
                pitch = get_pitch_from_note(current_match.note)
                opener = get_opener()
                template = "%s: %s vs %s%s, %s push back #GreenArmy"
                tweet = template % (
                        opener,
                        current_match.home,
                        current_match.away,
                        pitch,
                        current_match.time)
                yield tweet


def send_tweets(tweets):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    for tweet in tweets:
        if 0 < len(tweet) <= 140:
            api.update_status(status=tweet)

def print_tweets(tweets):
    for tweet in tweets:
        print(tweet)

if __name__ == '__main__':
    d = datetime.now()
    d = d + timedelta(hours=5)
    send_tweets(get_tweets(d, 29))
