# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 3.7 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.7.4](#r3.7.4)<br>
[r3.7.3](#r3.7.3)<br>
[r3.7.2](#r3.7.2)<br>
[r3.7.1](#r3.7.1)<br>
[Earlier Releases](#Earlier_Releases)


# <a name="r3.7.4"></a><span style='color:#006666'>r3.7.4</span>

Release date: 3rd August 2020.

## <span style='color:#666666'>qeframework</span>

The significant changes to the qeframework associated with this release are
described below.

#### QEPvLoadSaveButton

The QEPvLoadSaveButton is a new widget that allows a nominated xml file of PV
names and associated PV values (it uses the same format as used by QEPvLoadSave)
to be read and the values from the file written to the PVs.

The widget can also be used to capture a set of PV values and update the xml file.

#### QEPlot

This widget as been modified to add optional sizeVaraibles (similar to the size
variables used in QEPlotter) to limit the number of array elements that are
plotted.

One use case would be using a sscan record's current point (.CPT) field in order
to only plot up-to and including the current scan point.

#### QELineEdit

The QEgenericEdit parent class has been modified to introduced a dropOptions
property to allow DropToText and DropToTextAndWrite in addition to the
default/implict DropToVariable option.

This allows, for example, dragging a detector PV from a QELabel to a QELineEdit
widget connected to the .D01PV field of a sscan record, which will then write the
PV name associated with the QELabel to the sscan record's .D01PV field.

#### Alarm styles

The default framework background alarm colour names (as used by QELables etc) and
the solid alarm colour names (as used by graphical widgets) can now be redefined
using using environment variables.
Please see the documentation and
[environment variables page](environment_variables.html) for details.

#### QESimpleShape

QESimpleShape has been updated to ensure that the PV value used to select the
stateSet text, irrespective of the value of the displayAlarmStateOption property.
Use the .SEVR field if you want the state text selected by the alarm severity.

#### QEPlotter

Updated the QEPlotter widget to be more tolerant of NaN and +/-Inf PV values.


## <span style='color:#666666'>qegui</span>

No change to the qegui application per se.

For the run_qegui.bat, run_qt_designer.bat and run_qerad.bat scripts, we now set
the QT_PLUGIN_PATH by using the to %QE_FRAMEORK% variable as opposed to being
hard coded.

For the EPICS Qt installer config file, added our new archives to the
specification of the QE_ARCHIVE_LIST environment variable.
This is only applicable to Australian Synchrotron users.
Other sites will have to manually define QE_ARCHIVE_LIST.

Updated qeguiApp RELEASE and CONFIG_SITE file to be more configurable with
respect to caQtDM integration.

## <span style='color:#666666'>qeReadArchive</span>

Fixed the time zone issues with the qerad program.

The qerad program now uses double quotes in the help time string examples - this
makes the examples compatible with Windows.
Also updated examples to 2020.

## <span style='color:#666666'>qeBinaries</span>

New 3.7.4 rpm and msi file available after formal release.

## <span style='color:#666666'>documentation</span>

The documentation files, in the qeframework repository, have been updated to
reflect the above changes.
Also the documentation for the following widgets:

 * QELineEdit
 * QNumericEdit/QENumericEdit
 * QRadioGrouo/QERadioGroup

have now be separated into their own documents.


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



# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Please see the [release notes 3.6 page](release_notes_3.6.html) for the
the 3.6 series release notes.

Please see the [release notes 3.5 page](release_notes_3.5.html) for the
the 3.5 series release notes.

Please see the [release notes 3.4 page](release_notes_3.4.html) for the
the 3.4 series release notes.


<font size="-1">Last updated: Tue Jul 21 14:41:34 AEST 2020</font>
<br>
