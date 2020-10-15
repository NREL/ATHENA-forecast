'''
This is a local notebook module of helper definitions and functions for interacting with the TomTom Traffic Stats API.
'''
def get_24_hours(day):
    timeSets = []
    for hour in all_24_hours:
        timeSets.append({
            "name": day + " " + hour,
            "timeGroups": [{"days": [day], "times": [hour]}]
        })
    return timeSets
    

all_24_hours = [
            "0:00-1:00",
            "1:00-2:00",
            "2:00-3:00",
            "3:00-4:00",
            "4:00-5:00",
            "5:00-6:00",
            "6:00-7:00",
            "7:00-8:00",
            "8:00-9:00",
            "9:00-10:00",
            "10:00-11:00",
            "11:00-12:00",
            "12:00-13:00",
            "13:00-14:00",
            "14:00-15:00",
            "15:00-16:00",
            "16:00-17:00",
            "17:00-18:00",
            "18:00-19:00",
            "19:00-20:00",
            "20:00-21:00",
            "21:00-22:00",
            "22:00-23:00",
            "23:00-23:59"
          ]


dfw_network = {
    "name": "DFW",
      "geometry" : {
      "type": "Polygon",
      "coordinates":
        [[
            [-97.02,32.93],
            [-97.06,32.93],
            [-97.06,32.86,],
            [-97.02,32.86],
            [-97.02,32.93]
        ]]
        },
    "frcs": [
      "0",
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8"
    ],
    "timeZoneId": "US/Central",
    "probeSource":"ALL"
 }

days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN" ]

northTollPlazaLoc = {
    "latitude": 32.92351238213842,
    "longitude": -97.0410394384423
}
southTollPlazaLoc = {
    "latitude": 32.865513585114066,
    "longitude": -97.03972786933822
}
northExitLoc = {
    "latitude": 32.923487588624276,
    "longitude": -97.03972999192325
}
southExitLoc = {
    "latitude": 32.8661838354284,
    "longitude": -97.04149908506382
}
