#  hacky script to get a list of resources

import csv
import sys
import datetime

resources = []
reader = csv.reader(sys.stdin)
for row in reader:
    resources.append(row)




start_of_season = datetime.date(2017, 9, 2)
end_of_season = datetime.date(2018, 5, 5)
current_date = start_of_season

while current_date < end_of_season:
    for r in resources:
        dr = r + [str(current_date)]
        print(",".join(dr))
    sunday = current_date + datetime.timedelta(days=1)
    for r in resources:
        dr = r + [str(sunday)]
        print(",".join(dr))
    current_date += datetime.timedelta(weeks=1)

