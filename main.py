from location import get_observer_location
from satellite import get_next_passes

def format_satellite_output(all_passes_data):
    """
    Formats the output for satellite visibility data.

    Args:
        all_passes_data (dict): A dictionary where keys are satellite names
                                and values are dictionaries of pass details

    Returns:
        str: A formatted string displaying satellite names, number of passes,
             and details of each pass. If a satellite has no passes, it's not displayed.
    """

    output_lines = []
    for satellite_name, passes_dict in all_passes_data.items():
        if passes_dict:  # Only display if there are passes (dictionary is not empty)
            output_lines.append(f"{satellite_name}: {len(passes_dict)} visible pass(es)")
            
            # Iterate through the dictionary, sorting by pass number (key) for consistent order
            for pass_num in sorted(passes_dict.keys()):
                pass_details = passes_dict[pass_num]
                rise = pass_details['rise_time'].utc_datetime()
                peak = pass_details['peak_time'].utc_datetime()
                set_time = pass_details['set_time'].utc_datetime()
                output_lines.append(f"  Pass {pass_num}: Rise: {rise.strftime('%Y-%m-%d %H:%M:%S')}, Peak: {peak.strftime('%Y-%m-%d %H:%M:%S')}, Set: {set_time.strftime('%Y-%m-%d %H:%M:%S')}")
            output_lines.append("-" * 40)  # Separator
    return "\n".join(output_lines)

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
            output = format_satellite_output(passes)
            print(output)
        else:
            print(f"No visible satellites in your vicinity in the next {interval} day(s)")
            

        
if __name__ == "__main__":
    main()