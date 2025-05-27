# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>Repository Structure</span>

<br>

## <a name="Introduction"></a><span style='color:#006666'>Introduction</span>

This page describes how the repositories at GitHub are organised.

The transfer of the EPICS Qt framework from SourceForge to GitHub has been an ideal
opportunity for a few organisational changes.
These are outlined below.
There were no major functionality changes per se as part of the initial transfer.
However since the transfer a lot has happend (e.g. library split into load library
and plugin library, archive appliance integration, PV Access integration).

The major transfer change is that EPICS Qt was been split into a number of
components, each managed in its own GitHub repository.

The three primary repositories are:
- [QE Framework](https://github.com/qtepics/qeframework) repository which provides
the framework functional and plugin libraries,
- [QEGui Display Manager](https://github.com/qtepics/qegui) repository which
provides the qegui display manager; and
- The  [qtepics.github.io](qtepics.github.io) repository which holds useful
documentation above and beyond the detailed widget documenation currently part
of the [QE Framework](https://github.com/qtepics/qeframework) repository.

Also significant is the the [qeBinaries](https://github.com/qtepics/qeBinaries)
repository which contain rpm files (for Linux) and msi files (for Windows).

The other repositories less significant/optional, and basically provide examples
of using or extending the framework.

* [QE Monitor](https://github.com/qtepics/qeMonitor)
* [QE Read Archive](https://github.com/qtepics/qeReadArchive)
* [QE Widget Display](https://github.com/qtepics/qeWidgetDisplay)
* [QE Example Plugin](https://github.com/qtepics/qeExamplePlugin)
* [QE Byte Array Test](https://github.com/qtepics/qeByteArrayTest)

There is no longer an epicsqt.pro overall project file to build all sub projects.
Each code repository still has its own project file(s), e.g. framework.pro,
QEGuiApp.pro, and these may be opened by qtcreator in order to build each
component as could be done previously.

However, each component is now located within its own EPICS top directory that
allows the component to be readily and headlessly built in a much more EPICS-like
fashion by just calling make from within the top directory.
Under-the-covers, each component's application directory's Makefile essentially
invokes qmake and then make on the generated Makefile.

In the case of qeframework, the include files are placed in top/include and the
shared library/dll file is placed in top/lib/epics_host_arch.
The qeframework plugin library is located in top/lib/epics_host_arch/designer.
In the case of qegui, this is located in top/bin/epics_host_arch.

The use of the environment variable QE_TARGET_DIR may still be used to override
this.

Each code repository has a r3.4.2 tag which corresponds to the last
SourceForge 3.4.2 release.
The latest release is 3.7.1, and each repository has a corresponding r3.7.1 tag.


<font size="-1">Last updated: <Mon Aug 26 12:34:18 AEST 2019/font>
<br>
