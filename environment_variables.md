<br/>
# <span style='color:#006666'>EPICS Qt Environment Variables</span>

Environment variables influence the behavior both at build time and at run time.

## <span style='color:#006666'>Build Time Environment Variables</span>

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

When using _qtcreator_ , this must be defined for qeframework clients such as the qeplugin.pro and
QEGuiApp.pro projects, but need not be defined for the framework itself.
See note on QE_TARGET_DIR below.

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

### QE_CAQTDM (Optional)

If integration with PSI's caQtDM is required, this variable specifies the
location of the caQtDM_Project directory.

### QE_CAQTDM_LIB (Optional)

This provides the location of caQtDM_Lib if not within location specified by QE_CAQTDM.

### QTINC (Optional)

Applicable to Qt5 only, and defines include files needed for QtPrintSupport.

### QE_ARCHAPPL_SUPPORT (Optional)

When not defined or not set to YES, the QE Framework will only be built to support the EPICS Channel Archiver.
If set to YES, the framework will be built for both EPICS Channel Access Archive and
the EPICS Archiver Appliance.

See the [Archiver Appliance page](archiver_appliance.html) for more details.

### PROTOBUF_LIBS_DIR (Optional)

If you want to build the QE Framework with Archiver Appliance support (QE_ARCHAPPL_SUPPORT=YES),
Google Protocol Buffers have to be installed on the system.
If the directory containing the libraries is not on the standard library path,
its location can be defined using this variable.

### QE_TARGET_DIR (Optional/Deprecated)

When not defined, the executables, the libraries and the include files are
installed in to _<top>_/bin, _<top>_/lib and _<top>_/include directories as one would
expect for a regular EPICS module.

However, if this environment variable is defined it specifies the installation
location out-side of the top directory.
If used such that the QEFramework files are installed elsewhere, then QE_FRAMEWORK
must be defined accordingly.

This is a legacy option and we suggest it is not used.


## <span style='color:#006666'>Run Time Environment Variables</span>

### QT_PLUGIN_PATH (Required)

This must include _<where-your-epicsqt-is-located>_/qeframework/lib/<epics_host_arch>,
so that qegui (and designer) may load the QEPlugin library and create QEFramework widgets.

Note: the plugin library is located at:   _<where-your-epicsqt-is-located>_/qeframework/lib/<epics_host_arch>/designer

Using an environment variable is the easiest way to do this; there are other ways,
please refer to the Qt documentation.

### PATH and LD_LIBRARY_PATH (Required)

This is OS dependent.
The qegui executable and the EPICS and QEFramework libraries must be must be
on the appropriate paths.

For Linux, the  _-Wl,-rpath_  link flags are used, so LD_LIBRARY_PATH need only
be specified if the libraries are relocated.

On Windows builds, PATH must include %EPIC_BASE%\bin\%EPICS_HOST_ARCH% which is
where the ca.dll and Com.dll files are built;  and
_<where-your-epicsqt-is-located>\qeframework\lib\%EPICS_HOST_ARCH% which is
where the QEFramework.dll is located.

### QE_UI_PATH (Optional)

This defines alternative/additional paths used when searching for a ui file.
This augments qegui's -u command line option.

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

For the Archiver appliance, for format is hostname/path. Example:

    "cr01arc04/mgmt/bpl/"

### QE_ARCHIVE_PATTERN (Optional)

A pattern match applied when extracting PV list from the archives.
This can be used to restrict, and hence speed up, the amount of PV meta ArchiveDataServerretrieved from the archiver.

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
* EPICS_CA_SERVER_PORT etc.

can affect the operation of this program.
Please refer to EPICS R3.14 Channel Access Reference Manual for details.


<font size="-2">Last updated: Sat Dec 8 15:35:17 AEDT 2018</font>
<br>
