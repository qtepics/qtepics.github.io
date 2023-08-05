# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 3.9 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.9.2](#r3.9.2)<br>
[r3.9.1](#r3.9.1)<br>
[Earlier Releases](#Earlier_Releases)

# <a name="r3.9.2"></a><span style='color:#006666'>r3.9.2</span>

Expected release date: 16th August 2023.

## <span style='color:#666666'>general</span>

The most significant change for this release is the way in which external
process are launched using QEPushButton, QEMenuButton etc., specifically the
arguments are kept separated and not concatinated, with the command, into
a single command string.
We got away with it in Qt5 however Qt6 is more strict/correct.

## <span style='color:#666666'>qeframework</span>

#### Archive data retrieval

The framework now allows .SEVR and .STAT (severity and status) PV values to be
retrieved from the archiver (and plotted on the Strip Chart).

#### QEWaveformHistogram

The size of number of elements sanity check value has been increased to 100000.

#### QEImage

Modified to add an axis draw capability for the profiles.
This feature is selectable in designer using the __enableProfileAxes__ property
and in the run-time image dialog.

_Note:_ This applies to all three axes: horizontal, vertical and arbitary line.

#### applicationLauncher

The applicationLauncher class has been updated to handle arguments as separate
objects (in a QStringList) as opposed to being all bundling into the command
string.
This is essentially the oreviously commented out alternate (and cleaner) way
to run the program.
Also a bit of code layout tweaking.

#### QEMenuButton

This widget has been updateed to use a QStringList for program arguments
(a la QEPushButton).

The designer set up dialog associated with the QEMenuButton now allows
the argument to be edited as a string list - this editor is similar in
look and feel as the built-in string list property editor.
The dialog now has a better (as in similar to designer) reset icon for the
quazi properties.

_Note:_ The QEMenuButton widget remains backwards compatible with ui files
created by earlier versions which stored the program arguments as space
separeted text in a single string.

#### Default Protocol

Allow the default provider/protocol to be specified as adaptation parameter.
E.g. to use PV Access in stead of Channel Access by default, define the
environment variable QE_DEFAULT_PROVIDER as "pva".
On Linux:

    export QE_DEFAULT_PROVIDER=pva

#### QEPeriodic

Updated to spell Sulphur element name correctly (as in Australia/UK).
This should have no impact unless 3rd party code relies on the name out
of QEPeriodic::elementInfo (as one of our plugins does).

#### QEPvProperties

Show the enumeration index value as prefix to each enumeration value,
together with some minor layout tweaks.

For normative NTScalar and NTArray types, extract value type and use this to
qualifiy the PV id which used in QEPvProperties.

Update record field list to add the new alarm messahe (NAMSG) field introduced
in base-7.0.7, and updated the text associated with the DOL fields.

#### QEStripChart

When loading/restoring a configuration, do not attempt to insert beyond the end
of the predefined PV name list and thus avoid a seg. fault.
This only impacts Qt6, Qt5 is a little more forgiving of this error.

For the QEStripChart tool bar, removed Lock and PV status place holders tabs
which were a hang over from the Delphi original and not required.


#### QEComboBox, QERadioGroup

Both widgets now have an 'Apply current selection' option available in their
context menu.
This is particularly usefull if current value is undefined as in INVALID/UDF
(typically on IOC start) and allows the value to be set without selecting a
different value first.


#### QSimpleShape

This widget has been modified to include a noshape and a tick shape.
This change is also reflected in the QESimpleShape widget.

#### QEPlot

The widget now checks for NaN and Inf values and does not attempt to plot them.

Also added logScale plotting mode (y-axis) to the widget.
This can be selected by using the __logScale__ property.

## <span style='color:#666666'>qegui</span>

The only change is is a modifcation to the help text to include info about
the new provider environment variable.

# <a name="r3.9.1"></a><span style='color:#006666'>r3.9.1</span>

Release date: 6th March 2023.

## <span style='color:#666666'>general</span>

The most significant change to the EPICS Qt framework for the 3.9 release series
is that the framework is now compatible with Qt6 (specifically the changes were
developed and tested using Qt6.4.0).
Some of these changes mean that the framework is now __no longer__ compatible
with some earlier versions of Qt5 (specifically it still compiles against
Qt5.12.8, however it no longer compiles against Qt5.6) and is definitly
__no longer__ compatible with Qt4.

__Note:__ some conditional statements have been added to allow the framework to
build against both Qt5.12.8 and Qt6.4.0.
All of these are of the form of the following example taken from QEPlatform.h

    #if QT_VERSION < 0x060000
    #define QEKeepEmptyParts QString::KeepEmptyParts
    #define QESkipEmptyParts QString::SkipEmptyParts
    #else
    #define QEKeepEmptyParts Qt::KeepEmptyParts
    #define QESkipEmptyParts Qt::SkipEmptyParts
    #endif

All the version tests are Qt5 vs. Qt6 irrespective of when the change was
introduced by Qt.
If needs be, these test can be easily modified to be more precise and feedback
in this regard is always welcome.

The modification to achieve Qt6 compatibility are:
- Use of QRegularExpression in lieu of QRegExp.
- Use of setContentsMargins in lieu of setMargin.
- Use of drawRoundedRect in lieu of drawRoundRect.
- Use of QFontMetrics horizontalAdvance in lieu of width.
- Use of QString::asprintf in lieu of the sprintf method.
- Use of setForeground (brush) and setBackground (brush) in lieu of
  setBackgroundColor (colour) and setTextColor (colour) respectively.
- How to determine desktop and screen geometry.

There are many QVariant warnings when I build against Qt6 and these are still
to be addressed.

While the main purposed of this release is Qt6 compatibility, a number of
other updates have also been included and these are detailed below.

## <span style='color:#666666'>qeframework</span>

#### QENumbericEdit

The widget has been modified to stop doing an auto-write to PV on first update if
writeOnChange is true and the widget has been updated to conform to any DRVL/DRVH
and/or LOPR/HOPR constraints.
This fix was contributed by __Christian Notthoff__.

#### QEStringFormatting

The framework no longer trims leading and trailing spaces when writing a string
value to a PV.

#### QEPvProperties

Added the pycalc record (out pf pyDevice) fields to the list of known record types.

#### QECorrelation

The widget now allows a much smaller display span (1.0e-12) and uses a more
flexible value presentation format.

#### QEForm/QEFormGroupBox

Both these widgets have new slot functions setUiFileName and setUiFileSubstitutions
that modify the uiFile and variableSubstitutions properties respectively.
This allows dynamic form selection and/or substitutions at run time from any
other widget that can provide a sutable QString signal.

QEForm has also had a code scrub.
Many methods are now defined in the QEForm.cpp file as opposed to header, and
have been made const where applicable.

#### QEGraphicNames/QEGraphicMarkup

Added four markups, namely two horizontal marker lines and two vertical marker
lines.
Unlike most of the other markups, these are entirely under program control.

#### QEPlot

The QEPlot widget now exposes the embedded QEGraphic object to allow 3rd party
plugin/display manger manipulation of the available markups.

#### QEPlotter

The QEPlotter has two new optional PV variable name properties, viz:
xMarkerVariable and yMarkerVariable.

If/when the xMarkerVariable connects and provides a value, the new vertical
marker line is set visible and the value is used to set its position.
If the xMarkerVariable PV disconnects, the vertical marker is set non-visible.

The same applies to the yMarkerVariable and the horizontal marker line.

#### QAnalogSlider (and hence QEAnalogSlider)

Added an invertedApperance property, that is applies to he interbnal QSlider
widget and the axis below the slider.

#### QETable

Added some text formatting properties, namely: addUnits, forceSign, format,
separator and notation.
These have same meaning as per the QELabel widget.

#### QECheckBox (also QEPushButton and QERadioButton)

The QECheckBox is  a little more forgiving when decoding the update text to
determining if the button should be checked or unchecked.
If the PV text matchs neither the clickText and clickCheckedText properties,
then if the underlying PV provides an integer value (such as from an mbbi, bo etc.
record) and an integer value can be extracted from clickText and clickCheckedText
strings then the integer values are used to determining if the button should be
checked or unchecked.
If the integer values do noth match, the widget generates an error message and
prints a debug message.

#### QECaClient

Modified this unit to perform the QVariant to EPICS type conversion, which makes
it more symetrical (this unit also does the EPICS type to QVariant conversion),
and more consistant with the PvaClient.
QECaClient also includes a value range check - needs acai 1.6.4 or later.
These changes allow the IntegerFormatting and the FloatFormatting to be simplified.

#### QCaObject

Added a number of conveniance functions, including reading/wrting boolean values,
and writing integer and floating arrays.
This change only usefull to those wrting their own 3rd party widgets.

#### standardProperties

The unit now treats setting the displayAlarmStateOptions and/or oosAware like a
string formatting change, i.e. cause the widget to update immediately.
This change only usefull to those wrting their own 3rd party widgets.

#### framework.pro

The project file now directly calls up required ADSupport libraries as opposed
to the HDF5 plugin libraries
(the issue became apparent doing a buile on Ubuntu 22.04).

#### archapplDataSup

Removed spurious non-error error message when building archapplDataSup.

#### QEEnum

Removed QEEnum.h (for now) - it will only needed by EPICS Qt version 4.

## <span style='color:#666666'>qegui</span>

No functional changes for this release.
The help information (-h,--help option) has been updated to reflect the
new record types supported by QEPvProperties.

# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Please see the [release notes 3.8 page](release_notes_3.8.html) for the
the 3.8 series release notes.

Please see the [release notes 3.7 page](release_notes_3.7.html) for the
the 3.7 series release notes.

Please see the [release notes 3.6 page](release_notes_3.6.html) for the
the 3.6 series release notes.

Please see the [release notes 3.5 page](release_notes_3.5.html) for the
the 3.5 series release notes.

Please see the [release notes 3.4 page](release_notes_3.4.html) for the
the 3.4 series release notes.

<font size="-1">Last updated: Sat Aug  5 15:25:20 2023</font>
<br>
