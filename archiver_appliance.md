# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>Archiver Appliance Support for EPICS Qt </span>


[Introduction](#Introduction)<br>
[Design Decisions](#Design_Decisions)<br>
[Getting Ready](#Getting_Ready)<br>
[Building](#Building)<br>
[Running](#Running)<br>


# <a name="Introduction"></a><span style='color:#006666'>Introduction</span>

The [EPICS Archiver Appliance](https://slacmshankar.github.io/epicsarchiver_docs/)
(AA) has been around for a while now and it seems to be becoming a successor of
the EPICS Channel Access Archive.
As the Australian Synchrotron is also on the path of switching to AA, a decision
to add support for AA in QE Framework has been made.

In this page you will find some information about some design decisions, how to
prepare build environment and how to build QE Framework with AA.


# <a name="Design_Decisions"></a><span style='color:#006666'>Design Decisions</span>

## AA Version

During the development of AA support for QE Framework a requirements for some
extra AA features have arisen. Developers of AA have been kind enough to add
those features to the project; this however means that we have introduced a
dependency on a specific version of AA.

AA support for QE Framework has been developed with __Fall 2017 release
(tag v0.0.1_SNAPSHOT_27-November-2017)__ of AA.
Most probably it will work with newer versions; it definitely won't work with
older ones.

## Google Protocol Buffers

Archived data can be retrieved from AA in many different formats, however Google
Protocol Buffers (PB) are AA's native serializing tool and provide fast and
efficient serialization.
Speed was the main reason to go with PB, consequently this means that PB libraries,
headers and executables need to be present on the machine at build time and run time.
On most Linux distributions these are readily available to be installed using
distribution's package manager.

## archapplDataSup

All PB related code has been separated into a new support application, namely
archapplDataSup (located in the QE framework top directory).
Building of this application is dependent on how environment variables are set up.
The built library has only one entry point and one data structure.
The entry point is a function that takes raw PB input received from AA and saves
parsed data into a vector whose reference has been passed to the function.

This means that there are no dependencies on PB in the code of QE Framework Qt project
which allows the project to be built in exactly the same way as before, if no additional
environment variables are defined.

This also means that archapplDataSup can be used as a standalone library for any
other cases were parsing of AA's PB data is needed.

## Qt 5.0+

In Qt 5.0 support for JSON has been introduced as well as support for easy URL
query composition.
Since Qt 5.0 has been around for a while, those libraries have been used.
This means that in order to build QE Framework with AA support, Qt 5.0 or higher
must be used.

## Obsolete functions

Some of the functions have become obsolete and are only there so that any of
references to them from external applications don't become broken.
These functions are:

* QEArchiveAccess::initialize() - Not needed anymore with new modifications.

* QEArchiveAccess::initialize(const QString& archives, const QString& pattern) - This
functionality has now been removed. The archives and the pattern can now only be
defined using the QE_ARCHIVE_LIST and QE_ARCHIVE_PATTERN environment variables
respectively.

# <a name="Getting_Ready"></a><span style='color:#006666'>Getting Ready</span>

## Have AA Deployed

There is an extensive guide on how to do that on [AA's website](https://slacmshankar.github.io/epicsarchiver_docs/).
As mentioned before, AA support for QE Framework requires __Fall 2017 release (tag v0.0.1_SNAPSHOT_27-November-2017)__ or newer.

## Install Google Protocol Buffers

AA support for QE Framework has been tested with versions 2.5.0, 3.5.0, 3.5.1 and 3.11.1

### On Linux

This should be fairly painless.
All major distributions should have PB software available via their package manager.
So in case of Fedora, CentOS and other RedHat flavours you would run:

    yum install -y protobuf


At least in the case of CentOS 7, this will install a fairly old version of PB (2.5.0).
For the purpose of AA support in QE Framework, this is good enough, however you
can get the latest version of PB from their github releases website.

### On Windows

As expected, here is where it gets a bit trickier.
So far the building of PB has only been tested with MinGW on Windows 7 and Windows 10, both x64.

* CMake needs to be installed. It can be found [here](https://cmake.org/download/).

  * Make sure that the directory containing cmake.exe is on the PATH.


* MinGW needs to be installed, I simply used the one that comes with Qt installation

  * Make sure you add &lt;MinGW_DIR&gt;\bin and &lt;MinGW_DIR&gt;\lib to the PATH

  * If you haven't already, rename &lt;MinGW_DIR&gt;\bin\mingw32-make to make for convenience

* Download the source for C++ code from the [github releases website](https://github.com/protocolbuffers/protobuf/releases/latest).
The package name should be in the format of "protobuf-cpp-x.x.x.zip". Extract it.

* Open command prompt.

* Navigate to the directory where you have previously extracted PB source code to (PB_DIR).

* Navigate to &lt;PB_DIR&gt;/cmake, create directories &lt;PB_DIR&gt;/cmake/build/release and move into newly created directory.

* Run the following:


       cmake -G "MinGW Makefiles" ^
       -DCMAKE_BUILD_TYPE=Release ^
       -DCMAKE_CXX_STANDARD=11 ^
       -Dprotobuf_BUILD_SHARED_LIBS=ON ^
       -Dprotobuf_BUILD_TESTS=OFF ^
       -DCMAKE_INSTALL_PREFIX=<MinGW_DIR> ../..

This will generate Makefiles for MinGW, which will be
used to build Release build, have default C++ version set to C++11, build dynamic
libraries, avoid building tests and install generated files in &lt;MinGW_DI&gt;/lib,
&lt;MinGW_DIR&gt;/bin and &lt;MinGW_DIR&gt;/include

* Run:


      make -j3      # j3 is optional but it makes building a lot faster
      make install


* Check that everything has been installed successfully by running:


       protoc -h

This should print the help for this command.

* At least with the Qt provided MinGW, I had to copy the <MinGW_DIR>/include/google directory to <MinGW_DIR>/i686-w64-mingw32/include
otherwise the headers were not found when building the archapplDataSup library.


## Set Environment Variables

Three new optional environment variables have been introduced with AA support for QE Framework:

* QE_ARCHAPPL_SUPPORT - This is a build time variable. If set to YES, QE Framework
will be built with support for AA. If not defined, support for AA will not be built.

* QE_ARCHIVE_TYPE - This is a run time variable. It can take of two values (CA, ARCHAPPL)
where CA defines that we are connecting to EPICS Channel Access Archive and ARCHAPPL
defines that we are connecting to AA. If not defined, QT Framework will try to
connect to the EPICS Channel Access Archive.

* PROTOBUF_LIBS_DIR - This is a build time variable. In case PB libraries are
not on your PATH (Windows) or LD_LIBRARY_PATH (Linux), this variable is used
while building archapplDataApp to point to PB libraries directory.


# <a name="Building"></a><span style='color:#006666'>Building</span>

Once PB is installed and variables set, QE Framework can be normally built in
the same way as it has been built before, by executing ?make? in the QE Framework's
TOP directory.

PB version 3.6.0 or later requires C++ 11. To support that we've added a ARCHAPPL_USE_CPP11 flag in the $(TOP)/configure/CONFIG_SITE file.
By default the flag is set to YES and archapplDataSup will be built with C++ 11 support. If you don't want that, set it to NO but bear in 
mind that you have to use PB < 3.6.0. QeFramework doesn't rely on any functionallity added in versions after 3.6.0.

The build with AA support enabled will result in two new libraries archapplData.*
in QE Framework's libraries directory and one new header archapplData.h in framework's
include directory.


# <a name="Running"></a><span style='color:#006666'>Running</span>

The only thing that is left to do now is to define the URL in QE_ARCHIVE_LIST to the AA.
The URL should point to AA's management BPL so something like http://archiver01/mgmt/bpl
(protocol and port are not required; default is http and port 80).



<font size="-1">Last updated: Sat Jan 26 18:25:01 AEDT 2019</font>
<br>
