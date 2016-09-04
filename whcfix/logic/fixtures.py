import datetime

def is_fixtue_commencing(fixture, date_of_interest=None):
    if date_of_interest is None:
        date_of_interest = datetime.now()
    now = date_of_interest
    now_plus_15_minutes = datetime.now() + datetime.timedelta(minutes=15)
    return now < fixture.push_back < now_plus_15_minutes


def is_fixtue_finishing(fixture, date_of_interest=None):
    if date_of_interest is None:
        date_of_interest = datetime.now()
    now = date_of_interest
    fixtue_end = fixture.push_back + datetime.timedelta(minutes=60)
    return now > fixtue_end


def is_result_registered(fixture):
    return not fixture.result is None
