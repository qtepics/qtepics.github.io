# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 3.6 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.6.4](#r3.6.4)<br>
[r3.6.3](#r3.6.3)<br>
[r3.6.2](#r3.6.2)<br>
[r3.6.1](#r3.6.1)<br>
[Earlier Releases](#Earlier_Releases)


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



# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Please see the [release notes 3.5 page](release_notes_3.5.html) for the
the 3.5 series release notes.

Please see the [release notes 3.4 page](release_notes_3.4.html) for the
the 3.4 series release notes.


<font size="-1">Last updated: Mon Jul 20 18:21:17 AEST 2020</font>
<br>
