# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 3.9 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.9.1](#r3.9.1)<br>
[Earlier Releases](#Earlier_Releases)

# <a name="r3.9.1"></a><span style='color:#006666'>r3.9.1</span>

Expected release date: January/February 2023.

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
- Use of setContentsMargins in lieu of setSpacing.
- Use of drawRoundedRect in lieu of drawRoundRect.
- Use of QFontMetrics horizontalAdvance in lieu of width.
- Use of QString::asprintf in lieu of sprintf method.
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
other widget that can provide a QString signal.

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

<font size="-1">Last updated: Thu Jan 26 13:52:37 2023</font>
<br>
