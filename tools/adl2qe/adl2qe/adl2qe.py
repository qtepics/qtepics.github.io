#!/usr/bin/env python
#
# $File: //ASP/tec/gui/qtepics.github.io/trunk/tools/adl2qe/adl2qe/adl2qe.py $
# $Revision: #4 $
# $DateTime: 2021/03/15 10:44:49 $
# Last checked in by: $Author: starritt $
#

import os
import os.path
import json
import sys
import click

from . import __version__
from . import adl2dict
from . import adl2uigen


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
Alarm Modes
\b
EPICS Qt and MEDM differ in the way alarm modes are presented. While both 
provide the option to present data with or without an alarm mode colour, MEDM
sets the foreground, i.e. text colour, whereas EPICS Qt sets the background 
colour. When the widget is alarm sensiitve, the nominated MEDM font colour,
say white, may not be suitable for the default pale-ish EPICS Qt backround 
alarm colours, and is therefore set to black.
\b\n\b
Engineering Units
\b
MEDM has no option to implicitly present engineering units. These can be 
presented explicitly using a separate monitor of the .EGU field. The EPICS Qt 
addUnits property is neither set nor cleared by adl2qe, and each widget will
or will not present engineering units dependent on the widget class default.
\b
Requires python 3.6 or later.
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
Specifies geometry scaling (percent). Must be in the range 40 to 400.\
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--font_size', '-f',
              type=click.IntRange(4, 72),
              default=8,
              show_default=True,
              help="""\
Specifies font point size. Must be in the range 4 to 72.\
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--default_colours', '-c',
              is_flag=True,
              help="""\
Use default EPICS Qt colours for most widgets, i.e. ignore the MEDM \
colours specified in the .adl file(s).\
""")
#
# -----------------------------------------------------------------------------
#
@click.option('--version', '-v',
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
#------------------------------------------------------------------------------
#
def main(debug, scale, font_size, default_colours, filenames):
    """ adl2qe converts one or more medm .adl files into EPICS Qt .ui files.
    """
    count = 0
    success = 0
    
    for adl_file in filenames:
        count += 1

        parts = os.path.splitext(adl_file)
        if parts [1] != ".adl":
            print ("warning: %s does not have .adl extension" % adl_file)

        ui_file = parts[0] + ".ui"

        try:
            adl_dic = adl2dict.load_file(adl_file)
        except:
            print("failed to parse %s" % adl_file)
            raise

        if adl_dic == None:
            print("parse of %s returned None" % adl_file)
            continue

        
        if debug:
            print ("%s:\n%s\n\n" % (adl_file, json.dumps (adl_dic, indent=4)))

        try:
            adl2uigen.dump_to_file (ui_file, adl_dic, scale, font_size, default_colours)
            print("generated: %s" % ui_file)
        except:
            print("failed to write to %s" % ui_file)
            raise
            
        
        success += 1
        
    print("")
    print("adl2qe complete:  %d out of %d successfull" % (success, count))


__doc__ = main.__doc__


def call_cli ():
    """ Click wrapper function. This sets env variables for click and
        python 3, does no harm for python 2
    """
    os.environ["LANG"] = "en_US.utf8"
    os.environ["LC_ALL"] = "en_US.utf8"
    main()


if __name__ == "__main__":
    call_cli()

# end
