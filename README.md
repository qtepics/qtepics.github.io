# qtepics.github.io
EPICS Qt at github.

This describes how the seven respositories at github are organised.

NOTE: We are still preparing the github repositories including this documentation.
An annoucement will be made on tech-talk in due course when we are ready. 


The transfer of the EPICS Qt framework from SourceForge to github has been an ideal
opertunity for a few organisational changes. These are outlined below. There have 
been no functionality changes per se.

The major change is that EPICS Qt has been spilt into a number of components, each 
managed in its own github repository. The two primary repositories are qeframework 
and qegui which provide the framework library and the display manager respectively.
The documentation is included within the qeframework repository.

The other repositories are optional, and basically provide examples of using or 
extending the framework.

There is nolonger an epicsqt.pro overall project file to build all sub projects.
Each repository still has its own project file, e.g. framework.pro, QEGuiApp.pro,
and these may be opened by qtcreator in order to build each component as could
be done previously.

However, each component is now located within its own <top> directory that allows
the component to be readily (and headlessly) built in a much more EPICS-like
fashsion by just calling make from within the <top> directory. Under-the-covers, 
the componnent's application directory's own Makefile essentially invokes qmake 
and then make on the generated Makefile.

In the case of qeframework, the inlude files are placed in <top>/include and the shared 
library/dll file is place in <top>/lib/<epics_host_arch>. In the case of qegui, 
this is located in <top>/bin/<epics_host_arch>.  The use of the environment variable
QE_TARGET_DIR may still be used to override this. 

