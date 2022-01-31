# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 3.8 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.8.1](#r3.8.1)<br>
[Earlier Releases](#Earlier_Releases)

# <a name="r3.8.1"></a><span style='color:#006666'>r3.8.1</span>

Formal release date: 31th January 2022.

## <span style='color:#666666'>general</span>

The most significant changes to the EPICS Qt framework for the 3.8 release
series are:
- Two new widgets, QESelector and QEFromGroupBox.
- Re-factored the archive interface code.
- Removed many of the deprecated functions.
- 2D data visualisation updates.
- The more "mundane" changes since the previous release.

The details of each of these are described below.

Internal changes means the framework now needs acai-1-6-2 or later.

The project files have been updated to generate warning message to indicate
there is no more Qt4 support.

## <span style='color:#666666'>qtepics.github.io</span>

Documentation updates.

Re-working the adl2qe tool.

## <span style='color:#666666'>qeBinaries</span>

Following a "nasty" e-mail from github regarding size usage, the qeBinaries
repository has been deleted.

## <span style='color:#666666'>qeframework</span>

### New widgets

#### QESelector

This widget provides a combo box that allows the user to select an string
from a pre-defined list of strings, which is then written to the connected PV.
The set of strings may be defined as a QStringList property or read from
a text based configuration file.
Please see QESelector.pdf, located in qtepics.github.io repo, for details.

#### QEFormGroupBox

This widget is a combination QEGroupBox/QEForm widget (it inherits from
QEGroupBox and contains a QEForm widget).

Please see QEFormGroupBox.pdf, located in qtepics.github.io repo, for details.

### Archive access code refactorisation

The main change is to provide a separate thread for dealing with each archive
specified by the QE_ARCHIVE_LIST environment variable.
In this way, data may be retrieved from one archive without having to wait
for all the archives to complete initialising (i.e. providing a list of
available PVs).

The other benefit of this update is that the duplicate PV warning, as in
warning that the same PV is available from multiple archives, now works
as intended.

Known issue: the number outstanding requests status that appear on the
stripchart and in the archive status widget sometimes loses track.
This is being investigated.

From a users point of view, e.g. when using stripchart to retrieve historical
data, there is no change.

From a developer's point of view, there is no change unless your code
relies on in-directly including required header files.
See the change made to rad_control.cpp in the qeReadArchive repo for an
example of this.

### Deprecated Function Removal

Many, but not all, functions/properties etc. flagged as deprecated have been
removed.

The most common is the displayAlarmState boolean property and associated
support functions.
The property itself has been hidden, as in DESIGNABLE false, for many years and
has been supceeded by the displayAlarmStateOptions property.

From a users point of view, designing/using ui files, there is no change.
However from a developer's point of view, e.g. developing third party widgets and
plugins base on the EPICS Qt framework, some code changes may be required.

### QEStriptChart, QEScratchPad etc.

These widgets (i.e. those that inherited from QEAbstractDynamicWidget) have been
modified to update the main window title when a config file successfully loaded or
saved.

Utility functions have bbeen added to QECommon to help acheive this, and the
saveWidget/restoreWidget functions out of the persistanceManager have been
modified to return a boolean success/failure value.

### 2D Data Visualisation

This is still being developed.

The QESurface is now based on own QESurface widget  as opposed to the QT widget.
This overcomes a number of issues, the main one being the widgget is displayed
in-situ  as opposed to being a button that opens a separate window.

A data binning capability has been added.

We now expose the margin as a property in QESpectromgram and the QEWaterfall
widgets, and modified the QESpectromgram to allow third party display
mamanger/plugin to register a customisation paint function.

Like QEImage (see below) the context menus modified to indicate that
flip/rotate is a local data manipulation.

### Other Changes

#### QEPvProperties

Modified PV properties to "know" which fields are potential PV names - the
loss of obligatory ":" was the driver at the Australian Synchrotron;
but is good for more general users anyway.

In the record_field_list.txt, a field name with an * suffix is both read as
a long string and flagged as a PV name, and as such these fields get the usual
context menu options (plot strip chart etc.).

Added the aSub input fields (A,B,...U) and output fields (VALA, VALB,...VALU)
to the set of available fields, and added the common AMSG and UTAG fields to
the record field list file to support base-7.0.6.

__Note__: the widget code now checks for DBF_CHAR, not CHAR when checking for
the field type (needs acai-1-6-2 or later).

#### QEPushButton QERadioButton and QECheckBox

The button properties have been re-redered to locate the more important properties
towards the top of the property editor - no function change per se.

All three headers files have been brought into alignment as far as possible.


#### QENumbericEdit

Updated to allow an optional in built apply button.
When selected the write on change, write on enter etc. options are turned off.
The value is written only when the apply button is clicked.
The default button text is "A" (for apply), however this can be changed with
the applyButtonText property.

Also included a force sign property a la QELabel etc.

__Note__: the default addUnits property value __has changed__ from true to false.

#### QEGroupBox

Modified the QEGroupBox designer icon to be more QGroupBox like.

#### QEImage

Modified the context menu text/legend to emphasis that some of the data manipulation
controls are local control only.
Added use false colour to the options dialog, and made the use false colour and
show time functions slot functions.
No functional change per se.

#### QEMenuButton

The QEMenuButton widget now allows the use macros for the button text.

#### QEPlot

Allow zero pen width and use this to indicate no trace plot required.
Also clears any old data when new connection is being (re-)established.

#### QEPlotter

Ensure effective plot sizes are no greater than available data size (to avoid seg fault).

#### QEStripChart

When pruging the Stringchart data list of real-time data points, delete in chunks of 100
rather than individually - reduced CPU load for really fast updating PVs.
Also removed potential seg fault situation when attempting to access the description.

#### QERadioGroup

Removed the overly restrictive minimum size limits.

#### QESubstitutedLabel

The QESubstitutedLabel text property is now hidden, i,e not designable.
The actual text prperty value is created from the labelText property and any substitutions.

## <span style='color:#666666'>qegui</span>

Added a Reconnect All PVs menu option to qegui/qeframework.
This will close all the channels on the form, and then re-connect and re-subscribe.


# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Please see the [release notes 3.7 page](release_notes_3.7.html) for the
the 3.7 series release notes.

Please see the [release notes 3.6 page](release_notes_3.6.html) for the
the 3.6 series release notes.

Please see the [release notes 3.5 page](release_notes_3.5.html) for the
the 3.5 series release notes.

Please see the [release notes 3.4 page](release_notes_3.4.html) for the
the 3.4 series release notes.

<font size="-1">Last updated: Mon Jan 31 16:49:25 AEDT 2022</font>
<br>
