# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.7.4](#r3.7.4)<br>
[r3.7.3](#r3.7.3)<br>
[r3.7.2](#r3.7.2)<br>
[r3.7.1](#r3.7.1)<br>
[r3.6.4](#r3.6.4)<br>
[r3.6.3](#r3.6.3)<br>
[r3.6.2](#r3.6.2)<br>
[r3.6.1](#r3.6.1)<br>
[r3.5.3](#r3.5.3)<br>
[r3.5.2](#r3.5.2)<br>
[r3.5.1](#r3.5.1)<br>
[r3.4.3](#r3.4.3)<br>
[r3.4.2](#r3.4.2)<br>
[Earlier Releases](#Earlier_Releases)


# <a name="r3.7.4"></a><span style='color:#006666'>r3.7.4</span>

Expected release date: 8th August 2020.

# <a name="r3.7.3"></a><span style='color:#006666'>r3.7.3</span>

Release date: 16th April 2020.

The main feature of this release is is a rework of the QEPlot widget, the
introduction of a new QEDateTime widget, updates to cater for latest protobuf
version and how the archapplDataSup support library is built, and PVA image
decompression.

## <span style='color:#666666'>qeframework</span>

#### General

When a QE_UI_PATH variable directory ended ..., the framework used to search all
sub-directories for the given file name.
The search mechanism has been updated to include the top level directory itself
when ... used.

#### QEPlot

The QEPlot widget has undergone a significant upgrade.
The new features are:
 - Upto 8 (was 4) PV traces per widget.
 - The line thickness for each trace can be specified (new porpeties traceWidth*__N__*)
 - the plotted x range can now to be specified (new properties xFirst and xLast,
   defaults are -1e6 and +1e6)
 - It handles disconnects and invalid values as per the QEStripChart.
 - Allows multiple PV names dropped/pasted onto the widget.
 - It now sets default variableNameAsToopTip property to true;
   note: this is a slight backward incompatibility.
 - Added basic archive back-fill capability either specified as
   property, i.e. automatic back-fill when set true, and/or via context menu request.
 - Introduced new property, selectedYAxis, to allow Y axis is to be plotted on
   the Left (default) or the Right side of the widget.

Under-the-covers, QEPlot now uses QEGraphic (as opposed to qwt directly).
We also updated the QEPlot documentation and split into a separate document file.

#### QEScalarHistogram and QEWaveformHistogram

These widgets now inherit directly from QEHistogram, as opposed to inheriting
from QEFrame and containing a QEHistogram instance.
For the most part, this change has no impact, other than when opening a ui file
that contains a QEScalarHistogram or QEWaveformHistogram in designer, you will
get a warning message like:

    The file contains a custom widget 'QEWaveformHistogram' whose base class
    (QEFrame) differs from the current entry in the widget database
    (QEHistogram). The widget database is left unchanged.

The only impact is if you have written bespoke display manager and/or your own
plugin that contains a QEScalarHistogram or QEWaveformHistogram widget.
For the base class QEHistogram, the set/getPrecsion functions associated with
the axis precision property have been re-named to  set/getAxisPrecision.
These are not only more precise function named, bit also avoid a name
clash/ambiguity due to the inheritance restructuring.

#### QEDateTime

QEDateTime is a new non-EPICS aware widget that allows the current date and
time to be displayed on a ui form.
The format is controlled using the dateTimeFormat property.
The time zone can be either local time or UTC (essentially GMT) and appended
to the displayed date time if needed.

#### archapplDataSup

Added a configuration variable to enable (default) or disable c++11 support for
archapplDataSup build.

Updated archapplDataSup/src Makefile to more closely follow the standard EPICS
Makefile paradigm.
Note: A consequence of this is that on Windows, the generated archapplData.DLL
is now installed in the bin/<epics_host_arch> folder as opposed to the
lib/<epics_host_arch> folder.

The Makefile has also been modified to use PROTOBUF_INCLUDE_PATH environment
variable iff defined, and add related explanation note to CONFIG_SITE.

Modified Archive Appliance interface module to add support for long int types.

#### PVA Image Decompression (QENTNDArrayData)

When ADSUPPORT environment variable defined or specified in the qeframwork's
configuration RELEASE file, the QENTNDArrayData variant type now provides a
a means to decompress images that have been compressed using Area Detector's
codec plugin.
The codecs supported are jpeg, blosc, lz4, and bslz4.
The decompression is performed used function out of the ADSupport module.

QEImage has been updated to request decompression of PVA images.

#### QEPvProperties

Added field description column to the PV properties widget.
The internal record field list configuration file has been updated to include
field description for most record type (derived for the each record's dbd file).

Updated the QEPvProperties widget to handle the re-scaling of column widths as
more-or-less expected, and clear all columns, not just the field name column
when a new PV selected.

#### QECorrelation

Allow smaller sample time interval on the QECorrelation widget.
The minimum value has been reduced from 0.2sec to 0.05 sec.

#### QEPushButton, QERadioButton, QECheckBox

For enums values to variant conversion, when the format property is defined as
Default, the conversion now accept integer values as well as enumeration strings.
We check for enumeration string values first, and then integer values.
This similar behavior to caput.
Note: this excludes local enumeration (for now).

Extend the options for the disablesRecordPolocy property (was "ignore" and
"grayout") to include a "disable" option.
This disables the widget when the PV status indicated disabled.
We modified whole underlying mechanism to use the PV's STATus value as opposed
to subscribing for DISA and DISV fields which are not monitored.
The benefits are less PVs, and works for non IOC record PVs as well.

#### QEArchiveStatus

The QEArchiveStatus widget has been modified to add an update button to manually
request PV information and meta data from the defined archives.
This is in addition to the automatic once-a-day update.

Also use a grid layout for the archive status widget, and increase the maximum
number of allowed archives from 20 to 40.

#### QEStripChart statistics

Take special action when units are /s, /sec, /min and /Hr when determining the
units for the area under curve integration.
This was cribbed directly from the Delphi StripChart.

#### QEStripChart/QEPvLoadSave time selection

The associated time selection dialogs for both these widgets have been updated
to make minimum calendar widget sizes a bit larger, and also make the widgets
stretch as the dialog forms are stretched.

#### QEGraphic

Perform dynamic axis scaling on both left and right axis.
Be explicit with use of QwtPlot::yLeft axis selection instead of relying
on the axis argument default value, this will only impact users building against
the QEFramework library, however this changes does not impact used of the QEPlugin
library.


## <span style='color:#666666'>qegui</span>

#### Windows position

Ensure qegui first's form on Windows is in a sensible location for the case when
the taskbar is located at top of screen.

#### Menu

Added a histogram option to the default qegui menu.
This opens an from holding an empty QEWaveformHistogram widget onto which PV
names can be pasted or onto which EPICS aware widgets can be dragged and dropped.
The WaveformHistogram.ui form updated updated to reflect new widget inheritance.

#### msi configuration file

Update the wxs file for 3.7.3 release.
Added qeReadArchive as part of the generated msi file.
Created a simple candle + light convenience bat script.

## <span style='color:#666666'>qeBinaries</span>

New 3.7.3 msi file available.

# <a name="r3.7.2"></a><span style='color:#006666'>r3.7.2</span>

Release date: 11th November 2019.

The main feature of this release is the revamping of the caQtDm integration.
Please see [caQtDM integration documentation](caqtdm_integration.html) for details.
The other changes are itemised below.

## <span style='color:#666666'>qeframework</span>

#### QEStripChart

Setting QEStripChart PV variable names in designer now works as expected.

When calculating distribution statistics, avoid the potential divide by zero and
subsequent segmentation fault.

There have been three additional preset PV scaling options to the strip chart.
These are re-scale plotted data to upper, lower and centre third of the chart

Sorted out font on StripChart toolbar (especially when global style sheet is
being applied).
Also now apply a consistant formatting for zero values.

This widget has been modified to include markup settings when saveing and/or
restoring configuration data.

#### QEMenuButton

Updated the setup dialog to introduce a 3:5 stretch ratio for each side of the dialog.

The default name is now _name..._ (as opposed to 'X' plus number).

#### QEScalarHistogram and QEWaveformHistogram

Added readout format properties to scalar and waveform histogram widgets.
These are a subset of the usual display format properties.

#### QEImage

Made QEImage more robust with respect to dynamic scaling.

#### PV Access

Updated PV Access related functionality for base-7.0.3.
Now process precision and have dropped using format (form is still to be done).
The hysteresis is alwayus extracted as a byte from alarmValue.
Introduced opaque variant type for unknown/unhandled PVA types.

#### general

Removed use of deprecated functions.

#### documentation

Reworked QBitStatus/QEBitStatus documentation, and delivered as a separate document.

Removed the old readme.txt file and Updated the README.md file.

## <span style='color:#666666'>QEGui</span>

#### caQtDM

Support for caQtDM integration has been revampled and we now support V4.
Please see the [caQtDM integration](caqtdm_integration.html) page for details.
Note: caQtDM integration is still optional.

Running

    qegui -v

reveals if caQtDM integration has been included.

#### Dialogs

The various dialogs (about, saveConfig, restoreConfig and manageConfig) now use
QEDialog so that the dialog itself is located in the middle of the relavent form.
Ensure we save and relocate to the intial startup directory when using config
related dialogs.

#### designer

When opening designer, QEGui used to check for designer-qt4 program and then
the designer program.
Now we just attempt to callup designer.
Qt 4.8 users should fake designer to call designer-qt4.

#### structure

The QEGui files have been restructured.
The UISamples folder have beem moved from the qeguiApp/project directory to own
top level uiSamples directory.
The header files have been colocated with corresponding .cpp files in the
qeguiApp/project/src folder.

## <span style='color:#666666'>qeBinaries</span>

New 3.7.2 msi and rpm files available.

The new msi file includes a wrapper script for qegui and designer, so that we
don't clobber the 'global' QT_PLUGIN_PATH environment variable which can then
break other programs.

# <a name="r3.7.1"></a><span style='color:#006666'>r3.7.1</span>

Formal release date: 29th August 2019.

## <span style='color:#666666'>general</span>

The most significant change to the EPICS Qt framework going from the 3.6 releases
to the 3.7 release series is that the framework is now capable of supporting the
PV Access protocol for some of the normative types available via PV Access.
For NTNDArray type only 8bit mono images are currently supported, and will be
fixed for release 3.7.2

Refer to the [pv access](pv_access.html) page for details of this update.
__NOTE:__ this includes important build information.

The more "mundane" changes since the previous release are detailed below.

## <span style='color:#666666'>documentation</span>

The unwieldy large QE_QEGuiAndUserInterfaceDesign document has been made more
manageable by extracting widget specific information into another document,
namely: QEWidgetSpecifications.
This in turn may be further split in future releases, and the documentation for
any new widgets such as QEDistibution and QEFormStateChange will have their own
standalone document.

## <span style='color:#666666'>qtepics.github.io</span>

The markdown files within this depo. have under gone a restructure and general
renewal. The large index.md has been broken up into a number of smaller, topic
related and more manageable files.

Within the qtepics.github.io repository in the tools directory is the
__qe_git_test_build__ script that is used to check build-ability after each
commit or set of commits to github.
For Linux users, this could be used as the basis to create your own build script
suited to meet your own particular needs.

## <span style='color:#666666'>qeBinaries</span>

In the qeBinaries repository there are the following files:

###### EPICS_Qt_Installer_3_7_1.msi

This installs qegui, designer and the required libraries.
You also get a copy of caget and caput.
This does not include the PV Access functionality as it built against base-3.15,
nor does it include the ffMpeg capability.

###### epicsQt-3.7.1-el7.x86_64.rpm

This rpm installs qegui, designer and the required libraries.
It was assembled and tested on a CentOS 7 box.
It may work on other distros that use the YUM package manager.

## <span style='color:#666666'>qeframework</span>

#### QEDistrubtion

This is a new widget that can monitor a single PV and provides statistical information
about the value i.e: min, max, mean and standard deviation.
It also provides a graphical representation of this of this data.
Please refer to the QEDistrubtion documentation (out of the qeframework repository).

#### QEFormStateChange

This is a new widget that provides the means for automatic actions to take place
when a form is opened or closed.
This is akin to having QEPushButton on the form which is automatically clicked
when the form is opened and another when it is closed.
The available actions are write a value to a PV and/or invoke a local script.
It differs from a QEPushButton in that it cannot open another ui file.
Please refer to the QEFormStateChange documentation.

#### QENTTable

This is a new widget specifically for the NTTable normative type.
Please refer to the QEWidgetSpecifications documentation.

#### macro Expansion

This has been modified to avoid an annoying feature where defining a priority
substitution in terms of an exiting substitution of the same name failed.
So now, you can do something like:

    P=$(P)ABC

and it will expanded as expected.

Also added a quick 'nothing-to-do' test in the substitute function.

#### writeNow functions

Many control widgets have a writeNow function which causes the current value
to be written to the PV.
These functions are now public slots such that the functionality can be triggered
by a signal from another widget.

#### Alarm handling

When processing Archive Appliance data, the alarm severity was erroneously set as
status and the status set as severity.
This has now been now fixed.

QCaAlarmInfo's severityName function now includes the Channel Access archive
severity names as well.

Modified the QCaAlarmInfo::isInAlarm function to test severity as opposed to status.

#### QEAnalogProgressBar

Updated QEAnalogProgressBar to handle alarm colours more consistantly.
Maid some functions in QEAnalogIndicator virtual and protected to help do this.

#### QEGroupBox, QRadioGroup and QERadioGroup

These widgets will now interpret a property title of "-" as a blank title.
Previously setting a title blank would result in the original default title,
e.g. "QRadioButton".

#### QEPushButton, QECheckBox and QERadioButton

Added a NoUpdate choice to the updateOption property for completeness for when
the subscribe property is set true.
This combination to allows alarm sensitivity without changing the button text.

#### QEPvLoadSave

This now provide summary of the number equal, not equal and n/a values for each group.
This is shown as a three number tuple in the delta column.

Ensure action complete status set correctly when extracting data.
This ensures the abort results are properly presented to the user.

#### QEPlotter

Added a normal/reverse video property to the QEPlotter, this replicates the
QEStripChart look and feel.

#### QEScaling

QEScaling::getWidgetScaling function modified to take a const widget reference.
Also, removed debug/info statements from scaling module, they served no useful
purpose.

#### QESimpleShape/QSimpleShape

The QESimpleShape widget now copies both variable names when using the context
menu copyVariable option and when dragging on to anything that accepts textual
drops.

QESimpleShape modified to honor the "when in alarm state" option for both main
and edge colours.
User specified colours, when not in alarm, should be readily distinguishable from
alarm colours if/when this option is used.

QSimpleShape - added some new shapes: star, cross, plus and pentagon.
The cross and plus shapes are modify-able by the percentSize property.

Also created a shape selection slot function, which takes an int parameter.
This means that shape itself may be controlled by a PV, possibly via a QELink
or QECalcout widget.
We will endeavor to keep the int value to shape mapping contestant if/when new
shapes are added.

#### QEStripChart

The calculation capability and been extended to allow the calculation to be applied
to data retrieved from the archive and to previously acquired live data.

The QEStripChart's generate statistics functionality now includes a graphical
presentation similar to QEDistribution.

#### QEPvProperties

The Ch1, Ch2, Ch3 and Ch4 fields have been added to the iTech liberaSignal record
type's field list specification.
Note: the actual existence of some of the liberaSignal fields are device type
dependent.

#### QEMenuButton

Added an icon and iconSize properties - these are passed to and handled by the
internal QPushButton widget.
Also changed the hint size height to match that of QPushButton.

Explicitly call connectChannel, needed for new qcaobject::QCaObject objects.

#### persistanceManager

The persistanceManager has been extended to support addValue/getValue for QColor
type values.
This is only relevant if you have created your own widgets.

#### applicationLauncher

The function parameters are now const where applicable.
Also de-inlined the inline functions in order to de-clutter the header file.


## <span style='color:#666666'>qegui</span>

Integrated the QEDistibution widget into qegui, there is a built in form that
contains a single instance of the widget.
It is accessable from the menu:   __Tools | PV Distribution...__

# <a name="r3.6.4"></a><span style='color:#006666'>r3.6.4</span>

Release date: 4th February 2019.

Very few changes since release 3.6.3.
This release is essentially a "stake-in-the-ground" before release 3.7.1.
The main changes in this release are detailed below.
Please see the GitHub log for details.

## <span style='color:#666666'>qeframework</span>

#### QELog

The QELog module now stores upto 1000 log messages prior to the creation of a QELog widget.
A QELog widget may now be optionally flag as master, and as such it will retrieve
the stored log messages and display them to the user.
In this way, log messages created before the creation of a QELog widget are not lost.

Note: there can effectively only be one master QELog. The QELog built into qegui
has been set as master.

#### QEStripchart

When writing a PV trace to file, removed the extra "." inserted into the date
format (is this a Qt5.10 thing?).
Also use chart default directory for save file dialog.
Change the format on the time duration dialog to be HH:MM:SS where the HH is 24 hour.

#### QEEnvironmentVariables

Fixed the interpretation of false boolean environment variable values, and
also added YES and NO options.

## <span style='color:#666666'>qegui</span>

#### Parameters

Introduce long parameter options and allow use of adaptation_parameters_file.ini
file and/or environment variables.
This means that

    export QEGUI_ADJUST_SCALE=200 ; qegui

and

    qegui --adjust_scale=200

are eqivilent.
Run qegui -h for long name details.

Also just ignore unknown options - these may now be accessed by bespoke plugins.

#### Inbuilt QELog widget

Inbuilt qegui message log has the master attribute set.

#### caQtDM

Refactor caQtDM code into to separate interface module.
This work is a prelude to verion 4 integration.

## <span style='color:#666666'>qtepics.github.io</span>

All documentation upgraded to markdown.
Cleaner, can be maintained by simple text editor, and no more buggy translation
from .docx to .html

# <a name="r3.6.3"></a><span style='color:#006666'>r3.6.3</span>

Release date: 18th December 2018.

The main changes in this release are:

## <span style='color:#666666'>qeframework</span>

#### Macro Expansion

The macro expansion functionality has been enhanced.
It now does multiple passes (up to ten);
this allows macro to be defined in terms of other macros.

#### QEComboBox and QESpinBox

The default focus policy has been changed from WheelFocus to ClickFocus.
These widgets now ignore wheel events  when the widget does not have focus.
This stops unexpected PV writes when the wheel is (inadvertently) rotated.

#### QECorrelation (new)

The QECorrelation widget allows two scaler to be correleated and the result
presented to the user graphically together with the calculated correlation factor.
The user may select, at design time and/or run time, the sample interval and
the maximum number of points to be retained for the correlation.

#### QEStripChart

The delta time precision is now greater (up-to to 3) for shorter view durations.

We now ensure the graphic context menu "box" does not override the "line"
markup selection.

#### QEPvProperties

The acalcout record and associated fields have been added to the inbuilt
record/field resource file.

#### Archiver

When connecting to the Archiver Appliance, we now check if the URL
(specified by QE_ARCHIVE_LIST) ends with '/', and if it doesn't we add it.

## <span style='color:#666666'>qegui</span>

#### PV Correlation

Make new QECorrelation widget has been made available in qegui via menu:

    Tools | PV Correlation...


#### Version information

Update qegui -v to output library info:

    $ qegui -v
    QEGui version:     3.6.3 (Production)  Dec 13 2018 18:02:24 (using QT 5.10.0)
    Framework version: 3.6.3 (Production)  Dec 13 2018 17:58:44 (using QT 5.10.0)
    Framework attributes: FFMPEG video streaming, Archiver Appliance
    Support packages:  EPICS 3.15.5 and QWT 6.1.3
    Library path: /opt/Qt5.10/5.10.0/gcc_64/lib
    Plugin path:  /opt/Qt5.10/5.10.0/gcc_64/plugins

#### rpm constructor script

Created an epicsQt linux rpm constructor script.
The rpm will include the required Qt, EPICS, QWT and epicsQt libraries and plugins
together with epicsQt and designer.

Note: Intended for use by the developers, but feel free to experiment with it.

## <span style='color:#666666'>binaries</span>

A new version of the msi installation file for Windows has been uploaded.


# <a name="r3.6.2"></a><span style='color:#006666'>r3.6.2</span>

Release date: 8th October 2018.

The main changes in this release are:

## <span style='color:#666666'>qegui</span>

When outputting version info qegui now outputs the QE framework build option attributes , e.g.

    $ qegui -v
    QEGui version: 3.6.2 (Development) Oct 10 2018 18:38:19 (using QT 5.10.0)
    Framework version: 3.6.2 (Development) Oct 10 2018 18:35:52 (using QT 5.10.0)
    Framework attributes: FFMPEG video streaming, Archiver Appliance
    Support packages: EPICS 3.15.5 and QWT 6.1.3

This information is also shown on the help about dialog.

Added a nice qegui icon: for windows executable and QT versions 5 or higher only.

New windows are now relocated close to the opening window.
While Qt's habit of opening new windows a spread out as possible was sensible
for a single "small" monitor, it is not sensible when running on system with
two or even four or more "large" monitors.

##  <span style='color:#666666'>qeframework</span>

The significant changes for this release are:

#### QEPeridic
This widget has been re-worked to:

* Use new names and abbreviations for elements 113 to 118, i.e. uses:
Nihonium, Flerovium, Moscovium, Livermorium, Tennessine, Oganesson in lieu of
Ununtrium, Ununquadium, Ununpentium, Ununhexium, Ununseptium, Ununoctium;

* Added slots/signals to accept/emit the atomic number (int type) to complement
the existing element/abbreviation (QString type) slots and signals;

* Element layout reorganized w.r.t. the Lanthanides and Actinides;

* Both run time and design time dialogs now stretch and resize;

* Optional run time element selection button colorisation available via widget property; and

* Set the Thallium abbreviation to 'Tl' (and not 'Ti') - which instigated this whole update.


#### QEImage
The ellipse markup now take an optional ellipse rotation PV.
The value of this PV defines the clockwise rotation of the ellipse in degrees.

#### QEPushButton, QERadioButton and QECheckBox
The update option now allows any combination of Text, Icon and/or State.

#### QEStripChart
The save/restore configuration now also saves colour, plot mode, the draw mode,
the archive retrieval mode and time mode. It now also allows up to 400K (up from 40K)
live data points to be stored and plotted.
This may be extended/restricted by defining the QE_STRIPCHART_MAX_REAL_TIME_POINTS
environment variable.

#### QESimpleShape
This widget now no longer complains when being used to monitor the alarm state
of a non-numeric PV.

#### QENumericEdit
The "under-the-covers" value and the emitted values now exactly reflects the displayed value.

#### QENumericEdit
The value written to the PV now exactly reflects the displayed value.

#### QEHistogram and derived widgets
These now allow the specification and selection of a secondary background colour
and banding size - this allows histogram entries to be "grouped".

#### QELCDNumber (new)

This only suitable for numeric PVs as it uses the QLCDNumber widget under the covers.

## <span style='color:#666666'>binaries</span>

We have added an msi installation file for Windows - the installation includes:

* EPICS base ca and Com libraries;
* QE framework and plugin libraries;
* QEGui and designer executables; plus
* caget.exe, caput.exe and caMonitor.exe

It does not include FFMPEG support, but does include Archiver Appliance support.
It has been verified on both Windows 7 and 10 (it failed on an old Windows XP system).

All compilation performed using mingw 32-bit compiler.

Files are installed in "C:\Program Files (x86)\Australian Synchrotron\EPICS_QT_3_6_2\..."

QEGui and designer desktop icons are created.
The PATH environment variable is modified and system environment variables are created for:

* EPICS_CA_AUTO_ADDR_LIST
* EPICS_CA_MAX_ARRAY_BYTES
* QE_FRAMEWORK
* QE_ARCHIVE_TYPE

if they do not already exist.



# <a name="r3.6.1"></a><span style='color:#006666'>r3.6.1</span>

Release date: 20th April 2018.

The main change for this release is the inclusion of Archiver Appliance support.
See the [Archiver Appliance page](archiver_appliance.html) for more details.



# <a name="r3.5.3"></a><span style='color:#006666'>r3.5.3</span>

Release date: 16th April 2018.

The main changes in this release are:

## <span style='color:#666666'>qegui</span>

In the standard File menu, there are two new menu items. These are:

* List PV Names...<br>
This will offer the user a Save File dialog and if a file nominated, then it
will write all the PV names used on the current window to the nominated file;
and

* Screen Capture...<br>
This will offer the user a Save File dialog and if a file nominated, then it
will perform a screen scrape of the the window and write the image to the nominated
file (png format).

## <span style='color:#666666'>qeframework</span>

#### QEPlotter
The QEPlotter now checks for and does not attempt to plot NaN and +/- Inf numbers.
The widgits minimum and maximum X and Y range values are now exposed as properties.

#### QEStripChart
The QEStripChart widget modified to provide an expression evaluation capability.
This is similar to that already provided by QEPlotter.

#### QEImage
Reorganized the how ffmpeg functionality is/is not included into QEImage.
No functional change per se but does now avoids a seg-fault in designer.

#### QEUtilities
QEUtilities includes the functionality for List PV names and do a Screen Capture,
so this is now available to non-qegui Qt applications.

#### elementsRequired property
For single variable widgets such as QELabel, QESimpleShape etc., added an elementsRequired
integer property in order to limit the number of requested elements from an array PV.
The default value is 0 which is read as subscribe for all elements.
While restricting the number of elements subscribed for is sensible for monitors
such as QESimpleShape and QEBitStatus (the reason behind this change) care should
be taken when using it with control widgets.

#### disconnected graphical widgets
Make disconnected graphical widgets unambiguously greyer. Modify QBitStatus to use
the same washed-out colours as QESimpleShape.

#### disconnected signals
Issue the disconnected signals immediately on subscribe - then await connection.
This ensures widgets look disconnected asap if the associated PV does not exist.

#### font change events
Updated/added font change event in the event filter (as opposed to overriding the
fontChange function which isn't virtual in Qt5) to these widgets: QEHistogram,
QEMenuButton, QNumericEdit, QRadioGroup, QERadioGroup and QETable.
This widgets now respond property to font changes within designer and at run time.

#### QELabel, QESubstitutedLabel
For QLabel based widgets (QELabel, QESubstitutedLabel) widgets now have a light gray
colour style, both within designer and at run time (by setting the defaultStyle property).
This colour is very close to, but sufficiently different from the standard form
background colour, to be unobtrusive and yet help visualisation when designing
forms and at run time.

For alarm sensitive labels, this will be superseded by the standard alarm colour
when displaying the form at run time.

Note: For non alarm sensitive QELabels on forms with a non standard background colour,
you will have to clear the defaultStyle property.

#### QEDescriptionLabel (new)
The QEDescriptionLabel widget directly inherits from QELabel.
There is no extra functionality; however the widget has different default property
values (smaller font, not alarm sensitive, clear style-sheet, no indentation).
It is suitable/intended for displaying descriptive text, typically from the .DESC
field of a record.

#### QECalcout (new)
The QECalcout widget provides a calcout record-like widget.
So much so that where applicable the property names have been chosen to match the calcout record.
This widget can be used instead of and/or to complement the QELink widget.
This widget has no PV variables of its own.
The inputs, A to L, must be provided either by signals from other (QE) widgets or
preset as 'constants' using the a to l properties.
Under the covers, this widget uses the same calculation engine as the calc/calcout record.

#### QEPVLoadSave
The QEPVLoadSave widget has been updated to show not only the snap-shot/load/save
value, but also show the live value and difference value.

#### QEPvProperties
The built in list of records and associated record fields used by the QEPvProperties
widget has been updated to reflect base 3.15.5.

#### documentation
Updated the support documentation.



# <a name="r3.5.2"></a><span style='color:#006666'>r3.5.2</span>

Release date: 11th November 2017.

The main changes for this release are:

## <span style='color:#666666'>qegui</span>

Above and beyond any application scaling (see option -a in documentation and/or qegui -h),
qegui will now scale an individual window in response to a number of control+key
combinations in a similar fashion to many browsers and other programs.
The control+key actions are:

* control+plus-key or (control+equal-key): increase scaling by 2%;
* control+minus-key: decrease scaling by 2%; and
* control+zero-key: reset scaling.

## <span style='color:#666666'>qeframework</span>

#### mingw architecture
The framework project file now automatically defines the \_MINGW macro if the
EPICS host architecture is "win32-x86-mingw" or "windows-x64-mingw".

#### QEPvProperties
The QEPvProperties' context menu now provides a process record option (this writes
1 to the record's PROC field) and now provides consistent context menu even when
clicking on the value field within this widget.

#### QEPlotter
The QEPlotter widget has been updated so that it does not attempt to plot data if
the associated array PV has an invalid severity.
In now also clears any old plot data when establishing a new channel connection.

#### QEMenuButton
Incorporated Bob Gunion's change to the QEMenuButton which has modified to introduce
a labelText property to allow the button's text to be set and also to honor the
widget's font setting.

#### dbValueChanged
All single PV widgets now emit a parameter-less dbValueChanged signal in addition
to various other signals.

#### units
The units (typically specified in the EGU field) for a DBF_CHAR type has now available
to the QELabel and other widget type.
String formatting has modified to ignore the units when a DBF_CHAR array PV is
interpreted as a long string.

#### QEPvLoadSave
The way in which QEPvLoadSave widget handles array PVs and enumeration PVs has
been improved.



# <a name="r3.5.1"></a><span style='color:#006666'>r3.5.1</span>

Release date: 9th July 2017.

The main change for this release is that the QEPlugin library has been split the
into two distinct libraries which are:

 * QEFramework - the functional library which contains the widgets themselves
 together with support functionality. qegui and any other bespoke display managers
 programs will need to link against this library.

* QEPlugin - strictly the widget plugin library usable by any application using
the ui loader, such as qegui and designer.
The QEPlugin library is dependent on the QEFramework library.

Both libraries are part of the the qeframework repository, with QEFramework built
from the qeframeworkSup application and the QEPlugin library built from the new
qepluginApp application.
Using linux-x86_64 as an example EPICS host architecture the libraries are built and installed into:

    <top>/lib/linux-x86_64/libQEFramework.so
    <top>/lib/linux-x86_64/designer/libQEPlugin.so

This means that QT_PLUGIN_PATH need not change as the plugin library is installed
into a directory called designer (as was previously "faked" by use of a symbolic link).
When linking application building using the framework library need to reference
QEFramework as opposed to QEPlugin.

Because the qepluginApp build uses the qeframeworkSup, the following has been added
to the qeframework configure/RELEASE file:

    QE_FRAMEWORK=...

This needs to be configured to point to the qeframeworkSup top directory.
Unfortunately one cannot say QE_FRAMEWORK=$(TOP).
Please see comments in configure/RELEASE.

There have also been a number of other changes to qegui and qegramework since
release r3.4.3 as outlined below.
Apart from referencing the QEFramework library there have been no other changes
to qeByteArrayTest, qeMonitor, qeReadArchive etc.

## <span style='color:#666666'>qegui</span>

For windows - if the main window is off screen, then re-position windows to position (0,0).

Introduced an independent font scaling capability.
Use the -f options.
Run qegui -h for details.

## <span style='color:#666666'>qeframework</span>

#### QEConfiguredLayout, QEFileBrowser, QELog, QERecipe, QEScript

Modified QEConfiguredLayout, QEFileBrowser, QELog, QERecipe, QEScript to scope
local enumeration definitions so that they don't clash if two or more headers
are used in same compilation unit.

#### FFmpeg

mpeg - more version related conditional compilation.

#### framework project file
Added $$(EPICS_BASE)/include/compiler/msvc to the include path and for windows
defined EPICS_CALL_DLL when compiling the QE framework.

#### plugin icons
Updated some of the EPICS aware widget designer icons to be distinct from non
EPICS aware counter parts.

#### QEPvProperties
QEPvProperties - ensured correct field referenced when fields are sorted.
Also added RMOD, ADEL, MDEL, ALST, MLST and SYNC fields to the built in motor
record field list.

#### QEPlotter and QEStripChart

Save, set and restore all line styles when drawing graphic markups.

#### String Formatting
Add forceSign boolean property to widgets using string formatting, the default value is false.

#### Font Scaling

Introduced independent font scaling functionality.

#### QEPVLoadSave

Ensure all array elements are of the same and a suitable type before writing to the channel.

#### windowCustomisation

Include a QAction object as opposed to inheriting from QAction.
This is to support running on MAC OS.

#### QEPlot

Remove outward dependency on QWT, so that plugin library build does not need to
include QWT header files, and do a general tidy up.
Also inherit from QEFrame in order to provides the standard properties.



# <a name="r3.4.3"></a><span style='color:#006666'>r3.4.3</span>

Release date: 5th June 2017.

This release basically consolidates the transition from SourceForge to GitHub,
and also accommodates the support of headless builds (on Windows).
However, it also includes a major bug fix and a number of minor functional changes.

These are:

* qegui - modified the about dialog to include both the EPICS and QWT versions

* QEScratchPad - avoid segmentation fault in drag drop handling - check before de-referencing.

* QEScratchPad - use comma separator for the value QELabel widgets.

* QEGraphic - set minimum size - keep Qt5 happy.

* Modify contextMenu to allow Edit PV action selection criteria to be specified
as opposed to hard coded to Engineer User Level and enable by default for
QEPVProperties and QEScratchPad.

* Truncates strings to 40 chars before attempting to write DBF_STRING mode to a channel.

* Added .gitignore files to each repository.

* Component App/Sup make files are now more OS independent

* Updated sample .ui files to use current widget names (long over due).



# <a name="r3.4.2"></a><span style='color:#006666'>r3.4.2</span>

Release date: 29th April 2017.

This is initial release at GitHub.
This is functionally equivalent to the last SourceForge release despite the
overall restructure.



# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Refer to SourceForge for all history prior to release r.3.4.2 as the
SourceForge history was not been transferred to GitHub.


<font size="-1">Last updated: Sun Apr 26 15:05:12 AEST 2020</font>
<br>
