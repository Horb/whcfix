from collections import namedtuple
import csv
import sys
import logging

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

fixture_date_slots = []

with open('1718_DateSlots.csv', 'rb') as csvf:
    lines = csv.reader(csvf)
    for line in lines:
        date, time, pitch = line
        date_slots.append(DateSlot(date, time, pitch))


for fixture in fixtures:
    preferred_slots = []
    availabile_slots = []
    available_preferred = []

    # Determine Slot Preferences
    if fixture.home == "Wakefield 1 Ladies":
        preferred_slots.append(Slot('12:00:00', 'Blue'))

    elif fixture.home == "Wakefield Wanderers 1 Ladies":
        preferred_slots.append(Slot('10:30:00', 'Green'))

    elif fixture.home == "Wakefield 1 Mens":
        preferred_slots.append(Slot('12:00:00', 'Blue'))
        preferred_slots.append(Slot('15:00:00', 'Blue'))

    elif fixture.home == "Wakefield 2 Ladies":
        preferred_slots.append(Slot('12:00:00', 'Blue'))
        preferred_slots.append(Slot('13:30:00', 'Blue'))
        preferred_slots.append(Slot('15:00:00', 'Blue'))

    elif fixture.home == "Wakefield 2 Mens":
        preferred_slots.append(Slot('12:00:00', 'Blue'))
        preferred_slots.append(Slot('13:30:00', 'Blue'))
        preferred_slots.append(Slot('15:00:00', 'Blue'))

    elif "Ladies" in fixture.home:
        preferred_slots.append(Slot('15:00:00', 'Blue'))
        preferred_slots.append(Slot('13:30:00', 'Green'))
        preferred_slots.append(Slot('12:00:00', 'Blue'))

        preferred_slots.append(Slot('15:00:00', 'Green'))
        preferred_slots.append(Slot('13:30:00', 'Blue'))
        preferred_slots.append(Slot('12:00:00', 'Green'))

        preferred_slots.append(Slot('10:30:00', 'Green'))
        preferred_slots.append(Slot('16:30:00', 'Green'))
        preferred_slots.append(Slot('16:30:00', 'Blue'))
        preferred_slots.append(Slot('10:00:00', 'Blue'))

    elif "Mens" in fixture.home:
        preferred_slots.append(Slot('15:00:00', 'Green'))
        preferred_slots.append(Slot('13:30:00', 'Blue'))
        preferred_slots.append(Slot('12:00:00', 'Green'))

        preferred_slots.append(Slot('15:00:00', 'Blue'))
        preferred_slots.append(Slot('13:30:00', 'Green'))
        preferred_slots.append(Slot('12:00:00', 'Blue'))

        preferred_slots.append(Slot('16:30:00', 'Blue'))
        preferred_slots.append(Slot('10:00:00', 'Blue'))
        preferred_slots.append(Slot('10:30:00', 'Green'))
        preferred_slots.append(Slot('16:30:00', 'Green'))


    if not preferred_slots:
        logging.warning("No preferred slots for %s" % (fixture.home))
        continue

    availabile_slots = [
            date_slot for date_slot in date_slots
            if date_slot.date == fixture.date
            ]

    chosen = None
    for preferred in preferred_slots:
        logging.debug("Checking for a %s %s for %s on %s" % (
                preferred.time, preferred.pitch, fixture.home, fixture.date))
        for available in availabile_slots:
            logging.debug("    Against %s %s" % (available.time, available.pitch))
            if available.pitch == preferred.pitch and available.time == preferred.time:
                logging.debug("        Found %s %s" % (available.time, available.pitch))
                chosen = available
                break
        if chosen:
            break

    if chosen:
        fixture_date_slot = FixtureDateSlot(
                fixture.date, chosen.time, chosen.pitch, fixture.home, fixture.away)
        fixture_date_slots.append(fixture_date_slot)
        date_slots.remove(chosen)
    else:
        logging.warning("No slot for %s on %s" % (fixture.home, fixture.date))

writer = csv.writer(sys.stdout)
for fixture_date_slot in fixture_date_slots:
    date, time, pitch, home, away = fixture_date_slot
    writer.writerow([date, time, pitch, home, away])


