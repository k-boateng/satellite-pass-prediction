from location import get_observer_location
from satellite import get_next_passes

def main():
        location = get_observer_location()
        
        lat = location[0]
        lon = location[1]

        while True:
            try:
                interval = int(input("How far ahead do you want to check?(days): "))
                break
            except:
                 print("Integers only. Please try again.")
                 continue
        
        print(f'Getting satellite passes over your location in the next {interval} day(s).')


        passes = get_next_passes(lat, lon, days_ahead=interval)

        if passes:
            print(passes)
        else:
            print(f"No visible satellites in your vicinity in the next {interval} day(s)")
            

        
if __name__ == "__main__":
    main()