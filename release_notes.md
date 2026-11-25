# ![](epicsqt_logo.png?raw=true) <span style='color:#006666'>EPICS Qt 4.2 Release Notes</span>

# <span style='color:#006666'>Release Index</span>

[r4.2.1](#r4.2.1)<br>
[Earlier Releases](#Earlier_Releases)


# <a name="r4.2.1"></a><span style='color:#006666'>r4.2.1</span>

Exprected release date: 26th November 2026.

This is the first release of the EPICS Qt version 4.2 series.

## <span style='color:#006666'>whats new in release 4.2</span>

The main changes are outlined here. 
Other changes are detailed below.

#### PVXS

The main change for this release is the option to use PVXS as the PVA client.
As with other optional features, the inclusin of PVXS is controlled by an
envirionment variable: QE_PVXS_SUPPORT.

Please see [environment variables page](environment_variables.html) for details.

### Enums

The main code change is that all references to enumeration values
out of _QEEnums.h_ are now fully qualified, e.g.

      case QE::Time:

is now:

      case QE::Formats::Time:

The reason for this was to enable the _QE_ objject to becone a _QE_ namespace
which meant that each __enum__ would have to become an __enum class__.
Alas the knock on effect was some Windows builds, so postponing this change.


## <span style='color:#006666'>general</span>


## <span style='color:#006666'>qeframework</span>


## <span style='color:#006666'>qegui</span>


# <a name="Earlier_Releases"></a><span style='color:#006666'>Earlier Releases</span>

Please see the [release notes 4.1 page](release_notes_4.1.html) for the
the 4.1 series release notes.

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

<font size="-1">Last updated: Tue Nov 17 16:41:55 2026</font>
<br>
