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

class BaseXform(Enum):

    @classmethod
    def supports_stat(cls, stat: str) -> bool:
        return stat in cls.__related_stats__

    @classmethod
    def valid_xform(cls):
        return [member.value for member in cls]


class ValidXforms(BaseXform):
    __related_stats__ = ["calls", "callsmade", "callsanwered", "callsreceived" "callsunanswered", "callspend"]
    MEAN_HOUR = "meanhour"
    MIN_HOUR = "minhour"
    MAX_HOUR = "maxhour"
    SUM_BILL_DAY = "sumbillday"
    SUM_BILL_HOUR = "sumbillhour"
    SUM_DURATION_DAY = "sumdurationday"
    SUM_DURATION_HOUR = "sumdurationhour"
    COUNT_DAY = "countday"
    COUNT_HOUR = "counthour"
    AV_HOUR_BILL_SEC = "avhourbillsec"
    AV_DAY_BILL_SEC = "avdaybillsec"
    AV_HOUR_DURATION = "avhourduration"
    AV_DAY_DURATION = "avdayduration"

class ValidXformsAnswered(BaseXform):
    __related_stats__ = ["callsanswered"]
    SUM_RING_DAY = "sumringday"
    SUM_RING_HOUR = "sumringhour"
    AV_HOUR_RING = "avhourring"
    AV_DAY_RING = "avdayring"

class ValidXformsSpend(BaseXform):
    __related_stats__ = ["callspend"]
    MAX_SPEND_HOUR = "maxspendhour"
    MAX_SPEND_DAY = "maxspendday"
    SUM_SPEND_HOUR = "sumspendhour"
    SUM_SPEND_DAY = "sumspendday"

def check_xform(xform, stat):
    for enum_class in BaseXform.__subclasses__():
        if enum_class.supports_stat(stat.value):
            supported_xforms = enum_class.valid_xform()
            if xform.value in enum_class.valid_xform(): return True

    return False

def get_babble_stats(device, stat: Optional[Stats] = None, xform="", timespan: Optional[TimeUnit]=None, offset: Optional[TimeUnit]=None):
    
    if check_xform(xform, stat):
        xform = xform.value
    else:
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

leighton_stats = get_babble_stats("9022@omniis.babblevoice.com", Stats.CALLS_ANSWERED, timespan=TimeUnit.FIVE_DAYS, xform=ValidXformsAnswered.SUM_RING_HOUR)
print(leighton_stats)

