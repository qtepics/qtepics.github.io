#!/usr/bin/env python
#
# File: tools/adl2qe/adl2qe/adl2qe.py
# DateTime: Mon May 26 17:20:40 2025
# Last checked in by: starritt
#

import os
import os.path
import json
import sys
import click

from . import __version__
from . import AlarmMode
from . import FrameworkVersionValues
from . import FrameworkVersion
from . import adl2dict
from . import adl2uigen

# map for click ioptions.
#
_alarm_mode_map = {'WIA': AlarmMode.when_in_alarm,
                   'WD': AlarmMode.widget_default,
                   'MM': AlarmMode.medm_mode}

_alarm_mode_choices = tuple(_alarm_mode_map.keys())



# -----------------------------------------------------------------------------
#
def print_version(ctx, param, value):
    """ Click parser helper function """
    if not value or ctx.resilient_parsing:
        return

    vi = sys.version_info
    print("adl2qe version: %s  (python %s.%s.%s)" % (__version__, vi.major, vi.minor, vi.micro))
    ctx.exit()


# -----------------------------------------------------------------------------
# Allow -h as well as --help
#
context_settings = dict(help_option_names=['--help', '-h'],
                        terminal_width=96,
                        max_content_width=96)
#
# -----------------------------------------------------------------------------
# epilog test formatting not so great - the \b\n\b forces two newlines
#
@click.command(context_settings=context_settings,
               epilog="""
\b\n\b
\b\bAlarm Modes
\b
EPICS Qt and MEDM differ in the way alarm modes are presented. While both
provide the option to present data with or without an alarm mode colour, MEDM
sets the foreground, i.e. text colour, whereas EPICS Qt sets the background
colour. When the widget is alarm sensiitve, the nominated MEDM font colour,
say white, may not be suitable for the default pale-ish EPICS Qt backround
alarm colours, and is therefore set to black.
\b
Use the --alarm_mode option to control how wigests responds to the PV being in
alarm. There are three options:
    \b
WIA - always set to WhenInAlarm (default),
WD  - use EPICS Qt widget default, and
MM  - use medm clrmod setting.

\b\n\b
\b\bEngineering Units
\b
MEDM has no option to implicitly present engineering units. These can be
presented explicitly using a separate monitor of the .EGU field. The EPICS Qt
addUnits property is neither set nor cleared by adl2qe, and each widget will
or will not present engineering units dependent on the widget class default.
\b\n\b
\b\bGeneral
\b
Requires python 3.6 or later.
The qe_3_to_4_update tool can be used to convert a .ui file from version 3 to version 4
as opposed to re-running adl2qe again with --qeversion v4. This is especially helpfull
if any post-conversion modification have been made.
\b\n\b
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--debug', '-d',
              is_flag=True,
              help="""\b \
Output debug information
""",
              show_default=True)
#
# -----------------------------------------------------------------------------
#
@click.option('--scale', '-s',
              type=click.IntRange(40, 400),
              default=100,
              show_default=True,
              help="""\
Specifies geometry scaling x (percent).\
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--font_size', '-f',
              type=click.IntRange(4, 72),
              default=8,
              show_default=True,
              help="""\
Specifies font point size x.\
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--add_colon', '-a',
              is_flag=True,
              help="""\
Add colons such that variable name PV reference change from '$(macro)' to '$(macro):'
The default macro_name is P.
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--macro_name', '-m',
              type=str,
              default="P",
              show_default=True,
              help="""\
Specifies the macro name to which colons are added. \
Only used inconjunction with the --add_colon flag.
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--default_colours', '-c',
              is_flag=True,
              help="""\
Use default EPICS Qt colours for most widgets, i.e. ignores the MEDM \
colours specified in the .adl file(s).
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--alarm_mode', '-l',
              type=click.Choice(_alarm_mode_choices),
              default='WIA',
              show_default=True,
              help="""\
Controls setting of the displayAlarmStateOption property value:
WIA - always set to WhenInAlarm,
WD - use EPICS Qt widget default, and
MM - use medm clrmod setting
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--qeversion', '-q',
              type=click.Choice(FrameworkVersionValues),
              help="""\
Controls if converting for EPICS Qt 3.x.x (v3) or for EPICS Qt 4.x.x (v4).
There is no default.
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--version', '-V',
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True,
              help="Show version and exit.")
#
# -----------------------------------------------------------------------------
# nargs is set to -1, so that an unlimited number of arguments are accepted.
#
@click.argument('filenames', nargs=-1, required=True)
#
# -----------------------------------------------------------------------------
#
def main(debug, scale, font_size, add_colon, macro_name, default_colours,
         alarm_mode, qeversion, filenames):
    """ adl2qe converts one or more medm .adl files into EPICS Qt .ui files.
    """
    if qeversion is None:
        print(f"Error: Invalid value for '--qeversion' / '-q': 'None' is not one of 'v3', 'v4'.", file = sys.stderr)
        os._exit(2)

    if not add_colon:
        macro_name = None

    alarm_state_option = _alarm_mode_map[alarm_mode]

    if qeversion == 'v3':
        qev = FrameworkVersion.v3
    elif qeversion == 'v4':
        qev = FrameworkVersion.v4
    else:
        print(f"Error parsing arguments", file = sys.stderr)
        os._exit(8)


    print (f"alarm_mode {alarm_mode}    qeversion {qev}")

    count = 0
    success = 0

    for adl_file in filenames:
        count += 1

        parts = os.path.splitext(adl_file)
        if parts[1] != ".adl":
            print("warning: %s does not have .adl extension" % adl_file)

        ui_file = parts[0] + ".ui"

        try:
            adl_dic = adl2dict.load_file(adl_file)
        except BaseException:
            print("failed to parse %s" % adl_file)
            raise

        if adl_dic is None:
            print("parse of %s returned None" % adl_file)
            continue

        if debug:
            print("%s:\n%s\n\n" % (adl_file, json.dumps(adl_dic, indent=4)))

        try:
            adl2uigen.dump_to_file(ui_file, adl_dic, scale, font_size,
                                   default_colours, alarm_state_option,
                                   macro_name, qev)
            print("generated: %s" % ui_file)
        except BaseException:
            print("failed to write to %s" % ui_file)
            raise

        success += 1

    print("")
    print("adl2qe complete:  %d out of %d successfull" % (success, count))


__doc__ = main.__doc__


def call_cli():
    """ Click wrapper function. This sets env variables for click and
        python 3, does no harm for python 2
    """
    os.environ["LANG"] = "en_US.utf8"
    os.environ["LC_ALL"] = "en_US.utf8"
    main()


if __name__ == "__main__":
    call_cli()

# end
