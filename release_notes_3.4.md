# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 3.4 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r3.4.3](#r3.4.3)<br>
[r3.4.2](#r3.4.2)<br>
[Earlier Releases](#Earlier_Releases)

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


<font size="-1">Last updated: Mon Jul 20 18:08:23 AEST 2020</font>
<br>
