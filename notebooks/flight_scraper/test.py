
from athena.scraper import get_flight_data

filename = get_flight_data("2019-10-25 00:00:00", "2019-10-30 00:00:00")
print(filename)



