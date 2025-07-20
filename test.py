from skyfield.api import load,wgs84

ts = load.timescale()
satellites = load.tle_file("https://celestrak.org/NORAD/elements/visual.txt")


#Testing using SL-16 R/B
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['SL-16 R/B']

observer = wgs84.latlon(42.3583,-71.0603)

tStart = ts.now()
tEnd = ts.utc(tStart.utc.year, tStart.utc.month, tStart.utc.day + 2)

t, events = satellite.find_events(observer, tStart, tEnd, altitude_degrees=30)

for ti, event in zip(t, events):
    if event == 0:
        print(f"Rise: {ti.utc_strftime()}")
    elif event == 1:
        print(f"Culminate: {ti.utc_strftime()}")
    elif event == 2:
        print(f"Set: {ti.utc_strftime()}")
