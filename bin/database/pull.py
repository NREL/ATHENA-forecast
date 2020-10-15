""" Author: Monte Lunacek
    Purpose: Cache the main DFW tables for learning
"""
import athena

if __name__ == "__main__":


    db = athena.database.AthenaDatabase(cache=False)
    #print( db.bus_ridership_passengers() )
    #print( db.flight_passengers() )
    #print( db.control_plaza() )
    print( db.dfw_weather() )
  