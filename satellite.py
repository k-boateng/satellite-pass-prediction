from skyfield.api import load,wgs84
from skyfield.almanac import dark_twilight_day

ts = load.timescale()
satellites = load.tle_file("https://celestrak.org/NORAD/elements/visual.txt")
solar_ephemeris = load('de421.bsp') #loads ephemeris for twilight data

print(f'Loaded {len(satellites)} Satellites')


all_passes = {}


def get_next_passes(lat, lon, days_ahead = 2, altitude_degrees=30): #higher altitude -> more visible
    #Time Range
    tStart = ts.now()
    tEnd = ts.utc(tStart.utc.year, tStart.utc.month, tStart.utc.day + days_ahead)

    #observer's postion
    observer = wgs84.latlon(lat, lon)

    for sat in satellites:
        t, events = sat.find_events(observer, tStart, tEnd, altitude_degrees)

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
                    if sat.at(ti).is_sunlit(solar_ephemeris) and is_dark_enough(ti):
                        current_pass['is_visible_peak'] = True

            elif event == 2:
                if current_pass and 'rise_time' in current_pass:
                    current_pass['set_time'] = ti
                    
                    #At this point, the pass has all three events
                    if current_pass.get('is_visible_peak', False):
                        visible_passes_count += 1
                        visible_passes[visible_passes_count] = current_pass

                    current_pass = {} #Resets for the next pass.

        all_passes[sat.name] = visible_passes
        
    return all_passes
        

if __name__ == "__main__":
    pass

