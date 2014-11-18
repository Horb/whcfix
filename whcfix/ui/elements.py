import datetime


class DashboardItem(object):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    template = "dashboard_item_snippet.html"
    show_result_column = True

    def sort_priority(self, isoweekday):
        pass

    def __gt__(self, other):
        isoweekday = datetime.date.today().isoweekday()
        return self.sort_priority(isoweekday) > other.sort_priority(isoweekday)

    def __lt__(self, other):
        return not self.__gt__(other)

class NextMatchDashboardItem(DashboardItem):
    title = 'Next Match'
    show_result_column = False

    def __init__(self, listOfMatches):
        super(NextMatchDashboardItem, self).__init__()
        self.listOfMatches = listOfMatches

    def sort_priority(self, isoweekday):
        if isoweekday in [self.WEDNESDAY, self.THURSDAY, self.FRIDAY]:
            return 100
        else:
            return 10


class LastResultDashboardItem(DashboardItem):
    title = 'Last Result'

    def __init__(self, listOfMatches):
        super(LastResultDashboardItem, self).__init__()
        self.listOfMatches = listOfMatches

    def sort_priority(self, isoweekday):
        if isoweekday in [self.SATURDAY, self.SUNDAY, self.MONDAY, self.TUESDAY]:
            return 100
        else:
            return 10


class TodaysMatchesDashboardItem(DashboardItem):
    title = "Today"

    def __init__(self, listOfMatches):
        super(TodaysMatchesDashboardItem, self).__init__()
        self.listOfMatches = listOfMatches

    def sort_priority(self, isoweekday):
        return 1000
