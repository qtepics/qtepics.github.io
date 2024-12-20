# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 4.1 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r4.1.2](#r4.1.2)<br>
[r4.1.1](#r4.1.1)<br>
[Earlier Releases](#Earlier_Releases)


# <a name="r4.1.2"></a><span style='color:#006666'>r4.1.2</span>

Release date: 20th December 2024.

## <span style='color:#666666'>general</span>

The main change in this release is the removal of most depricated usage compiler
warnings.
Special thanks to Sean Dawson re updates later than Qt6.4.

I currently do regular nightly builds using Qt6.4 on AlmaLinux9, CentOS Stream 8
and Windows 10, and using Qt5.12.8 on CentOS 7.
I also do irregular builds using Qt6.4 on Debian 12.


## <span style='color:#666666'>qeframework</span>

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

## <span style='color:#666666'>qegui</span>

The Alarm Colour Selection widget has been incorporated into the qegui display
manager in the Tools menu.

# <a name="r4.1.1"></a><span style='color:#006666'>r4.1.1</span>

Release date: 24th August 2024.

This is the first release of EPICS Qt version 4 and the first release of the 4.1 series.

## <span style='color:#666666'>whats new in version 4</span>

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

## <span style='color:#666666'>general</span>

During the migration to version 4 and ironing out any issues before releasing
to the wider community a number of other on-going updates to the framework and 
the display manager - these are detailed below.

## <span style='color:#666666'>qeframework</span>

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


## <span style='color:#666666'>qegui</span>

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

<font size="-1">Last updated: Fri Dec 20 12:30:12 AEDT 2024</font>
<br>
