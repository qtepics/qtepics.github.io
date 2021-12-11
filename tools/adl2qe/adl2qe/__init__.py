""" adl2qe
    MEDM adl file to EPICS Qt ui file converter
"""

import enum

__version__ = "1.2.1"
__license__ = "GPL3"


# Determines how displayAlarmStateOption is specified.
#
AlarmMode = enum.Enum("AlarmMode", ("when_in_alarm",    # Always set to WhenInAlarm
                                    "widget_default",   # i.e. not set at all
                                    "medm_mode"))       # use medm clrmod setting

# end
