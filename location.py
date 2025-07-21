import requests

def get_observer_location():
    try:
        print("Using your Ip to detect your location...")
        response = requests.get("https://ipinfo.io/json", timeout=10)
        data = response.json()
        loc = data.get("loc", "")  #(latitude,longitude)
        if loc:
            splitLoc = loc.split(",")
            lat = float(splitLoc[0]) #latitude
            lon = float(splitLoc[1]) #longitude
            print(f"Your location: {lat:.4f}, {lon:.4f}")
            return lat, lon, 0  # Default elevation which is 0m
    except Exception as e:
        print(f"IP location lookup failed: {e}")

    # If unable to detect location
    print("Please enter your location manually.")
    lat = float(input("Latitude: "))
    lon = float(input("Longitude: "))
    try:
        elev = float(input("Elevation in meters (optional, default 0): ") or 0)
    except:
        elev = 0

    return lat, lon, elev

if __name__ == "__main__":
    pass
