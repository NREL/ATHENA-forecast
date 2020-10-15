""" Author: Monte Lunacek
    Purpose: Define SQL strings used in the database.py class
"""
dfw_weather = """
select * from dfw_weather;
"""

bus_ridership = """
select 
date_trunc('hour', period_end) +
    (((date_part('minute', period_end)::integer / 30::integer) * 30::integer)
    || ' minutes')::interval  AS period,
route, sum(pax_count_non_ada) as sum
FROM dfw_bus_ridership
group by route, period;
"""

control_plaza = """
SELECT date_trunc('hour', entry_time) +
    (((date_part('minute', entry_time)::integer / 30::integer) * 30::integer)
    || ' minutes')::interval  AS period,
    count(veh_count) AS COUNT 
FROM dfw_plaza_entryexit  
WHERE ( stay_min < 120 and 
        stay_min > 8)
GROUP BY period 
ORDER BY period;
"""

flights = """
SELECT f.flight_sched_time AS period, 
    f.flight_dest_org,
    f.flight_operation, 
    f.flight_type, 
    f.flight_regno, 
    a.num_seats
FROM dfw_flights f
    LEFT OUTER JOIN faa_nnumber n ON n.n_number = f.flight_regno
    LEFT OUTER JOIN faa_aircraft a ON n.mfr_model_code = a.mfr_code 
WHERE flight_type = 'PAX'
"""

summary_table = """
SELECT * FROM summary_table;
"""

weather_table = """
SELECT * FROM weather_table;
"""

dfw_plaza_entryexit = """
select * from dfw_plaza_entryexit;
"""
