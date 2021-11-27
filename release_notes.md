# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 3.8 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.8.1](#r3.8.1)<br>
[Earlier Releases](#Earlier_Releases)

# <a name="r3.8.1"></a><span style='color:#006666'>r3.8.1</span>

Expected  release date: 15th December 2021.

## <span style='color:#666666'>general</span>

The most significant changes to the EPICS Qt framework for the 3.8 release
series are:
- Two new widgets, QESelector and QEFromGroupBox.
- Re-factored the archive interface code.
- Removed a number of deprecated functions.
- 2D data visualisation updates
- The more "mundane" changes since the previous release.

The details of each of these are described below.

Internal changes means the framework needs acai-1-6-2 or later.
   Modify Qt4 warning message to indicate no more support.


## <span style='color:#666666'>qtepics.github.io</span>

Documentation updates.

Re-working the adl2qe tool.

## <span style='color:#666666'>qeBinaries</span>

Following a "nasty" e-mail from github re size usage, the qeBinaries repository
has been deleted

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
The property itself has been hidden, as in DESIGNABLE false, and supceeded by,
replaced by the displayAlarmStateOptions property for a while.

From a users point of view, designing/using ui files, there is no change.
From a developer's point of view, e.g. developing third party widgets and
plugins base on the EPICS Qt framework, some code changes may be required.

### 2D Data Visualisation

TBD

### Other Changes

#### QEPvProperties

Modified PV proerties to "know" which fields are potential PV names - the
loss of obligatory ":" was the driver for the Synchrotron;
but is good for more general users anyway.

In the record_field_list.txt, field name with a * suffix are both read a long
string and flagged as a PV name, as such these fields get the usual context
menu options (plot strip chart etc.).

Added the aSub input fields (A,B,...U) and output fields (VALA, VALB,...VALU)
to the set of available fields, and added the common AMSG and UTAG fields to
the record field list file to support base-7.0.6

#### QENumbericEdit

Updated to allow an optional in built apply button.
When selected the write on change, write on enter etc. options are turned off.
The value is written only when the apply button is clicked.
The default button text is "A" (for apply), however this can be changed.

Also included a force sign property a la QELabel etc.

__Note__: the default addUnits property value __has changed__ from true to false.

#### QEGroupBox

Modified the QEGroupBox designer icon to be more QGroupBox like.

## <span style='color:#666666'>qegui</span>

Added a Reconnect PVs option to qegui/qeframework.

# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Please see the [release notes 3.7 page](release_notes_3.7.html) for the
the 3.7 series release notes.

Please see the [release notes 3.6 page](release_notes_3.6.html) for the
the 3.6 series release notes.

Please see the [release notes 3.5 page](release_notes_3.5.html) for the
the 3.5 series release notes.

Please see the [release notes 3.4 page](release_notes_3.4.html) for the
the 3.4 series release notes.

<font size="-1">Last updated: Sat Nov 27 17:46:31 AEST 2021</font>
<br>
