""" adl2qe
    MEDM adl file to EPICS Qt ui file converter
"""

import enum

__version__ = "1.3.2"
__license__ = "GPL3"


# Determines how displayAlarmStateOption is specified.
#
AlarmMode = enum.Enum("AlarmMode", ("when_in_alarm",    # Always set to WhenInAlarm
                                    "widget_default",   # i.e. not set at all
                                    "medm_mode"))       # use medm clrmod setting

# Specifies if we converting files for use with QE 3.x.x or 4.x.x
#
FrameworkVersionValues = ("v3", "v4")
FrameworkVersion = enum.Enum("FrameworkVersion", FrameworkVersionValues)

# end
