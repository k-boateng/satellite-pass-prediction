from skyfield.api import load,wgs84
from skyfield.almanac import dark_twilight_day

ts = load.timescale()
satellites = load.tle_file("http://www.celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle") #All active satellites


#Testing using SL-16 R/B
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']
observer = wgs84.latlon(42.3583,-71.0603)
solar_ephemeris = load('de421.bsp') #loads ephemeris for twilight data


#Time Range
tStart = ts.now()
tEnd = ts.utc(tStart.utc.year, tStart.utc.month, tStart.utc.day + 2)

t, events = satellite.find_events(observer, tStart, tEnd, altitude_degrees=30) #higher altitude -> more visible



def is_dark_enough(time):
    #0 -> night
    #1 -> astronomical twilight
    #2 -> nautical twilight
    #3 -> Civil twilight
    #4 -> daylight

    return dark_twilight_day(solar_ephemeris, observer)(time) < 3

visible_passes = {}
visible_passes_count = 0
current_pass = {}


for ti, event in zip(t, events):
    

    if event == 0:
        current_pass = {'rise_time': ti}
        current_pass['is_visible_peak'] = False #assumes the pass is not visible until the peak.
    
    elif event == 1:
        if current_pass and 'rise_time' in current_pass: #ensures the peak time has a corresponding rise time.
            current_pass['peak_time'] = ti
            #check visiblity conditions at peak
            if satellite.at(ti).is_sunlit(solar_ephemeris) and is_dark_enough(ti):
                current_pass['is_visible_peak'] = True

    elif event == 2:
        if current_pass and 'rise_time' in current_pass:
            current_pass['set_time'] = ti

            
            #At this point, the pass has all three events
            if current_pass.get('is_visible_peak', False):
                visible_passes_count += 1
                visible_passes[visible_passes_count] = current_pass

            current_pass = {} #Resets for the next pass.


print(visible_passes)
    
    

    







