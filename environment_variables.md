# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt Environment Variables</span>

[Introduction](#Introduction)<br>
[Build Time Environment Variables](#Build)<br>
[Run Time Environment Variables](#Runtime)<br>

# <a name="Introduction"></a><span style='color:#006666'>Introduction</span>

Environment variables influence the behavior both at build time and at run time.
These can be further broken down into thos that affect the EPICS Qt framework in
general and those that explicitly impact the QEGui display manager program.

# <a name="Build"></a><span style='color:#006666'>Build Time Environment Variables</span>

## <a name="Build"></a><span style='color:#006666'>EPICS Qt Framework</span>

### EPICS_BASE (Required)

This defines the location of EPICS base.
For headless builds, this is defined in the configure/RELEASE file, however
when using _qtcreator_ it must be explicitly defined.

### EPICS_HOST_ARCH (Required)

This defines the host architecture, .e.g. linux-x86_64, windows-x64, win32-x86-mingw.

### QE_FRAMEWORK (Required)

This defines the location of the qeframework _installation_ directory,
i.e. the qeframework's <i>top</i> directory.

For headless builds, this is defined in the configure/RELEASE file, however when
using _qtcreator_ it must be explicitly defined.

When using _qtcreator_ , this must be defined for qeframework clients such as the
qeplugin.pro and QEGuiApp.pro projects, but need not be defined for the framework
itself.
See note on QE_TARGET_DIR below.

### ACAI (Required for EPICS Qt 3.7 or later)

This defines the location of the acai _top_ directory.

For headless builds, this is defined in the qeframework's configure/RELEASE file,
however when using _qtcreator_ it must be defined explicitly.

### QWT_INCLUDE_PATH (Required)

This defines the location of the QWT header files. Typically this is:

    /usr/include/qwt

on Linux.

### QWT_ROOT (Optional)

If this variable is not defined, the default location of QWT library is used.
If defined then this is used to locate the QWT library.

### QE_FFMPEG (Optional)

If you want MPEG support, install FFmpeg and define this environment variable.
This can be defined as anything (we suggest YES) on Linux,
but must point to the FFmpeg directory on Windows.

### QTINC (Optional)

Applicable to Qt5 only, and defines include files needed for QtPrintSupport.

### <a name="QE_PVACCESS_SUPPORT"></a>QE_PVACCESS_SUPPORT (Optional, EPICS Qt 3.7 or later)

For headless builds, this is automatically defined by the qeframeworkSup's Makefile
and is set to YES when EPICS base 7 or later in use and is otherwise set to to NO.
If this is not the desired behavior (e.g. using EPICS 3 plus EPICS 4), then the
Makefile should be modified.

When using qtcreator to make/build the EPICS Qt framework this environment variable
must be set manually.
When not defined or not set to YES, the EPICS Qt Framework will be built to support
the Channel Access protocol only.
If set to YES, the framework will attempt to built to support both the Channel
Access and PV Access protocols.
If set to YES and the EPICS Qt framework is being built against EPICS base 3.16
or earlier, the build will fail:

    protocol/QEPvaCheck.h:49:2: error: #error Including PV ACCESS support requires EPICS base 7 or later.
    If PV ACCESS support not required then unset QE_PVACCESS_SUPPORT environment variable.


See the [Getting Started page](getting_started.html) for more details.

### <a name="ADSUPPORT"></a>ADSUPPORT (Optional)

This defines the location of the Area Detector ADSupport module top directory.
If not required, ADSUPPORT must be unset as it serves both as a flag and location.

For headless builds, this can be defined in the qeframework's configure/RELEASE
file, however when using qtcreator it must be defined explicitly.

The ADSupport module is used to decompress images compressed using the Area
Detector Codec plugin and delivered via a PV Access NTNDArray PV.
The decompression modes supported by the EPICS Qt framework are jpeg, lz4, blosc
and bslz4. If used, __your__ AD support module must be built to support all of
these.

ADSUPPORT need only be defined if QE_PVACCESS_SUPPORT is set to YES, however it
will build/link against the ADSupport module even when QE_PVACCESS_SUPPORT is NO.


### <a name="QE_ARCHAPPL_SUPPORT"></a>QE_ARCHAPPL_SUPPORT (Optional)

When not defined or not set to YES, the QE Framework will only be built to support
the EPICS Channel Archiver.
If set to YES, the framework will be built for both EPICS Channel Access Archive and
the EPICS Archiver Appliance.

See the [Archiver Appliance page](archiver_appliance.html) for more details.

### PROTOBUF_INCLUDE_PATH (Optional)

If you want to build the QE Framework with Archiver Appliance support (QE_ARCHAPPL_SUPPORT=YES),
Google Protocol Buffers have to be installed on the system.
If the directory containing the header files  is not on the standard compiler include path,
its location can be defined using this variable.

An alternative to defining an environment variable is to define this value in
qeframework's configure/CONFIG_SITE file.

### PROTOBUF_LIB_DIR (Optional)

If you want to build the QE Framework with Archiver Appliance support (QE_ARCHAPPL_SUPPORT=YES),
Google Protocol Buffers have to be installed on the system.
If the directory containing the libraries is not on the standard library path,
its location can be defined using this variable.

An alternative to defining an environment variable is to define this value in
qeframework's configure/CONFIG_SITE file.

### QE_TARGET_DIR (Optional/Deprecated)

When not defined, the executables, the libraries and the include files are
installed in to _<top>_/bin, _<top>_/lib and _<top>_/include directories as one would
expect for a regular EPICS module.

However, if this environment variable is defined it specifies the installation
location out-side of the top directory.
If used such that the QEFramework files are installed elsewhere, then QE_FRAMEWORK
must be defined accordingly.

This is a legacy option and we suggest it is not used.

## <a name="Build"></a><span style='color:#006666'>QEGui Display Manager</span>

### QE_CAQTDM (Optional)

If integration with PSI's caQtDM is required, this variable specifies the
location of the caQtDM_Project directory.

### QE_CAQTDM_MAJOR_VERSION (Required if QE_CAQTDM is defined)

This specifies the major version of the caQtDM being used.
Currently, as of November 2019, only version 4 is supported.
We have dropped support for version 3.

### QE_CAQTDM_LIB (Optional)

This provides the location of caQtDM_Lib if not within location specified by QE_CAQTDM.


# <a name="Runtime"></a><span style='color:#006666'>Run Time Environment Variables</span>

These environmnet variables affact all programs/display managers using the EPICS Qt
framework.

## <a name="Build"></a><span style='color:#006666'>EPICS Qt Framework</span>

### QT_PLUGIN_PATH (Required)

This must include _<where-your-epicsqt-is-located>_/qeframework/lib/<epics_host_arch>,
so that qegui (and designer) can load the QEPlugin library and create QEFramework widgets.

Note: the plugin library is located at:   _<where-your-epicsqt-is-located>_/qeframework/lib/<epics_host_arch>/designer

***Note***: the "/designer" suffix ***must not*** be added to the QT_PLUGIN_PATH
definition, this is implicitly added by the Qt plugin loader.
It is a "feature" of the Qt system.

Using an environment variable is the easiest way to do this; there are other ways,
please refer to the Qt documentation.

### PATH and LD_LIBRARY_PATH (Required)

This is OS dependent.
The qegui executable and the EPICS and QEFramework libraries must be must be
on the appropriate paths.

For Linux, the  _-Wl,-rpath_  link flags are used, so LD_LIBRARY_PATH need only
be specified if the libraries are relocated.

On Windows builds, PATH must include %EPIC_BASE%\bin\%EPICS_HOST_ARCH% which is
where the ca.dll and Com.dll files are built; and
{where-your-epicsqt-is-located}\qeframework\lib\%EPICS_HOST_ARCH% which is
where the QEFramework.dll is located.

### QE_UI_PATH (Optional)

This defines alternative/additional paths used when searching for a ui file.
This augments qegui's -u command line option.

### QE_DEFAULT_PROVIDER (Optional)

This defines default provider/protocol used when an expicit protocol is __not__
specified as part of the PV name.
This should be defined as one of "ca" or "pva" (case in-sensitive).

The default default when QE_DEFAULT_PROVIDER is undefined or ill-defined is "ca".

| PV Name | QE_DEFAULT_PROVIDER | Protocol used  |
|:--------|:--------------------|:---------------|
| ca://SOME:PV  | Any           | Channel Access |
| pva://SOME:PV | Any           | PV Access      |
| SOME:PV       |               | Channel Access |
| SOME:PV       | ca or CA      | Channel Access |
| SOME:PV       | pva or PVA    | PV Access      |
| SOME:PV       | error         | Channel Access |


### QE_STYLE_COLOR_NAMES and QE_COLOR_NAMES

These environment variables allow the default alarm colours to be overridden -
this may be particularly useful for colour blind users.

QE_STYLE_COLOR_NAMES defines the background colours to be used for QELabel and
the like, while QE_COLOR_NAMES defines the more solid graphical colours used by
QESimpleShape, QEHistogram etc.

The format of each is a set of colon separated colour names, e.g

    "green:yellow:red:white:blue"

or
    "#00ff00::#ffff00:#ff0000:#ffffff:#0080ff"

or a combination of names and hex values.

The colours specify the colour used for no alarm, minor alarm, major alarm,
invalid and out of service respectively.

If a colour missing, then the default is used, e.g. to only define the invalid
colour to orange, define

    QE_STYLE_COLOR_NAMES as ":::#ffc0a0"

Note: if dark background style colours are selected, then the font colour will
be set to white.

### QE_ARCHIVE_TYPE (Optional)

This specifies the type of archiver from which the epicsQt framework will attempt
to retrieve archived PV values.

Currently supported options are __CA__ for the traditional EPICS Channel Access
Archive and __ARCHAPPL__ for EPICS Archiver Appliance.
If not defined, the default is __CA__.

In order to connect to EPICS Archiver Appliance, the framework needs to be built
with Archiver Appliance support.
See [QE_ARCHAPPL_SUPPORT](#QE_ARCHAPPL_SUPPORT)

### QE_ARCHIVE_LIST (Optional)

This specifies a space separated list of Channel Access archive servers.
In turn each server is specified by a slash ('/') separated host name, port number
and cgi program.
Example:

    "cr01arc01:80/cgi-bin/ArchiveDataServer.cgi cr01arc02:80/cgi-bin/ArchiveDataServer.cgi"

For the Archiver appliance, for format is hostname[:port]/path.
The default port number is 80.
Example:

    "cr01arc04:80/mgmt/bpl/ sr02ir01arc01/mgmt/bpl/"

### QE_ARCHIVE_PATTERN (Optional)

A pattern match applied when extracting PV list from the Channel Access archives.
This can be used to restrict, and hence speed up, the amount of PV meta
ArchiveDataServer retrieved from the archiver.

### QE_STRIPCHART_PREDEFINED_PVS (Optional)

This defines up to ten space separated PV names that are added to the Strip Chart context menu.
If you don't know which PVs to define here, speak to your operators.

Example:

    "SR11BCM01:CURRENT_MONITOR  SR11BCM01:LIFETIME_MONITOR"


### QE_STRIPCHART_MAX_REAL_TIME_POINTS (Optional)

This defines the maximum number of real time or live data points the Strip Chart will store per channel.
Once this number is exceeded, older real time points are dropped.
When not specified, the maximum number of stored points defaults to 400,000.
The smallest value than can be defines is 10,000.
The upper limit is the maximum integer value (2,147,483,647).

### QE_GLOBAL_STYLE_SHEET (Optional)  

This defines a global style that is applied to any application (including designer)
that has loaded at least one epicsQt widget.
The style is applied provided at least one QE widget is included on the form displayed (or being designed).

Running _qegui -h_ provides a nice example of defining a style suitable for
Qt5 to _"fix"_ the way QGroupBox widgets are presented.

### QE_RECORD_FIELD_LIST (Optional)  

This specifies a file that defines or replaces the set of field names associated
with each record type.
The framework already knows about all the record types from EPICS base, most of the
record types from the synApps distribution, together with the AS developed
concat record type and the iTech libera and liberaSignal record types.

Refer to the QEPvProperties widget in the QE_QEGuiAndUserInterfaceDesign documentation for details.


## <span style='color:#006666'>General</span>

Running _qegui -h_ provides further details about each of these environment variables.

As the EPICS Qt framework is a Channel Access client, the values assigned to:

* EPICS_CA_AUTO_ADDR_LIST,
* EPICS_CA_ADDR_LIST,
* EPICS_CA_MAX_ARRAY_BYTES,
* EPICS_CA_SERVER_PORT,
* EPICS_PVA_AUTO_ADDR_LIST,
* EPICS_PVA_ADDR_LIST etc.

can affect the operation of this program.
Please refer to EPICS R3.14 Channel Access Reference Manual for details.

## <a name="Build"></a><span style='color:#006666'>QEGui Display Manager</span>

These environmnet variables affact QEGui only.
They will not affect other bespoke display managers using the EPICS Qt framework.

With the exception of --help and --version, any QEGui long option may now also be
specified by a corresponding environment variable.

This environment variable is the long option name without the leading --,
converted to upper case and prefixed by "QEGUI_".

For example, on Linux, the following are equivalent:

    export QEGUI_ADJUST_SCALE="120"
    export QEGUI_DISABLE_AUTOSAVE="YES"
    qegui

and

    qegui --adjust_scale=200  --disable_autosave


If both an environment variable and command line option are specified, the command
line option takes precedence.
Run qegui -h to get a complete list of long options.

### QEGUI_CAQTDM_CONTEXT_MENU

When caQtDm is integrated into QEGui, this environment variable controls whether
the caQtDm widgets use their native context menu or the EPICS Qt standard
context menu. Set this variable to "1", "TRUE" or "YES" to select this feature.


<font size="-1">Last updated: Sun May 21 13:39:50 2023</font>
<br>
