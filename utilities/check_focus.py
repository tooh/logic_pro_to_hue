#!/usr/bin/env python3

# needs full disk access permission for Terminal


import json
import os
import datetime

ASSERT_PATH = os.path.expanduser("~/Library/DoNotDisturb/DB/Assertions.json")
MODECONFIG_PATH = os.path.expanduser("~/Library/DoNotDisturb/DB/ModeConfigurations.json")
def get_focus():
    focus = "No focus" #default
    assertJ = json.load(open(ASSERT_PATH))['data'][0]['storeAssertionRecords']
    configJ = json.load(open(MODECONFIG_PATH))['data'][0]['modeConfigurations']
    if assertJ:
        modeid = assertJ[0]['assertionDetails']['assertionDetailsModeIdentifier']
        focus = configJ[modeid]['mode']['name']
    else:
        date = datetime.datetime.today()
        now = date.hour * 60 + date.minute

        for modeid in configJ:
            triggers = configJ[modeid]['triggers']['triggers'][0]
            if triggers and triggers['enabledSetting'] == 2:
                start = triggers['timePeriodStartTimeHour'] * 60 + triggers['timePeriodStartTimeMinute']
                end = triggers['timePeriodEndTimeHour'] * 60 + triggers['timePeriodEndTimeMinute']
                if start < end:
                    if now >= start and now < end:
                        focus = configJ[modeid]['mode']['name']
                elif start > end: # includes midnight
                    if now >= start or now < end:
                        focus = configJ[modeid]['mode']['name']
    return focus

if '__main__' == __name__:
    print(get_focus())
