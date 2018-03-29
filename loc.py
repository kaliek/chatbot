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

# checks if the question asks for location
# and if there is "ORGANIZATION" entity
# returns the location needs to be searched for
def isLocation(q_class, entity):
    orgs = []
    if q_class == "['LOC']" and entity:
        for e in entity:
            if e[1] in LOC:
                orgs.append(e[0])
    return orgs

# uses http request to ask Google Map about the location
# returns latitude and longitude of the location
def sendGMap(orgs):
    location = []
    for o in orgs:
        title = " ".join(o.split(","))
        location.append(get_lat_lng(title))
    return location
