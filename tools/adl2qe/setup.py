# File: tools/adl2qe/setup.py
# DateTime: Mon May 26 17:20:40 2025
# Last checked in by: starritt
#
# setup.py for adl2qe
#
# Note: to upload to aspypi, run command:
#
#    python setup.py sdist upload -r aspypi
#

import sys
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
