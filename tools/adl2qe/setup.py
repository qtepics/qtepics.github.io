# $File: //ASP/tec/gui/qtepics.github.io/trunk/tools/adl2qe/setup.py $
# $Revision: #2 $
# $DateTime: 2019/08/25 21:37:19 $
# Last checked in by: $Author: starritt $
#
# setup.py for adl2qe
#

import re
from setuptools import setup

assert sys.version_info >= (3, 6), \
    "\n  you must use python 3.6 or greater.\n  currently using python %s.%s.%s" % \
    (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

with open('adl2qe/__init__.py', 'r') as f:
    version = re.search(r'__version__ = "(.*)"', f.read()).group(1)

setup(
    name="AS-Utils-adl2qe",
    version=version,
    author="Andrew Starritt",
    author_email="andrews@ansto.gov.au",
    license="GPL3",
    description="""adl2qe is an MEDM adl file to EPICS Qt ui file converter.\
""",
    packages=["adl2qe"],
    install_requires=[
        "click"
    ],
    entry_points="""
        [console_scripts]
        adl2qe=adl2qe.adl2qe:call_cli
    """
)

# end