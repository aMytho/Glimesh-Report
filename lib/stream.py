import sys
import requests

TGREEN = '\033[32m' # Green Text
ENDC = '\033[m' # reset to the defaults
BLUE = "\x1b[34m"

def get_stream_info(name, client_id):
    print("Searching for " + str(name))

    if name == "cancel()":
        sys.exit("Ending Report")

    requestBody = 'query {user(username: "%s") {id, countFollowers, username, channel {status, stream {countViewers, title, category {name}}}}}'%name
    auth = {'Authorization': f'Client-ID {client_id}'}

    glimeshResponse = requests.post('https://glimesh.tv/api/graph', headers=auth, data=requestBody)
    data = glimeshResponse.json()

    # Make sure the user actually exists
    if "data" not in data:
        sys.exit("That user was not found.")

    data = data["data"]

    # default properties
    followCount = data["user"]["countFollowers"]
    status = data["user"]["channel"]["status"]

    # check for a stream
    stream = data["user"]["channel"]["stream"]
    if stream:
        viewCount = stream["countViewers"]
        title = stream["title"]
        category = stream["category"]["name"]

        report = f"{name} has {followCount} followers. Channel status: {status}."
        streamReport = f"Curently streaming {title} in {category} with {viewCount} viewers."

        print(TGREEN + "- - - User Info - - -" + ENDC)
        print(report)
        print(TGREEN + "- - - Stream Info - - -" + ENDC)
        print(streamReport)

        print("Access last 10 chat messages?")
        if "y" == input("y / n | "):
            messageRequestBody = 'query {channel(streamerUsername: "%s") {chatMessages(last:10) {edges {node {message, insertedAt, user {username}}}}}}'%name
            messageRequest = requests.post('https://glimesh.tv/api/graph', headers=auth, data=messageRequestBody)

            messageData = messageRequest.json()
            messages = messageData["data"]["channel"]["chatMessages"]["edges"]

            for i in range(len(messages)):
                print(BLUE + messages[i]["node"]["user"]["username"] + ": " + ENDC + messages[i]["node"]["message"] + " | Timestamp: " + messages[i]["node"]["insertedAt"])
            sys.exit(TGREEN + "- - - Finished - - -" + ENDC)
        else: 
            sys.exit(TGREEN + "- - - Finished - - -" + ENDC)
    else:
        report = f"{name} has {followCount} followers. Channel status: {status}"
        print(report)
        sys.exit(TGREEN + "- - - Finished - - -" + ENDC)