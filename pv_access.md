# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>PV Access Support for EPICS Qt </span>
<br>
[Introduction](#Introduction)<br>
[Normative Types](#Normative_Types)<br>
[Build Considerations](#Build_Considerations)<br>
[New/Modified Widgets](#New_Widgets)<br>
[Protocol Selection](#Protocol_Selection)<br>

# <a name="Introduction"> </a><span style='color:#006666'>Introduction</span>

This page provide information regarding the introduction of the use of the PV
Access protocol into EPICS Qt.

The PV Access protocol has been available as EPICS 4 modules for a number of years
and has recently been merged into EPICS base as part of EPICS 7.
As the Australian Synchrotron is planning to include some EPICS 7 functionality,
especially on new beam-lines, we have decided to add support for PV Access
to the EPICS Qt (QE) framework.

This support is being introduced as part of the EPICS Qt 3.7 release.

# <a name="Normative_Types"></a><span style='color:#006666'>Normative Types</span>

For the 3.7.1 release, the following normative types are be supported.

* NTScalar
* NTScalarArray
* NTEnum
* NTTable
* NTNDArray - only 8bit mono images are currently supported.

Support for other image types will be part of a later 3.7 release.
Support for other normative types will be added as and when needed.

# <a name="Build_Considerations"></a><span style='color:#006666'>Build Considerations</span>

## <span style='color:#0066a6'>Building EPICS</span>

If EPICS Qt is to be built with PV Access support - see below - then you will
need EPICS 7 or later.
While I suspect it would be possible to add PV Access functionality by building
against EPICS 3.15.5 and EPICS 4.6, the inclusion of PV Access into the EPICS Qt
framework is assumes you are using EPICS 7.

There are two things to be aware of.

### -std=gnu++11

The PV Access modules make extensive use of C++ templates, and I ran into some
name mangling issues when building the QE framework against base-7.0.1.1.
Adding the following line to _base_/configure/os/CONFIG_SITE.Common.linux-x86_64

    OPT_CXXFLAGS += -std=gnu++11

fixed this problem. _Thanks to Michael Davidsaver for suggesting the solution_.
This is one of the flags that Qt uses when compiling the QE framework.
It was easier to build EPICS base with this flag that rebuild Qt without it.

Notes:
   - So far (as of August 2019) I have only built the EPICS Qt PV Access support
   on CentOS 7 using gcc, other platforms/build chains may require something similar.
   - The extra OPT_CXXFLAGS could probably be relocated such that it _only_ impacts
   the building of the PV Access modules, and not _everything_ in EPICS base.
   There may be a better place with a more restricted scope to specify this.
   - That said, I have build/run many other EPICS related modules with this additional
   flag in place with no apparent ill effects.

### modules/normativeTypes/src/nttable.cpp

For base-7.0.2, I found an apparent bug in nttable.cpp which needs fixed to
QENTTablethe use of the QENTTable widget.

At line 274 in the NTTable::getColumnNames function, replace

    return pvNTTable->getStructure()->getFieldNames();

with

    return pvValue->getStructure()->getFieldNames();

This has since been fixed in base-7.0.3.

## <a name="Building_ACAI"></a><span style='color:#0066a6'>Building ACAI</span>

While not directly PV Access related, a significant change to the EPICS Qt framework
for release 3.7.1 is that the low level Channel Access code has been dropped, and
has been replaced by use of the ACAI library.
This is available from:

[https://github.com/andrewstarritt/acai](https://github.com/andrewstarritt/acai)

The need to include ACAI is irrespective of whether PV Access functionality is
or is not included. See the [getting started](getting_started.html#ACAI) page for
more information.

## <a name="Building_EPICS_Qt"></a><span style='color:#0066a6'>Building EPICS Qt 3.7</span>

While I suspect it would be possible to add PV Access by building against
EPICS 3.15.5 and EPICS 4.6, the inclusion of PV Access into the EPICS Qt framework
is selected by checking for EPICS 7 or later.

When performing a headless build, the qeframeworkSup/Makefile checks the EPICS
version and sets the QE_PVACCESS_SUPPORT environment variable accordingly:

    ifdef BASE_7_0
       export QE_PVACCESS_SUPPORT := YES
    else
       export QE_PVACCESS_SUPPORT := NO
    endif

The framework.pro project file checks for this environment variable and if set
to 'YES', then adds QE_PVACCESS_SUPPORT to the set of DEFINES.
It also adds pvData, pvAccess and nt to the set of required libraries.

The inclusion of the PV Access functionality depends using EPICS base 7.
If not using EPICS base 7, the qmake phase outputs a warning message, but
build process continues without the PV Access functionality.

If building the EPICS Qt framework using _qtcreator_, or explicitly calling qmake
and make then __you will have to__ explicitly set the QE_PVACCESS_SUPPORT environment
variable.

The EPICS Qt framework code also has a checks the EPICS base version if the
QE_PVACCESS_SUPPORT macro defined (see QEPvaCheck.h), and will:

    #error Including PV ACCESS support requires EPICS base 7 or later.

if the QE_PVACCESS_SUPPORT macro is defined _and_  EPICS_VERSION < 7.
If you intend to try building PVA support using base 3.15 and EPICS 4.6 then
you will have to modify the QEPvaCheck.h file.


# <a name="New_Widgets"></a> <span style='color:#006666'>New/Modified Widgets</span>

A new widget QENTTable has been created to specifically support the NTTableData
normative type.

The QEImage widget has been updated to support the NTNDArrayData normative type.
Currently this only supports mono 8-bit pixel images.

All EPICS aware widgets may read/display and/or write using PV Access if the
underlying normative type is suitable.
For example a QELabel can handle PV Access data using NTScalar or NTEnum types,
but cannot display NTTable or NTNDArray data.


# <a name="Protocol_Selection"> </a><span style='color:#006666'>Protocol Selection</span>

All widgets' variable (PV) properties may now be prefixed by __&lt;protocol&gt;://__
in order to specify the protocol to be used. The allowed protocols are __ca://__ for
Channel Access, and when PV Access support included, __pva://__ for PV Access.

The default protocol when no protocol has been specified is Channel Access (__ca://__).
In future releases, the default protocol might become selectable by use of an
environment variable.

The functionality that determines the required protocol strips off the characters
before the first __://__ in the specified variable name and uses this to select
the protocol.
This has the following consequence: if using a PV whose name that actually contains
the character sequence "__://__", then __you must__ explicitly proceeded the PV name with
a protocol specifier.

In this respect, 3.7 is not quite backward compatible with 3.6;
even if the PV Access functionality is not included.
In practice, this should not be a problem unless you have a weird PV naming
convention.

Examples:

    ca://CURRENT_MONITOR   - connect to PV 'CURRENT_MONITOR' using Channel Access.
    pva://CURRENT_MONITOR  - connect to PV 'CURRENT_MONITOR' using PV Access.
    CURRENT_MONITOR        - connect using default protocol, Channel Access.
    xyz://FRED             - unknown protocol - this results in a message on stderr:
                             PV protocol identification failed for: "xyz://FRED"
    ca://WEIRD//:NAME      - connect to PV 'WEIRD//:NAME' using Channel Access.

<font size="-1">Last updated: Thu Sep 26 16:46:20 AEST 2019</font>
<br>
