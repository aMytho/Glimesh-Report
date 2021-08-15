import os
from lib.stream import get_stream_info
from lib.live_channels import get_live_channels

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.split('='))
        for line in fh.readlines() if not line.startswith('#')
    )

os.environ.update(vars_dict)

function_to_run = input("What do you want a report on? 1 for stream info and 2 for live channels.")
if function_to_run == "1":
    name = input("Which channel do you want a report on? ")
    get_stream_info(name, os.environ['CLIENT_ID'])
elif function_to_run == "2":
    name = input("Which user do you want get the followers for? ")
    get_live_channels(name, os.environ['CLIENT_ID'])
else:
    print("Finished")