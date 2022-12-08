# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt Getting Started</span>


[Introduction](#Introduction)<br>
[Download and Build](#Download)<br>
[qtcreator Build](#qtcreator)<br>

# <a name="Introduction"></a><span style='color:#006666'>Introduction</span>

There are number of different types of EPICS Qt users, and getting started is
different for each user type.
EPICS Qt users can broadly be divided into the following categories (note a user
may "belong" to more than one category):

*  Code down loader and builder - this user knows how to down load and install
the Qt development tool suite and download the source code from GitHub and build
the EPICS Qt framework and QEGui display manager.

*  Code rich plugin and/or application developer - this user know how to develope
his/her own plugins and/or own Qt display manager.

*  Code free form designer - this user if familiar with designer (Qt's form design
tool) as well as the standard Qt widget set, the EPICS Qt widget set and any other
available widgets.

*  GUI user - this user is familiar with the run time aspects of the widgets, for
example understanding the meaning of the alarm colour, how to add a PV to the strip
chart and how to retrieve data from the archive.
Such users include operators, beam-line scientists and facility users.


# <a name="Download"></a><span style='color:#006666'>Download and Build</span>

The following items are needed to build EPICS Qt.

## <span style='color:#006666'>EPICS</span>

Information regarding downloading and building EPICS may be found at
[EPICS Home at Argonne](https://epics.anl.gov/) and also at the new
[EPICS Controls](https://epics-controls.org/) web site.
Alternatively speak to your local EPICS expert.

EPICS Qt has successfully been built and tested using, but not limited to,
EPICS base  versions 3.14.12.5, 3.15.6, 7.0.3, and 7.0.6.1
For PV Access functionality, EPICS 7 is required.

## <span style='color:#006666'>Qt</span>

Qt is available from the [https://www.qt.io/](https://www.qt.io/) web page.
Versions 4.6, 4.8.4, 5.6, 5.7, 5.9, 5.10, and 5.12 have been successfully
used at the Australian Synchrotron.
Qt Version 4 is nolonger now actively supported.
For new users I would recommend Qt 5.12.
For users whi need access to the Archive Appliance, Qt5 is required.

After installation and adding the appropriate directory/folder to your PATH
variable you should be able to do something similar to the following on Linux:

    $ export PATH=${PATH}:/opt/Qt5.12.8/5.12.8/gcc_64/bin
    $ qmake -v
    QMake version 3.1
    Using Qt version 5.12.8 in /opt/Qt5.12.8/5.12.8/gcc_64/lib
    $ uic -v
    uic 5.12.8
    $ moc -v
    moc 5.12.8

and like this on Windows:

    C:\>qmake -v
    QMake version 3.0
    Using Qt version 5.6.1 in C:/qt5/5.6/mingw49_32/lib
    C:\>uic -v
    uic 5.6.1
    C:\>moc -v
    moc 5.6.1


## <span style='color:#006666'>QWT</span>

The selected version of QWT must be compatible with your version of Qt.
For Qt 5.6 or later we use QWT version 6.1.3.
For Qt 5.13 we found 6.1.3 uses a number of deprecated function and QWT 6.1.4 is
recommended.

For Linux users, a suitable version of QWT may be available via your
distribution's package manager (e.g. dnf/yum, apt).
If not, it is available from [http://qwt.sourceforge.net/](http://qwt.sourceforge.net/).

## <a name="ACAI"> <span style='color:#006666'>ACAI</span>

From EPICS Qt version 3.7.1 on-wards, the low level Channel Access handling has
been dropped from the EPICS Qt framework and has been replaced by the ACAI package.
This is available from [https://github.com/andrewstarritt/acai](https://github.com/andrewstarritt/acai)

    git clone https://github.com/andrewstarritt/acai.git

Building ACAI is straight forward. After downloading, cd to the &lt;top&gt;
directory, modify the line the EPICS_BASE= definition in the configure/RELEASE
(or configure\\RELEASE on windows) file to point to **your** local EPICS base
location and then call make.

Once ACAI has been build, and with a suitable PATH environment variable
defined, you should be able to do similar to the following:

    $ export PATH=${PATH}:/epics/acai/bin/linux-x86_64
    $ acai_monitor -v
    ACAI 1.7.3 using EPICS 7.0.6.1, CA Protocol version 4.13

or:

    C:\> acai_monitor -v
    ACAI 1.7.3 using EPICS 3.14.12.4, CA Protocol version 4.13

acai_monitor is a test/demo program that uses the ACAI and EPICS libraries,
however the program itself is not used by EPICS Qt.

I suggest the latest version of ACAI, however you must use ACAI version 1.5.8 or later.

## <span style='color:#006666'>Google Protocol Buffers</span>

This is only required if building the Archive Appliance interface.
Please see the [Archive Appliance](archiver_appliance.html) page for details.
For Linux users using the yum package manager, this can be achieved by
(drop the sudo if running as root):

    sudo yum install -y protobuf

For Windows users, there is some info in [Archive Appliance](archiver_appliance.html).

## <span style='color:#006666'>FFMpeg Support</span>

This is only required if building FFMpeg Support.
For Linux users using the yum package manager, this can be achieved by
(drop the sudo if running as root) first installing the nux repo if needs be.
For CentOS 7 this can be done like this:

    sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
    sudo rpm -Uvh \
      http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm

And to install the ffmpeg packages themselves please run:

    sudo yum install -y  ffmpeg-devel  ffmpeg-libs


## <span style='color:#006666'>EPICS Qt</span>

The EPICS Qt source code and documentation is available from the
 [EPICS Qt website](https://github.com/qtepics) at GitHub.
The EPICS Qt site provides a number of repositories.
In order to build the EPICS Qt libraries and the QEGui display manager, you
will need to download the following:

* [framework and support libraries](https://github.com/qtepics/qeframework)

    git clone https://github.com/qtepics/qeframework.git

* [QEGui display manager](https://github.com/qtepics/qegui)

    git clone https://github.com/qtepics/qegui.git


### Modify RELEASE files

The commands shown here illustrate downloading and building EPICS Qt in the
directory <span style='color:#00c000'>/home/user/qtepics</span>.
This is just for the purposes of providing example commands.
You are free to down load and install anywhere on your system.
Replace the <span style='color:#00c000'>green</span> part of the path in the
examples below to suit your own environment.

Note: This instructions are currently Linux-centric, however Windows users should
have no trouble translating these to the Windows equivalent.

Modify <span style='color:#00c000'>/home/user/qtepics</span>/__qeframework__/configure/RELEASE file such that:

    QE_FRAMEWORK=<span style='color:#00c000'>/home/user/qtepics</span>/qeframework<br>
    ACAI=__a reference your ACAI diretory__
    EPICS_BASE=__a reference your EPICS base diretory__


If you are using EPICS 7 together with PV Access, and wish to decompress images
compressed using the Area Detector Codec plugin, the modify
<span style='color:#00c000'>/home/user/qtepics</span>/__qeframework__/configure/RELEASE file
such that:

    ADSUPPORT=__a reference your ADSUPPORT module__

If not required, please remove the ADSUPPORT definition.

Modify <span style='color:#00c000'>/home/user/qtepics</span>/__qegui__/configure/RELEASE file such that:

    QE_FRAMEWORK=<span style='color:#00c000'>/home/user/qtepics</span>/qeframework<br>
    EPICS_BASE=__a reference your EPICS base diretory__



### Environment Variables

Define EPICS_HOST_ARCH (e.g. export EPICS_HOST_ARCH=linux-x86_64)

Define QWT_INCLUDE_PATH (e.g. export QWT_INCLUDE_PATH=/usr/include/qwt)

Define QWT_ROOT to the qwt location (e.g. C:/qwt-6.1.3/ on Windows or<br>
export QWT_ROOT='/usr/local/qwt-6.1.3' on Linux if not in default location)

_Optional:_ Define QE_FFMPEG if mpeg streaming is required (on Windows, this must
  point to the FFMPEG directory; on Linux just being defined is sufficient).

_Optional:_ Define QE_ARCHAPPL_SUPPORT=YES to include Archive Appliance support.

_Optional:_ Define PROTOBUF_INCLUDE_PATH. When Archive Appliance selected, location
of the protobuf header files (if not already in tool chain search path).

_Optional:_ Define PROTOBUF_LIB_DIR. When Archive Appliance selected, location
of the protobuf library files (if not already in tool chain search path).

_Optional:_ Define QE_CAQTDM if integration of PSI's caQtDM into QEGui is required.
If you want caQtDM integrated, download and build it and define the environment
variable QE_CAQTDM to point to the caQtDM_Project directory.

_Optional - deprecated:_ Defining QE_TARGER_DIR forces libraries, header files
and binaries to be built/installed into the nominated directory.
This is not recommended and included for legacy purposes only.
Note: If this environment variable is defined, you must modify the QE_FRAMEWORK
definitions in the configure/RELEASE files to be consistent with this variable.

More details are available at [environment_variables.html](environment_variables.html).

### qmake

When building in headless, i.e. command line, mode, the qmake program is invoked
to generate a Makefile based on the project .pro file.
Ensure that your PATH environment variable results in required version of qmake
being available.
For some versions of Qt 4, the qmake program is known as qmake-qt4.
In this case it will be necessary to "fake" it, e.g.:

    cd ${HOME}/bin
    ln -s /usr/bin/qmake-qt4 qmake

or something similar.

Also, qmake is called without the -spec option defined and relies on the default
spec file (e.g. linux-g++) being suitable.
If this is not the case then you must _fake_ the qmake command to suit your
environment. Alternatively, one could also modify the Makefiles:

    <span style='color:#00c000'>/home/user/qtepics</span>/qeframework/qeframeworkSup/Makefile<br>
    <span style='color:#00c000'>/home/user/qtepics</span>/qeframework/qepluginApp/Makefile<br>
    <span style='color:#00c000'>/home/user/qtepics</span>/qegui/qeguiApp/Makefile<br>

to suit your environment.

### MinGW compiler

Since commit 69d1623 (qeframework repository 8/July/2017), the \_MINGW macro is
automatically defined TRUE if the EPICS_HOST_ARCH is either win32-x86-mingw or
windows-x64-mingw.

See the
<span style='color:#00c000'>/home/user/qtepics</span>/qeframework/qeframeworkSup/project/framework.pro
project file (approximately lines 103-110) for details.

### Build Framework Libraries, Plugin Library and Display Manager

This is simply:

    cd <span style='color:#00c000'>/home/user/qtepics</span>/qeframework
    make

    cd <span style='color:#00c000'>/home/user/qtepics</span>/qegui
    make

### qe_git_test_build

The [qe_git_test_build](tools/qe_git_test_build) script may be used on Linux to
clone the git repositories, build the framework libraries and build the qegui
display manger.

I use this after each git push update to ensure the head version of the code can
still be successfully built;
I currently do this using Qt5.12.8 on CentOS 7.

Run __qe_git_test_build -h__ for help information.

While it was not intended as a general purpose download and build script, it
could be the basis of such a script that could suit your facility.


# <a name="qtcreator"></a><span style='color:#006666'>qtcreator Build</span>

This getting started section assumes the reader is familiar with qtcreator.

There are three separate Qt projects, one each for qeframework, qeplugin and qegui.
There is no overall project to build them all. Note: the archapplDataSup _must_ be
built command line style.

One consequence is when building the QE Framework using qtcreator, the framework
project must be configured with an extra build step in install the header
files so that they are available when building the qeplugin library, qegui program
or any other QE Framework client.
This step is done automatically when using the headless build option described in
the previous section.

Another consequence is that in addition to the environment variables required
for the headless build as described above, the environment variables EPICS_BASE,
ACAI, QE_FRAMEWORK and if required ADSUPPORT must also be defined manually when
using qtcreator.

## qeframework

Using <span style='color:#00c000'>/home/user/qtepics</span> as the git clone
location, open the following project file in qtcreator:

<span style='color:#00c000'>/home/user/qtepics</span>/qeframework/qeframeworkSup/project/framework.pro

During the qmake phase the following message is output.

    Project MESSAGE: Note: By default qtcreator does not have a 'make install' build step. When using qtcreator, modify project
    Project MESSAGE: ....: to add an install build step which is required to install header files to ../../include

To do this, open the project build configuration page in qtcreator and click on
Add Build Step button/combo box and select Make.
In the Make arguments line edit specify install.
In the existing regular make step, consider adding a __-j N__  argument to allow
parallel compilation (where N is the number of available CPU cores).

# ![](build_steps.png?raw=true)

_Note:_ if you know of a way of automatically adding this build step by adding
some directive into the project file, please do let me know.

## qeplugin

Still using /home/user/qtepics at the git clone location, open the following
project file in qtcreator:

<span style='color:#00c000'>/home/user/qtepics</span>/qeframework/qepluginApp/project/qeplugin.pro

## qegui

Again using /home/user/qtepics as the example, open the following project file
in qtcreator :

<span style='color:#00c000'>/home/user/qtepics</span>/qegui/qeguiApp/project/QEGuiApp.pro

<font size="-1">Last updated: Wed Dec  7 13:53:47 2022</font>
<br>
