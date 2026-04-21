# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 4.1 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r4.1.6](#r4.1.6)<br>
[r4.1.5](#r4.1.5)<br>
[r4.1.4](#r4.1.4)<br>
[r4.1.3](#r4.1.3)<br>
[r4.1.2](#r4.1.2)<br>
[r4.1.1](#r4.1.1)<br>
[Earlier Releases](#Earlier_Releases)


# <a name="r4.1.6"></a><span style='color:#006666'>r4.1.6</span>

Exprected release date: 25th April 2026

## <span style='color:#006666'>general</span>

The most significant change from a user's point of view is that standard context
menu now can identify when the associated data type is a NTTable, NTNDArray or
some other opaque PV Access data type and include a suitable context entry,
i.e. one of:

 - "Show in NTTable",
 - "Show as Image", or
 - "Show as Opaque".

A new QEOpaque widget has been created to display unknown PV Access data types;
it show the data in a textual form illusrated by this example:

<pre>
epics:p2p/Stats:1.0 
    epics:nt/NTScalar:1.0 ccacheSize
        ulong value 0
        alarm_t alarm
            int severity 0
            int status 0
            string message 
        time_t timeStamp
            long secondsPastEpoch 0
            int nanoseconds 0
            int userTag 0
...
    epics:nt/NTScalar:1.0 banHostPVSize
        ulong value 0
        alarm_t alarm
            int severity 0
            int status 0
            string message 
        time_t timeStamp
            long secondsPastEpoch 0
            int nanoseconds 0
            int userTag 0
</pre>

Some for of exapnd/edid functionality could be added at a later date.

The most significant code changes are:

 - the framework uses QEChannel (which is an alias for qcaobject::QCaObject),
 - the framework now use signals/slots that use a single struct argument.

These changes do not impact exsiting ui files, using designer or qegui.
For 3rd party widget delvelopers, the old style signals still exist, altough
QEChannel will report a run time depracation warning if these are used.

Other changes are identified below.


## <span style='color:#006666'>qeframework</span>

#### QEOpaqueData 

New widget - see above.

#### QBitStatus/QEBitStatus

Updated to add two new string properties: setText and unsetText.
The text is displayed in the centre of each "bit".
Both default to an empty string.

#### QCaAlarmInfo

Added a debug << operator - for developer use.

#### QCaObject/QEChannel

Generate warning and debug message if/when deprecated signals are used.

Also use deleteLater for the CA/PVA client object rather than explicitly
disconnecting any signal/slot connections in the QCaObject destructor.

#### QEString

Do additonal checks when array action is Ascii.
When array action is Ascii, we are never interested in a single element of the array.
This fixed an issue with QELineEdit/QEFileBrowser when trying to write to a char
array record.

#### QEScript

Updated to use new process call API when using Qt6.

#### QELineEdit

Add apply button option (similar to QENumericEdit).

__Note__: QELineEdit no longer inherits from QEGenericEdit, and is now obsolete form
a QE framework point of view, howver left in place incase it is being used by and 3rd
party widgets.

#### QEAbstractDynamicWidget/QEWidget

Relocated the useOwnPersistantName bool flag from QEAbstractDynamicWidget to QEWidget.
QEWidget: add getDetailedConfiguration and setDetailedConfiguration methods.
This allows 3rd party used to save and load detailed widget configuration data.

#### QEStripChart

Allow a time offset to be specified when plotting data on the StripChart 
(some refinement still required).
Exchanged context menu order for "General..." and "Reset" - more convenient (for me ;-)

Also swaped the calculated high/low limits when using a negative scaling (m) value.

#### QEPvaData

For epics:nt/NTTable types, now extracts the descriptor field if it exists.

#### QENTTable

Added a showPVname property which eables/disables dipalying the PV name
at the top of the widget; the property defaults o false.

On PV connection, the widget clears out any data from the previous connection.  

#### QETable

Updated to request variant data (as oppoed to floating array data).
This allowes string arrays to be displayed in a QETable widget.

__Note__: strings a left aligned.


#### QECaClient

QECaClient objects now include the lower level CA client object into QECaClient itself.
Slightly quicker, and may help to reduce memory fragmentation and cache mssing.

Also now spell variant correctly - all are private artefacts, so no user impact.

#### QEHistogram

Updated to honor the autoBarGapWidths property when the orientation is vertical.
Also updated auto bar to gap ratio be 3 to 1.

## <span style='color:#006666'>qegui</span>

Updated to support action requests for context menu entries "Show in NTTable", 
"Show as Image" and "Show as Opaque".

## <span style='color:#006666'>environment variables</span>

#### QE_AD_SUPPORT

This is a new optional environment variable to control whether image decompression
for NTNDArray PVs is included into the QE framework.

To include image decompression define this to be 'YES'.

This splits the role of the ADSUPPORT variable which previously both speficied 
the location of the Area Detector's ADSupport's top directory _and_ whether to
include image decompression functionality.


# <a name="r4.1.5"></a><span style='color:#006666'>r4.1.5</span>

Release date: 20th Feb 2026

## <span style='color:#006666'>general</span>

The most significant change in this release is that the framework/QEImage now can
handle other that uint8 mono images via PV Access, this completing long term goel
for PV access.
This was acheived by cribbing the NTNDArrayConverter code out of Area Detector.
Compressed images can de inflated provided ADSUPPORT is defined in the configure/RELEASE
file and that ADSupport is configure to build the required functions.

The code files now use the much less verbose SPDX tags, e.g.:

    SPDX-FileCopyrightText: 2017-2025 Australian Synchrotron
    SPDX-License-Identifier: LGPL-3.0-only

and updated with a current e-mail address.

There is a new (headless) build control environment variable:

     QE_NUMBER_OF_CORES

which controls the number cores allocated to build the qeFramework.
When __not__ specified, this defaults to 4.

## <span style='color:#006666'>qeframework</span>

#### QEPvaClient

The PVA client now detects and forwards a meta data update indication.

#### QECaClient

The QECaClient leverage off ACAI 1.8.1 to get property/meta data updates.

#### QENTNDArrayConverter

Added QENTNDArrayConverter, copied and pruned from Area Detector adCore R3-14.  

#### QENTNDArrayData

Reworked to use new QENTNDArrayConverter, now handles colour images.
Also, when available, QENTNDArrayData decompresses the image (as opposed to leaving it to QEImage).

#### QEImage

Update the setPvaImage slot function to handle updated QENTNDArrayData variant,
and now no attempt to decompress the image.

The widget now handles descrete "old-stye" array data received via PVA correctly.

Updated the _brightnessContrastAutoImageRequest_ and
_imageDisplayPropertiesChanged_ slot methods to be public.

Also added a background to the time timestamp.

#### QEChannel

New - currently a typedef of qcaobject::QCaObject.
This reason for this is that QCaObject is inconsistant being the only object with
its own name space, and __QEChannel__ reflects that we support both the CA and PVA protcols.  

Eventually the roles of QEChannel and QCaObject will be reversed and QCaObject will become
deprecated.

Also inroducing signal structures to contail all the connection and data update info
(as opposed to separete signal parameters).  
This reduces the size of the boiler plate code, and make signal modification much easier.

Some widgets have been updaterd to use QEChannel and the new signal structures.
This is ongoing and will probably not be complete until the next release.

__Note__: These changes affects 3rd party plugin/display managers developers only.
For now, no changes are required.

#### QEPlatform

Introduce and use some QDateTime wrapper methods to avoid deprecation warnings.

__Note:__ The framework still build against Qt 5.12.8 and upto Qt 6.8.1


#### VariableManager

Use deleteLater() to remove QCaObjects/QEChannel object to avoid potential seg faults.


#### QNumericEdit

Added a new valueEdited signal only emitted when the value is modified by user input.
This is similar to how many native Qt widget work.

#### QENumericEdit

Modify internal Apply button style sheet when the widget is disabled.

Uses the new valueEdited signal and drops the isMetaDataUpdate check.
This keeps usage of CA and PVA consistant.

#### QEStripChart

Added checkbox show/hide (similar to QEPlotter), and re-purposed double click
for regular/bold, as opposed to opening the PV dialog box - that is what the
button does.

#### QEPlotter

Re-purposed double click for regular/bold selection - keep consistant
with QEStripChart.

#### QEAbstractDynamicWidget

Report warning if/when loading/saving a configuration file fails.
This impacts QEStripChart, QEScratchPad and QEPlotter widgets.

## <span style='color:#006666'>qegui</span>

No functional change.

# <a name="r4.1.4"></a><span style='color:#006666'>r4.1.4</span>

Release date: 5th Dec 2025

## <span style='color:#006666'>general</span>

Nothing _ground-braking_ this release, just general improvements including a couple
of improvments provided by Christian Nothoff.

For third party widget developers: note the have been some minor API changes. 

## <span style='color:#006666'>qeframework</span>

#### QEImage/mpeg

This now supports avformat/avcodec version 59 (as used by Alma 9);<br>
The mpeg module still compiles against avformat/avcodec version 58 (as used by CentOS stream 8);<br>
and has dropped support for avformat/avcodec version 57 (as used by CentOS 7).

#### QEImage

Fixed the from mpeg slot specification missed during transition to version 4.

#### QCaObject

Updated so that during object destruction we disconnect signals/slots connections
before calling client->closeChannel ().
This avoids occasional corrupted double-linked list errors.

#### QEFLoating/QEInteger/QEString

We now handle QStringList variant types (from STRING array PVs),
This was especially applicable when the selected array-mode is Ascii, and
avoids malloc unchain warnings and segmentation faults.

#### Control Widgets (excluding buttons):

Added a number of _setPvValue_ slot functions which take a bool, int,
double or QString value.
These allow non framework widgets to effectively write values to the
asociated PV using the signal slot mechanism.
Credit: Christian Nothoff

#### QEButtons

Co-locate the clickCheckedText and clickText properties.
This only affects the property order of appearance in designer.

#### QEStringFormatting

When time formating is selected, use the raw string if PV value is non-numeric.

#### QEPlot

Ensure the _yMin_ property values always less than the _yMax_ property value
(cribbed from strip chart).
Use _yMin_ in log mode, even when _autoscale_ is set.

#### QEPvLoadSave

Implemented the sort functionality to sort items by PV name.

#### QEStripChart

Added a write all traces to file capability (there is a new button on the tool bar).
All values are reampled to the same 1 second time interval prior to writing to a
file, using text or csv format.

Refreshed the tool bar button icons.

#### QEDescriptionLabel

Added an _enableDots_ property; this right pads the text with repeating " .  .  . ".

#### QESpinBox

Added an _autoStepSize_ property; allow auto step size selection, and make this
widget somewhat similar to the QENumericEdit.
Credit: Christian Nothoff

#### QEAnalogSlider/QAnalogSlider

Updated widget to auto scale the minor, major intervals and the precison.

#### QEFileBrowser

This widget now honours font setting, and had an optional boarder, and
controllable margins.

#### QEArchiveStatus

Added a little colour - just for fun.

#### QEManagePixmaps

The managePixmaps class has been renameed to QEManagePixmaps (filenames unchanged).
The number of allowd pixmaps has increased form 8 to 16.

QELabel, QEFrame and QEGenericButton have been updated to use new QEManagePixmaps and
now have additional pixmap properties.

__Note:__ This change may impact 3rd party widgets.

#### QEScaling

The QEScaling class now also scales push button icon sizes.

#### QEEnums

Thus class now provides an enum value to string and reverse function string to
enum value functions together with a count/number enum values function.

#### VariableNameManager/VariableManager

The classes now use more approrpiate data structures.
No functonal change per se.

#### QEExpressionEvaluation

API change to include specifying the number of allowed input letters.
QEPlotter and QEStripChartItem have been updated to use the new QEExpressionEvaluation API.

__Note:__ This only impacts 3rd party widgets using QEExpressionEvaluation.


## <span style='color:#006666'>qegui</span>

Updated saveRestoreManager to use the enum to string and string to enum functions
out of QEEnum.

Renamed the licence file COPYING to LICENSE for overall consistancy.

In run_qegui.bat and .run_qt_designer.batbat files: setting up environment variables
do not require quotes.

# <a name="r4.1.3"></a><span style='color:#006666'>r4.1.3</span>

Release date: 27th May 2025.

## <span style='color:#006666'>general</span>

For our local source code control, we habve migrated from from perforce to git.
Many files have been updated to remove perforce style key words - no functional
change per se.

EPICS Qt now has a read-only options.
This can be used to provide a gui interface (perhaps for training or testing) 
without the possibility of inadvertantly writing to a critical PV.


## <span style='color:#006666'>qeframework</span>

#### QECaClient/QEPvaClient

These have been updated to handle QEVectorVariants when writing CA array data, and 
also handle QStringList when writing PVA data.

Updated to avoid segment faults on shutdown, also bring CA and PVA client managers 
into alignment (credit Yang Zhenghan).


#### QESpinBox

Added  __autoScale__ property to allow auto scaling to be disabled.
Based on idea from Christian Notthoff, ANU.

#### QEAnalogIndicator/QEAnalogProhressBar

Added  __animationTime__ property to provide a progress bar/meter animation capability.
The new poroprty defaults to 0.0 which implies instantaneous, i.e. no animation.
Based on idea from Christian Notthoff, ANU.

#### QCaObject

The getStringValue() method now takes a QE::ArrayActions parameter to control
how strings were accessed - it default to QE::Index.  
The previous implicit default oe QE::Ascii did not work if the PV was itself an
array of strings.

Added a getIsMetaDataUpdate() method to indicate if an update update is the 
first/meta data update.

Updated applicable widgets to use this common method to determine if an update
is the first update rather than each managing their own isFirtUpdate flag.

#### QEComment

This is a new widget that allowd a comment to be embedded within a ui form using 
the __comment__ property.

#### QEExitButton

This new widget, inspired by edm, allows the form or the whole application to
be closed by clicking on a button.
The __exitProgram__ property controls which type of exist is performed.

#### QELink

As well as various equality tests, this widget now has a LookUp option is the __condition__
property.
When selected, the widget will use the input value to select from one of the values 
specified in the __lookupValues__ property.


#### QEPvLoadSave

Updated to hande knock-on effects of from using vector variants in the CA client. 
It now saves uchar arrays as numbers, as oppoed to characters.

Improved the summary format and include qe, ne and n/a qualifiers (as opposed to just 3 numbers)

Compare arrays (live and saved) correctly and consistantly.
Changed the array format, e.g. from "&lt;&lt; 36 element array &gt;&gt;" to "&lt;&lt; array[36] &gt;&gt;".

Overall better error reporting.

#### QEPvLoadSave and QEPvProperties 

Updated context menus to cater for array PVs.

#### QESelector

Updated to alway honour the __source__ proerty when set to SourceFile.

#### QEGenericEdit/QELineEdit

Restore writeNow call for DropToTextAndWrite option,

#### QESimpleShape

Allow independent main and edge control regarding use of style colours.
Ths is done using new __edgeUseStyleAlarmColours__ property.

#### QENumericEdit

Now displays the write forbidden cursor (e.g. when in read-olny mode).

#### QEWidget

Update applicable methods to take a __const__ QCaAlarmInfo parameter.


#### QEFormStateChange

Brought the widget's paint method and designer icon .png file into alignment.


## <span style='color:#006666'>qegui</span>

The only signifcant change is the introduction of a read-only option.
Use either the command line option **--read_only**  or set the environment
varaibel QE_READ_ONLY="1"

Also updated the EPICS_Qt_Installer.wxs versions.
Finally removed some perforce keywords if a few files.

# <a name="r4.1.2"></a><span style='color:#006666'>r4.1.2</span>

Release date: 20th December 2024.

## <span style='color:#006666'>general</span>

The main change in this release is the removal of most depricated usage compiler
warnings.
Special thanks to Sean Dawson re updates later than Qt6.4.

I currently do regular nightly builds using Qt6.4 on AlmaLinux9, CentOS Stream 8
and Windows 10, and using Qt5.12.8 on CentOS 7.
I also do irregular builds using Qt6.4 on Debian 12.


## <span style='color:#006666'>qeframework</span>

#### QEPlotter

The menuSelected slot method is now public (to allow programtic control of the widget).

#### QEAlarmColourSelection

This is a new widget to allow dynamic selection of the alarm colours.
This superceeds any QE_STYLE_COLOR_NAMES and QE_COLOR_NAMES environment
variable settings.

#### QEAbstract2DData

This widget now uses the vector value functions as opposed to the [] operator
to access cached data.
This is a significant optimisation.

#### QECaClient

The CA client now used the vector variants, as opposed to QVariantLists.
This is also provides significant optimisation.

#### QEHistogram

This widget has been updated to handle setting min/max values better
(and consistant with other widgets).
This now allows setting a min value >= the default max value.
This change also bebefits the QEScalarHistogram and QEWaveformHistogram widgets.

#### QEArchiveStatus

The QEArchiveStatus widget now shows total number of PVs.

####  QEStripChart

This has updated to handle to betercheck for NaNs and and infinities.

#### Adaptation parameters

Allow hex (and other radix) integers when accessing integer adaptation parameters.

Added a  getFilename function to adaptation paramaters.
This interprets a leading "~/" text as in the user's home directory.

## <span style='color:#006666'>qegui</span>

The Alarm Colour Selection widget has been incorporated into the qegui display
manager in the Tools menu.

# <a name="r4.1.1"></a><span style='color:#006666'>r4.1.1</span>

Release date: 24th August 2024.

This is the first release of EPICS Qt version 4 and the first release of the 4.1 series.

## <span style='color:#006666'>whats new in version 4</span>

The main change for this major release is how bespoke property enumeration types
are defined in each of the QE widgets.

In version&nbsp;3, each widget defined it's own version of common enumeration types
used by the framework (e.g. the displayAlarmStateOption property) and made these 
available to designer with their own Q_ENUM (enumeration-type) declaration.
In the actual xml ui file, using QELabel as an example, this would be saved
as:

    <property name="displayAlarmStateOption">
      <enum>QELabel::WhenInAlarm</enum>
    </property>


In version 4, essentially all common propery enumeration types are now specified
in a single file (QEEnums.h) in a single object class (QE) together with a single
Q_ENUM declaration.
In the actual xml ui file this would be saved as:

    <property name="displayAlarmStateOption">
      <enum>QE::WhenInAlarm</enum>
    </property>

The advantages of this are:

- less boiler-plate code in each widget header file,
- easier to maintain consistancy,
- because the ui file no longer include the widget class name where the property
  is defined it will be possible to relocate properties to, possibly new,
  intermedate class parents, and/or refactor the class hiearchy without breaking
  any existing ui files.

The disadvantages is ui files created using EPICS Qt version 3 may be incompatible
with version 4, specifically if they have explicitly specified a value for one
of the relocated enumeration properties.
A python tool is avilable to upgrade ui files created with version 3 to be 
compatible with version 4.

Please see the [upgrading to version 4 page](upgrading_to_version4.html) more details.

Once upgraded, from a ui form designer point of view, creating and modifying ui
files, with a couple of specific exceptions, looks exactly as it did with
version 3.
These exceptions are also detailed in the upgrading to version 4 guide.

If you have written your own widget plugin module, some code changes may be 
be required - the complier will help you find these.
Please refer to the upgrading to version 4 guide.

## <span style='color:#006666'>general</span>

During the migration to version 4 and ironing out any issues before releasing
to the wider community a number of other on-going updates to the framework and 
the display manager - these are detailed below.

## <span style='color:#006666'>qeframework</span>

#### QEStripChart

This widget has been modified to only generate statatisitcs using points explicity
displayed on the chart; we do not include any points before or after (such as a value 
at time now which can adveresly skew the statistics of historical data).

#### Internal Archive Meta Data

Use simpler data structues to hold archive related PV meta data to greatly 
reduce the memory requirement.
On our system, with approx 500000 (TBC) PVs this saved about 2.8GB.

Also, when the end time is invalid and less that start time, typically 0, set 
to the current rerad time.
This avoids  time range (TBC exact wording) errors.

#### QENumericEdit, QNumericEdit

Modified to have a value wrap-around/modulo capability.
This only applies when the new **wrapValue** property is set true.

#### QELCDNumber

Hide unnecessary properties in designer, plus use standard code indentation.

#### Drag/drop

Rework to get drag/drop working as actually intended.
Also improved standard drag/drop to inhibit initiating drag with empty text.

#### QECaClient, QEPvaClient

Update protocol clients to be polymorphic and leverage off this in the QCaObject class.

#### QEAbstractDynamicWidget

Stop unwanted pixmap properties being seen in designer.

#### Including/excluding PV Access

The QE_PVACCESS_SUPPORT environment variable is now honored by make.
Previously, this was selected by the use to EPICS base 7 or later.
Now is can be explicity defined as YES or NO by the user.
If undefined, then the previous behaviour is preserved.

#### Bug fixes and othet code impovements

QEGroupBox, QEPvLoadSaveButton: Tidy up the setManagedVisible slot function.

Remove warning: implicitly-declared  operator= warnings (exposed with gcc 11.4.1 
on Alma 9), and other deprecated function calls.

windowCustomisation : check is same customisation is being applied - if so return.

Ensure the result of a  str.toStdString().c_str() operation stays in scope.


## <span style='color:#006666'>qegui</span>

####  Help | About dialog

Allow clip-board copy of ui filename/pathnames from windows tab.

#### Menu: New Window

Rather than just creating an empty window which needs the Open Window menu
entry to be selected to do anything usefull, the New Window menu now invokes
the open file dialog.

#### QEGuiApp.pro

Added console to the config - this allow console (standardout) output on windows.


# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Please see the [release notes 3.9 page](release_notes_3.9.html) for the
the 3.9 series release notes.

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

<font size="-1">Last updated: Tue Apr 21 09:55:11 2026</font>
<br>
