###########################################################################
# This is a script to stop the running measurements. To run this script
# Change the API key to the user's API key.
###########################################################################
from ripe.atlas.cousteau import AtlasStopRequest

# API Key. Make sure to give StopRequest permission.
ATLAS_API_KEY = "f00d3214-a18e-4f6d-8188-104dd1192b36"

# List to hold all the request Ids.
req_list = []
# File with the request numbers
f = open("./resources/tostop", "r")

for line in f.readlines():
    req_list += line.strip()[1:-1].split(', ')

for req in req_list:
    atlas_request = AtlasStopRequest(msm_id=req.strip(), key=ATLAS_API_KEY)
    (is_success, response) = atlas_request.create()
    if is_success:
        print("Request Id - " + str(req) + " Successfully Stopped!!")
    else:
        print("Error Stopping Request Id - " + str(req))
