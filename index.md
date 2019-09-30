# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt at GitHub</span>


## <a name="Introduction"></a><span style='color:#006666'>Introduction</span>

Welcome to EPICS Qt at GitHub.

EPICS Qt is a layered framework based on Qt for accessing Experimental Physics and
Industrial Control System (EPICS) data using Channel Access (CA) and PV Access (PVA).
It has been designed for rapid development of control system graphical interfaces,
initially developed at the Australian Synchrotron.

The EPICS Qt (QE) Framework can be used in three ways:

* Code Free GUI systems using Qt's Designer application with the QE Framework plugin
to design GUIs, and the QEGui application to present GUIs to users.

* Code Rich GUI development using Qt's Integrated Development Environment with the
QE Framework widgets and data objects to design GUI applications.

* Console application development using Qt's Integrated Development Environment
with the QE Framework data objects to design console applications that can access
EPICS data.

Note, there are many variations to the above, such as using another Integrated
Development Environment like Eclipse, or developing new plugin widgets to implement
desired functionality, then using those widgets within a code free GUI development.

Other documents you may be interested in are:

* [QE_QEGuiAndUserInterfaceDesign.pdf](https://github.com/qtepics/qeframework/blob/master/documentation/QE_QEGuiAndUserInterfaceDesign.pdf) -
general documentation for developing code free GUI applications.

* [QEWidgetSpecifications.pdf](https://github.com/qtepics/qeframework/blob/master/documentation/QEWidgetSpecifications.pdf) -
widget specific documentation for developing code free GUI applications.

* [QE_FrameworkOverview.pdf](https://github.com/qtepics/qeframework/blob/master/documentation/QE_FrameworkOverview.pdf) -
technical overview of the QE framework.

* [QE_ReferenceManual.pdf](https://github.com/qtepics/qeframework/blob/master/documentation/QE_ReferenceManual.pdf) -
reference manual for programmers using QE widgets and classes.


## <a name="License"></a><span style='color:#006666'>License</span>

The EPICS QT Framework is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

The EPICS QT Framework is distributed in the hope that it will be useful, but
__WITHOUT ANY WARRANTY__; without even the implied warranty of __MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE__.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with the EPICS QT Framework.
If not, see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).


## <a name="Structure"></a><span style='color:#006666'>Repository Structure</span>

The repository structure is documented separately in
[structure.html](structure.html).


## <a name="RoadMap"></a><span style='color:#006666'>Quick Road-map for Code Free GUI Development</span>

* __Ensure you have:__ EPICS, acai, Qt and QWT installed see getting started below.

* __Download source:__ see Download source code and documentation below.

* __Set up build environment__, i.e. the RELEASE files see Modify RELEASE files;
and the environment variables see environment variables or environment variables.

* __Build framework__ see Build Plugin Library and Display Manager.

* __Build qegui__ (display manager) see Build Plugin Library and Display Manager.

* __Set up run time environment__ (environment variables) see environment variables.

* __Run__ qegui.


## <a name="Headless"></a><span style='color:#006666'>Getting Started</span>

This is documented separately in
[getting_started.html](getting_started.html).


## <a name="Environment_Variables"></a><span style='color:#006666'>Environment Variables</span>

These are documented separately in
[environment_variables.html](environment_variables.html).


## <span style='color:#006666'>Archiver Appliance (Optional)</span>

Please visit [EPICS Archiver Appliance](archiver_appliance.html) support documentation.


## <span style='color:#006666'>PV Access Support</span>

Please visit the [PV Access support documentation](pv_access.html) for details.


## <span style='color:#006666'>PSI's caQtDM Integration</span>

Please visit the [caQtDM integration documentation](caqtdm_integration.html) for details.


## <a name="Collaboration"></a><span style='color:#006666'>Future Plans</span>

In brief:
- Update PV Access functionality to support all image formats.
- Revisit PSI's caQtDM integration.


## <a name="Collaboration"></a><span style='color:#006666'>Feed Back and Collaboration</span>

Please email: [andrews@ansto.gov.au](andrews@ansto.gov.au)

Note: this is new e-mail address - the old synchrotron.org.au address will still
work for a while.


## <a name="Release_Notes"></a><span style='color:#006666'>Release Notes</span>

These are documented separately and are available [here](release_notes.html).

## <a name="Credits"></a><span style='color:#006666'>Credits</span>

### Developers

Andrew Ryder, Glenn Jackson, Anthony Owen, Ricardo Fernandes, Anton Maksimenko,
Andraz Pozar, Andrew Starritt, Zai Wang.

### 3rd Party Software

Apart from EPICS base and Qt itself, the EPICS Qt framework uses the following:

The framework relies on QWT for plotting
[https://sourceforge.net/projects/qwt/](https://sourceforge.net/projects/qwt/).

To access the Channel Access Archive data, the framework relies on the
maiaXmlRpcClient and support classes written by Frerich Raabe <raabe@kde.org>,
Ian Reinhart Geiser <geiseri@kde.org>, Karl Glatz and
Sebastian Wiedenroth <wiedi@frubar.net>.

When build with EPICS Archiver Appliance support, the EPICS Qt framework relies
on Google Protocol Buffers
[https://developers.google.com/protocol-buffers/](https://developers.google.com/protocol-buffers/).

When built with MPEG support, the EPICS Qt framework relies on FFmpeg for reading
MPEG image streams [https://www.ffmpeg.org/](https://www.ffmpeg.org/).

The QEGui application can be built to support caQtDM (version 3 and after
EPICS Qt release 3.7.2 will support version 4) widgets provided by The Paul
Scherrer Institute.
[http://epics.web.psi.ch/software/caqtdm/](http://epics.web.psi.ch/software/caqtdm/).


<font size="-1">Last updated: Mon Sep 30 19:27:29 AEST 2019</font>
<br>
