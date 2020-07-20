# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 3.5 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.5.3](#r3.5.3)<br>
[r3.5.2](#r3.5.2)<br>
[r3.5.1](#r3.5.1)<br>
[Earlier Releases](#Earlier_Releases)


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


# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Please see the [release notes 3.4 page](release_notes_3.4.html) for the
the 3.4 series release notes.


<font size="-1">Last updated: Mon Jul 20 18:17:10 AEST 2020</font>
<br>
