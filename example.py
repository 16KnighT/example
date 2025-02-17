import os
import requests
from enum import Enum
from typing import Optional

#retrieves access token
with open(os.path.expanduser('~') + "/.bvtoken.secret", 'r') as f:
    MY_TOKEN = f.readline()[:-1] #access token in hidden file

headers = {
    "Authorization": f"Bearer {MY_TOKEN}"
}

#acceptable stats for queues and devices
class DeviceStats(Enum):
    CALLS = "calls"
    CALLS_MADE = "callsmade"
    CALLS_ANSWERED = "callsanswered"
    CALLS_RECEIVED = "callsereceived"
    UNANSWERED = "callsunanswered"
    SPEND = "callspend"

class QueueStats(Enum):
    ANSWERED = "answered"
    ABANDONED = "abandoned"
    QUEUE = "queue"

#acceptable time spans
class TimeUnit(Enum):
    DAY = "86400"
    FIVE_DAYS = "432000"
    WEEK = "604800"
    TWO_WEEKS = "1209600"
    FOUR_WEEKS = "2419200"

#base Xform class
class BaseXform(Enum):

    #checks if the class supports a specific stat
    @classmethod
    def supports_stat(cls, stat: str) -> bool:
        return stat in cls.__related_stats__

    #returns a list of xforms in the class
    @classmethod
    def valid_xform(cls):
        return [member.value for member in cls]

#subclasses for organisation
class BaseDeviceXform(BaseXform):
    pass
class BaseQueueXform(BaseXform):
    pass

class DeviceXforms(BaseDeviceXform):
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

class XformsDeviceAnswered(BaseDeviceXform):
    __related_stats__ = ["callsanswered"]
    SUM_RING_DAY = "sumringday"
    SUM_RING_HOUR = "sumringhour"
    AV_HOUR_RING = "avhourring"
    AV_DAY_RING = "avdayring"

class XformsDeviceSpend(BaseDeviceXform):
    __related_stats__ = ["callspend"]
    MAX_SPEND_HOUR = "maxspendhour"
    MAX_SPEND_DAY = "maxspendday"
    SUM_SPEND_HOUR = "sumspendhour"
    SUM_SPEND_DAY = "sumspendday"

class XformQueueAnswered(BaseQueueXform):
    __related_stats__ = ["answered"]
    MAX_HOUR_WAIT = "maxhourwait"
    MAX_DAY_WAIT = "maxdaywait"
    MAX_HOUR_BRIDGE = "maxhourbridge"
    MAX_DAY_BRIDGE = "maxdaybridge"
    MIN_HOUR_WAIT = "minhourwait"
    MIN_DAY_WAIT = "mindaywait"
    MIN_HOUR_BRIDGE = "minhourbridge"
    MIN_DAY_BRIDGE = "mindaybridge"
    MEAN_HOUR_WAIT = "meanhourwait"
    MEAN_DAY_WAIT = "meandaywait"
    MEAN_HOUR_BRIDGE = "meanhourbridge"
    MEAN_DAY_BRIDGE = "meandaybridge"
    SUM_HOUR_WAIT = "sumhourwait"
    SUM_DAY_WAIT = "sumdaywait"
    SUM_HOUR_BRIDGE = "sumhourbridge"
    SUM_DAY_BRIDGE = "sumdaybridge"
    COUNT_HOUR = "counthour"
    COUNT_DAY = "countday"

class XformQueueAbandoned(BaseQueueXform):
    __related_stats__ = ["abandoned"]
    MAX_HOUR_WAIT = "maxhourwait"
    MAX_DAY_WAIT = "maxdaywait"
    MIN_HOUR_WAIT = "minhourwait"
    MIN_DAY_WAIT = "mindaywait"
    MEAN_HOUR_WAIT = "meanhourwait"
    MEAN_DAY_WAIT = "meandaywait"
    SUM_HOUR_WAIT = "sumhourwait"
    SUM_DAY_WAIT = "sumdaywait"
    COUNT_HOUR = "counthour"
    COUNT_DAY = "countday"

class XformQueue(BaseQueueXform):
    __related_stats__ = ["queue"]
    MAX_HOUR_MEMBER = "maxhourmember"
    MAX_DAY_MEMBER = "maxdaymember"
    MAX_HOUR_CONSUMER = "maxhourconsumer"
    MAX_DAY_CONSUMER = "maxdayconsumer"
    MAX_HOUR_CALLER = "maxhourcaller"
    MAX_DAY_CALLER = "maxdaycaller"
    MAX_HOUR_WAITING = "maxhourwaiting"
    MAX_DAY_WAITING = "maxdaywaiting"
    MAX_HOUR_BRIDGE = "maxhourbridge"
    MAX_DAY_BRIDGE = "maxdaybridge"
    COUNT_HOUR = "counthour"
    COUNT_DAY = "countday"
    MIN_HOUR_MEMBER = "minhourmember"
    MIN_DAY_MEMBER = "mindaymember"
    MIN_HOUR_CONSUMER = "minhourconsumer"
    MIN_DAY_CONSUMER = "mindayconsumer"
    MEAN_HOUR_CALLER = "meanhourcaller"
    MEAN_DAY_CALLER = "meandaycaller"
    MEAN_HOUR_WAITING = "meanhourwaiting"
    MEAN_DAY_WAITING = "meandaywaiting"
    MEAN_HOUR_BRIDGE = "meanhourbridge"
    MEAN_DAY_BRIDGE = "meandaybridge"

#checks if the xform is acceptable depending on the stat
def check_xform(xform, stat, cls):
    for enum_class in cls.__subclasses__():
        if enum_class.supports_stat(stat.value):
            supported_xforms = enum_class.valid_xform()
            if xform.value in enum_class.valid_xform(): return True

    return False

#function for retrieving device stats
def get_device_stats(device, stat: Optional[DeviceStats] = None, xform="", timespan: Optional[TimeUnit]=None, offset: Optional[TimeUnit]=None):
    
    if check_xform(xform, stat, BaseDeviceXform):
        xform = xform.value
    else:
        xform = ""
        print("invalid xform")

    print(xform)
    print(stat.value)

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

#function for retrieving queue stats
def get_queue_stats(group, domain, stat=None, xform=None, timespan: Optional[TimeUnit]=None, offset: Optional[TimeUnit]=None):

    if check_xform(xform, stat, BaseQueueXform):
        xform = xform.value
    else:
        xform = ""
        print("invalid xform")

    url = "https://www.babblevoice.com/api/queue/stats"
    params = {
        "g": group,  
        "d": domain,
        "s": stat if xform is not None else '',
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

leighton_stats = get_device_stats("9022@omniis.babblevoice.com", DeviceStats.CALLS_ANSWERED, timespan=TimeUnit.FIVE_DAYS, xform=ValidXformsAnswered.SUM_RING_HOUR)
print(leighton_stats)

queue_stats = get_queue_stats("Queue", "omniis.babblevoice.com", QueueStats.ABANDONED, XformQueue.SUM_DAY_WAIT, TimeUnit.DAY)
print(queue_stats)
