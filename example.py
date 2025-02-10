import os
import requests
from enum import Enum
from typing import Optional

with open(os.path.expanduser('~') + "/.bvtoken.secret", 'r') as f:
    MY_TOKEN = f.readline()[:-1] #access token in hidden file

headers = {
    "Authorization": f"Bearer {MY_TOKEN}"
}

class Stats(Enum):
    CALLS = "calls"
    CALLS_MADE = "callsmade"
    CALLS_ANSWERED = "callsanswered"
    CALLS_RECEIVED = "callsereceived"
    UNANSWERED = "callsunanswered"
    SPEND = "callspend"

class TimeUnit(Enum):
    DAY = "86400"
    FIVE_DAYS = "432000"
    WEEK = "604800"
    TWO_WEEKS = "1209600"
    FOUR_WEEKS = "2419200"

def append_valid_xforms(valid_xforms, stat):
    if stat.value == "callsanswered":
        valid_xforms.extend([
            "sumringday", "sumringhour", "avhourring", "avdayring"
        ])
    elif stat.value == "callspend":
        valid_xforms.extend([
            "maxspendhour", "maxspendday", "sumspendhour", "sumsspendday"
        ])


def get_babble_stats(device, stat: Optional[Stats] = None, xform=None, timespan: Optional[TimeUnit]=None, offset: Optional[TimeUnit]=None):
    valid_xforms = [
        "meanhour", "minhour", "maxhour", "sumbillday", "sumbillhour",
        "sumdurationday", "sumdurationhour", "countday", "counthour",
        "avhourbillsec", "avavdaybillsec", "avhourduration", "avavdayduration"
        ]

    append_valid_xforms(valid_xforms, stat)
    
    if xform not in valid_xforms:
        xform = ""
        print("invalid xform")

    url = "https://www.babblevoice.com/api/device/stats"
    params = {
        "f": device,  
        "s": stat.value if stat is not None else '',
        "x": xform,  
        "t": timespan.value if timespan is not None else '',  
        "o": offset.value if offset is not None else '',
        "of": "json"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching stats")
        return None

devices = requests.get("https://www.babblevoice.com/api/device", headers=headers).json()
print(f"number of devices on the server: {len(devices["rows"])}")

leighton_stats = get_babble_stats("9022@omniis.babblevoice.com", Stats.CALLS_ANSWERED, timespan=TimeUnit.FIVE_DAYS, xform="sumringhour")
print(leighton_stats)

