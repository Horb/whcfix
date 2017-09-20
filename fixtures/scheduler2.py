from collections import namedtuple
import csv
import sys
import logging
from itertools import groupby
from re import match

Fixture = namedtuple('Fixture', ['date', 'home', 'away'])
DateSlot = namedtuple('DateSlot', ['date', 'time', 'pitch'])
Slot = namedtuple('Slot', ['time', 'pitch'])
FixtureDateSlot = namedtuple(
        'FixtureDateSlot', ["date", "time", "pitch", "home", "away"])

fixtures = []

with open('1718_Fixtures.csv', 'rb') as csvf:
    lines = csv.reader(csvf)
    for line in lines:
        date, home, away = line
        fixtures.append(Fixture(date, home, away))

date_slots = []


with open('1718_DateSlots.csv', 'rb') as csvf:
    lines = csv.reader(csvf)
    for line in lines:
        date, time, pitch = line
        date_slots.append(DateSlot(date, time, pitch))

def get_preferences(f, match_day):
    A = [
            Slot('15:00:00', 'Green'),
            Slot('13:30:00', 'Blue'),
            Slot('12:00:00', 'Green'),
            Slot('15:00:00', 'Blue'),
            Slot('13:30:00', 'Green'),
            Slot('12:00:00', 'Blue'),

            Slot('16:30:00', 'Blue'),
            Slot('16:30:00', 'Green'),
            Slot('10:00:00', 'Blue'),
            Slot('10:30:00', 'Green'),
            ]
    B = [
            Slot('15:00:00', 'Blue'),
            Slot('13:30:00', 'Green'),
            Slot('12:00:00', 'Blue'),
            Slot('15:00:00', 'Green'),
            Slot('13:30:00', 'Blue'),
            Slot('12:00:00', 'Green'),

            Slot('16:30:00', 'Green'),
            Slot('16:30:00', 'Blue'),
            Slot('10:00:00', 'Green'),
            Slot('10:30:00', 'Blue'),
            ]
    isMale = "Mens" in f.home
    isFemale = not isMale
    isEven = match_day % 2 == 0
    isOdd = not isEven
    if isMale and isOdd:
        return A
    if isMale and isEven:
        return B
    if isFemale and isOdd:
        return B
    if isFemale and isEven:
        return A
    
    

def assign_fixture(f, match_day):
    logging.debug("Attempting to assign fixture for %s on %s" % (f.home, f.date))
    global date_slots
    global fixture_date_slots
    prefered_slots = []
    availabile_slots = []
    available_prefered = []

    if f.home == "Wakefield 1 Ladies":
        prefered_slots.append(Slot('12:00:00', 'Blue'))

    elif f.home == "Wakefield Wanderers 1 Ladies":
        prefered_slots.append(Slot('10:30:00', 'Green'))

    elif f.home == "Wakefield 1 Mens":
        prefered_slots.append(Slot('12:00:00', 'Blue'))
        prefered_slots.append(Slot('15:00:00', 'Blue'))

    elif f.home == "Wakefield 2 Ladies":
        prefered_slots.append(Slot('12:00:00', 'Blue'))
        prefered_slots.append(Slot('13:30:00', 'Blue'))
        prefered_slots.append(Slot('15:00:00', 'Blue'))

    elif "Ladies" in f.home:
        prefered_slots = get_preferences(f, match_day)

    elif "Mens" in f.home:
        prefered_slots = get_preferences(f, match_day)

    if not prefered_slots:
        logging.warning("No prefered slots for %s" % (f.home))

    availabile_slots = [
            date_slot for date_slot in date_slots
            if date_slot.date == f.date
            ]

    chosen = None
    for p in prefered_slots:
        logging.debug("Checking for a %s %s for %s on %s" % (
                p.time, p.pitch, f.home, f.date))
        prefered_and_available = [
                a for a in availabile_slots
                if a.pitch == p.pitch and a.time == p.time
                ]
        if prefered_and_available:
            chosen = prefered_and_available[0]
            logging.debug("    Found %s %s" % (chosen.time, chosen.pitch))
            break
        else:
            logging.debug("    None Available.")
    else:
        logging.warning("No slot for %s on %s" % (f.home, f.date))

    if chosen:
        fixture_date_slot = FixtureDateSlot(
            f.date, chosen.time, chosen.pitch, f.home, f.away)
        fixture_date_slots.append(fixture_date_slot)
        date_slots.remove(chosen)
        return

    # Split the rest by gender and sort by rank


def by_rank(f):
    pattern = r'(?P<Club>[\w\s]+) (?P<Rank>\d{1}) (?P<Gender>\w+)'
    m = match(pattern, f.home)
    rank = int(m.group('Rank'))
    gender = m.group('Gender')
    return (rank, gender)

by_date = lambda f: f.date
sorted_fixtures = sorted(fixtures, key=by_date)
fixtures_by_date = groupby(sorted_fixtures, key=by_date)

fixture_date_slots = []
logging.basicConfig(level=logging.WARN)
for match_day, (date, fs) in enumerate(fixtures_by_date):
    fixtures_by_rank = sorted(fs, key=by_rank)
    for f in fixtures_by_rank:
        assign_fixture(f, match_day)

writer = csv.writer(sys.stdout)
for fixture_date_slot in fixture_date_slots:
    date, time, pitch, home, away = fixture_date_slot
    writer.writerow([date, time, pitch, home, away])


