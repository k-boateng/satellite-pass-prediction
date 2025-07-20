from skyfield.api import load,wgs84
from skyfield.almanac import dark_twilight_day

ts = load.timescale()
satellites = load.tle_file("https://celestrak.org/NORAD/elements/visual.txt")


#Testing using SL-16 R/B
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['SL-16 R/B']
observer = wgs84.latlon(42.3583,-71.0603)
solar_ephemeris = load('de421.bsp') #loads ephemeris for twilight data


#Time Range
tStart = ts.now()
tEnd = ts.utc(tStart.utc.year, tStart.utc.month, tStart.utc.day + 2)

t, events = satellite.find_events(observer, tStart, tEnd, altitude_degrees=30)


def is_dark_enough(time):
    #0 -> night
    #1 -> astronomical twilight
    #2 -> nautical twilight
    #3 -> Civil twilight
    #4 -> daylight

    return dark_twilight_day(solar_ephemeris, observer)(time) < 3


for ti, event in zip(t, events):
    eventType = ""
    if event == 0:
        eventType = "Rise:"
    elif event == 1:
        eventType = "Peak:"
    elif event == 2:
        eventType = "Set:"

    if satellite.at(ti).is_sunlit(solar_ephemeris) and is_dark_enough(ti):
        print(f"{eventType} {ti.utc_strftime()}")
