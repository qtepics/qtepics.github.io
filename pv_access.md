# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>PV Access Support for EPICS Qt </span>


[Introduction](#Introduction)<br>


# <a name="Introduction"></a><span style='color:#006666'>Introduction</span>

The new PV Access protocol have been available as EPICS 4 modules and has
recently been merged into EPICS base as part of EPICS 7.
As the Australian Synchrotron is planning to include some EPICS 7 functionality,
especially in new BRIGHT beam-lines, we have decided to add support for PV Access
to the EPICS Qt (QE) framework.
This support is being introduced as part of the EPICS Qt 3.7 release.

On this page you will find some information about some design decisions, how to
prepare the build environment and how to build and use the modified.

# <a name="Design_Decisions"></a><span style='color:#006666'>Design Decisions</span>

## EPICS Version

While I suspect it would be possible to add PV Access by building against
EPICS 3.15.5 and EPICS 4.6 for example, the inclusion of PV Access into the
framework is selected by checking for EPICS 7 or later.

When performing a headless build, the qeframeworkSup/Makefile checks the EPICS
version and sets the QE_PVACCESS_SUPPORT environment variable accordingly:

    ifdef BASE_7_0
       export QE_PVACCESS_SUPPORT := YES
    else
       export QE_PVACCESS_SUPPORT := NO
    endif

The framework.pro project file checks for this environment variable and if set to
'YES', then adds QE_PVACCESS_SUPPORT to the set of DEFINES.
It also adds pvData, pvAccess and nt to the set of required libraries.

The inclusion of the PV Access functionality depends using EPICS base 7.
If not using EPICS base 7, the qmake phase outputs a warning message, but
build process continues without the PV Access functionality.

If building the EPICS Qt framework using _qtcreator_, you will have to explicitly
set this environment variable.

The EPICS Qt framwwoek code also checks the EPICS base version (see QEPvaCheck.h),
and will

    #error Including PV ACCESS support requires EPICS base 7 or later.

if the QE_PVACCESS_SUPPORT macro is defined _and_  EPICS_VERSION < 7.


# Building EPICS base 7

### -std=gnu++11

The PV Access modules make extensive use of C++, and I ran into a name mangling
issue when building the QE framework against base-7.0.1.1.
Adding the following line to _base_/configure/os/CONFIG_SITE.Common.linux-x86_64

    OPT_CXXFLAGS += -std=gnu++11

fixed this problem. _Thanks to Michael Davidsaver for the solution_.
These are the same flags that Qt uses when compiling the QE framework.
It was easier to build EPICS base with this flag that rebuild Qt.

Notes:
   - So far (as of April 2019) I have only built the PV Access support on CentOS 7 using gcc.
   - Where I placed/specified the extra OPT_CXXFLAGS could probably be relocated
such that it only impacts the building of the PV Access modules, and not _everything_
There may be a better place with a more restricted scope to specify this.
   - That said, I have build/run many other EPICS related modules with this additional
   flag in place with no apparent ill effects.

### modules/normativeTypes/src/nttable.cpp

For base-7.0.2, I found an apparent bug in nttable.cpp  
At line 274 in the NTTable::getColumnNames function, replace

    return pvNTTable->getStructure()->getFieldNames();

with

    return pvValue->getStructure()->getFieldNames();


# Building EPICS Qt 3.7

The low level api code to the Channel Access library has been striped out of the
framework and replaced by the ACAI library.
This is irrespective of the inclusion/exclusion of the PV Access functionality.

ACAI provides a thin-ish C++ wrapper around the low level Channel Access API.
The ACAI library is available from git hub:

    git clone https://github.com/andrewstarritt/acai.git

This has been in use operationally at the Australian Synchrotron since the startedof 2019 without issue. It has been successfully built on Linux CentOS 6 and 7 using gcc and on Windows 7 and 10 using mingw.

If building headless, then the qeframework component's configure/RELEASE file
must be modified to point to the ACAI's top directory.

If building the EPICS Qt framework using _qtcreator_, you will have to explicitly
set the ACAI environment variable to point to this location.

# New/Modified Widgets

A new widget QENTTable has been created to specifically support the NTTableData
normative type.

The QEImage widgets has been updated to support the NTNDArrayData normative type.
Currently this only supports mono 8-bit pixel images.

# Protocol Selection

All widgets' variable (PV) properties may now be prefixed by __&lt;protocol&gt;://__
in order to specify the protocol to be used.
The default protocol when no protocol has been specified is Channel Access.

The allowed protocols are __ca__ for Channel Access and when built against EPICS 7,
__pva__ for PV Access. Examples:

    ca://CURRENT_MONITOR   - connect using Channel Access.
    pva://CURRENT_MONITOR  - connect using PV Access.
    CURRENT_MONITOR        - connect using default protocol, Channel Access.
    xyz://CURRENT_MONITOR  - unknown protocol

In future releases, the default protocol may be selectable by an environment variable.

The functionality that determines the required protocol strips of the characters
before the first __://__ in the specified variable name and uses this to select
the protocol.
This has the following consequence: if using a PV whose names contains the actual
character sequence "__://__", then you _must_ explicitly proceeded the PV name with
a protocol specifier.

In this respect, 3.7 is not backward compatible with 3.6 even if the PV Access
functionality is not included.
In practice, this should not be a problem unless you have a weird PV naming
convention.

<font size="-1">Last updated: Fri Apr  5 19:49:02 AEDT 2019</font>
<br>
