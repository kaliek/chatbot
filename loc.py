import requests

try:
    with open('googlemap_api.txt', 'r') as f:
        API = f.readline().strip()
except IOError:
    print("No token file. Please create a token.txt with your token in the first line.")
    sys.exit()

def get_lat_lng(add):
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(add, API))
    location = response.json()["results"][0]["geometry"]["location"]
    return [location['lat'], location['lng']]

