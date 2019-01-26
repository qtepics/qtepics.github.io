# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt Getting Started</span>


[Introduction](#Introduction)<br>
[Download and Build](#Download)<br>

# <a name="Introduction"></a><span style='color:#006666'>Introduction</span>

There are number of different types of EPICS Qt users, and getting started is
different for each type.
EPICS Qt users can broadly be divided into the following categories (note a user
may "belong" to more than one category):

*  Code down loader and builder - this user knows how to down load and install
the Qt development tool suite and download the source code from GitHib and build
the EPICS Qt framework and QEGui display manager.

*  Code rich plugin and/or application developer.

*  Code free form designer - this user if familiar with designer (Qt's form design
tool) as well as the standard Qt widget set, the EPICS Qt widget set and any other
available widgets.

*  GUI user - this user is familiar with the rub time aspects of the widgets, for
example understanding the meaning of the alarm colour, how to add a PV to the strip
chart and how to retrieve data from the archive.
Such user include operators, beam-line scientists and facility users.


## <a name="Download"></a><span style='color:#006666'>Download and Build</span>

The following items are needed to build EPICS Qt.

### <span style='color:#006666'>EPICS</span>

Information regarding downloading and building EPICS may be found at
[EPICS Home at Argonne](https://epics.anl.gov/) and also at the new
[EPICS Controls](https://epics-controls.org/) web site.
Alternatively speak to your local EPICS expert.

EPICS Qt has successfully be built using versions 3.14.12.5, 3.15.5 and 7.0.1.1.

### <span style='color:#006666'>Qt</span>

Qt is available from the [https://www.qt.io/](https://www.qt.io/) web page.
Versions 4.6, 4.8.4, 5.6, 5.7, 5.9 and 5.10 have been successfully used at the
Australian Synchrotron.
Version 4.8.4 is the earliest version we now actively support.
For new users I would recommend Qt 5.10.
For Archive Appliance users, Qt5 is required.

After installation at adding the appropriate directory/folder to your PATH variable
you should be able to do something similar to the following on Linux:

    $ export PATH=${PATH}:/opt/Qt5.10/5.10.0/gcc_64/bin
    $ qmake -v
    QMake version 3.1
    Using Qt version 5.10.0 in /opt/Qt5.10/5.10.0/gcc_64/lib
    $ uic -v
    uic 5.10.0
    $ moc -v
    moc 5.10.0

and to this on Windows:

    C:\>qmake -v
    QMake version 3.0
    Using Qt version 5.6.1 in C:/qt5/5.6/mingw49_32/lib
    C:\>uic -v
    uic 5.6.1
    C:\>moc -v
    moc 5.6.1


### <span style='color:#006666'>QWT</span>

The selected version of QWT must be compatible with your version of Qt.
For Qt 5.6 or later we use QWT version 6.1.3. For Linux users, a suitable version
of QWT may be available via your distribution's package manager (e.g.yum, apt).
If not, it is available from [http://qwt.sourceforge.net/](http://qwt.sourceforge.net/).


### <span style='color:#006666'>ACAI</span>

From EPICS Qt 3.7 on-wards, the low level Channel Access handing has been striped
out of the EPICS Qt framework and is now handled by the ACAI package.
This is available from [https://github.com/andrewstarritt/acai](https://github.com/andrewstarritt/acai)

    git clone https://github.com/andrewstarritt/acai.git

Building ACAI is straight forward. After downloading, cd to the &lt;top&gt;
directory, modify the line the EPICS_BASE= definition in the configure/RELEASE
(or configure\RELEASE on windows) file to point to **your** local EPICS base
location and then call make.

Once ACAI has been build, and with a suitable PATH environment variable
defined, you should be able to do similar to the following:

    $ export PATH=${PATH}:/epics/acai/bin/linux-x86_64
    $ acai_monitor -v
    ACAI 1.4.6 using EPICS 3.15.5

or:

    C:\> acai_monitor -v
    ACAI 1.4.6 using EPICS 3.14.12.4

acai_monitor uses the ACAI and EPICS libraries but itself is not used by EPICS Qt.

### <span style='color:#006666'>Google Protocol Buffers</span>

This is only required if building the Archive Appliance interface.
Please see the [Archive Appliance](archiver_appliance.html) page for details.
For Linux users using the yum package manager, this can be achieved by
(drop the sudo if running as root):

    sudo yum install -y protobuf

For Windows users ....

### <span style='color:#006666'>FFMpeg Support</span>

This is only required if building FFMpeg Support.

### <span style='color:#006666'>EPICS Qt</span>

The EPICS Qt source code and documentation is available from the [EPICS Qt website](https://github.com/qtepics) at GitHub.
The EPICS Qt site provides a number of repositories.
In order to build the EPICS Qt libraries and the QEGui display manager, you
will need to download the following:

* [framework and support libraries](https://github.com/qtepics/qeframework)<br>
git clone https://github.com/qtepics/qeframework.git

* [QEGui display manager](https://github.com/qtepics/qegui)<br>
git clone https://github.com/qtepics/qegui.git


This getting started guide and other information is available from:
[https://qtepics.github.io/](https://qtepics.github.io/)


<font size="-1">Last updated: Sat Jan 26 20:35:59 AEDT 2019</font>
<br>
