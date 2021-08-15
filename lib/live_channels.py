import sys
import requests

TGREEN = '\033[32m' # Green Text
ENDC = '\033[m' # reset to the defaults
BLUE = "\x1b[34m"

def get_live_channels(name, client_id):
    print("Getting live channels for " + str(name))

    if name == "cancel()":
        sys.exit("Ending Report")
    
    requestBody = 'query {user(username: "%s") {followingLiveChannels {edges {node {status, streamer {username}, stream {countViewers, title, category {name}}}}}}}'%name
    auth = {'Authorization': f'Client-ID {client_id}'}

    glimeshResponse = requests.post('https://glimesh.tv/api/graph', headers=auth, data=requestBody)
    data = glimeshResponse.json()

    # Make sure the user actually exists
    if "data" not in data:
        sys.exit("That user was not found.")

    channels = data["data"]["user"]["followingLiveChannels"]["edges"]

    for i in range(len(channels)):
        currentChannel = channels[i]["node"]

        if currentChannel["status"] != "OFFLINE":
            title = currentChannel["stream"]["title"]
            category = currentChannel["stream"]["category"]["name"]
            viewCount = currentChannel["stream"]["countViewers"]
            print(BLUE + "- - - Livestream Found - - -" + ENDC)
            print(currentChannel["streamer"]["username"] + " is Live")
            print(f"Curently streaming {title} in {category} with {viewCount} viewers.")

    sys.exit(TGREEN + "- - - Finished - - -" + ENDC)
