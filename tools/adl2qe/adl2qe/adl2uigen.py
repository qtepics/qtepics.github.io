# $File: //ASP/tec/gui/qtepics.github.io/trunk/tools/adl2qe/adl2qe/adl2uigen.py $
# $Revision: #16 $
# $DateTime: 2024/10/09 12:17:34 $
# Last checked in by: $Author: starritt $
#

"""
Note: we indent the generated xml, not because designer or qegui
needs it, but this helps with debugging.
"""

import os.path
import xml.sax.saxutils

from . import AlarmMode
from . import FrameworkVersion
from . import adl2colour

# ------------------------------------------------------------------------------
#
class_object_counters = {}


def object_name_reset():
    global class_object_counters
    class_object_counters = {}


def gen_object_name(classname):
    assert isinstance(classname, str), "classname argument is not a string"

    if classname in class_object_counters:
        j = class_object_counters[classname] + 1
    else:
        j = 1

    class_object_counters.update({classname: j})
    return "%s_%03d" % (classname.lower(), j)


# -------------------------------------------------------------------------------
#
def escape(text):
    """ modified escape to do " as well as &, < and >
    """
    result = xml.sax.saxutils.escape(text)
    result = result.replace('"', "&quot;")
    return result


# ------------------------------------------------------------------------------
# Python class names reflect Qt class names.
#
class QWidget (object):

    m = 10
    d = 10
    font_size = 8
    default_colours = False          # as in use default EPICS Qt colours
    alarm_state_option = AlarmMode.when_in_alarm

    @staticmethod
    def relative_position(item, origin):
        result = {}
        result['x'] = item['x'] - origin['x']
        result['y'] = item['y'] - origin['y']
        result['width'] = item['width']
        result['height'] = item['height']
        return result

    @classmethod
    def scale(cls, x):
        return int((int(x) * QWidget.m) // QWidget.d)

    def __init__(self, adl, target, level):
        self._adl = adl
        self._target = target
        self._level = int(level)
        self._object_name = gen_object_name(self.classname)

        # Stop nonsense
        if self._level > 50:
            self._level = 50

    @property
    def classname(self):
        return self.__class__.__name__

    @property
    def adl(self):
        return self._adl

    @property
    def target(self):
        return self._target

    @property
    def level(self):
        return self._level

    @property
    def object_name(self):
        return self._object_name

    @property
    def indent(self):
        result = " " * self._level
        return result

    def write_line(self, line):
        self.target.write(self.indent + line + '\n')

    def write_widget(self, parent_geo=None):
        # write xml head
        #
        save_level = self._level
        self.write_line('<widget class="{cn}" name="{on}">'.
                        format(cn=self.classname, on=self.object_name))
        self._level += 1

        # All widgets have a geometry.
        # In adl files, the object positions are absolute, not relative to the composite
        # However in Qt form, child wigets' geometries are relative to their parents.
        #
        geo = self.adl.get("object", None)
        if parent_geo is not None:
            geo = QWidget.relative_position(geo, parent_geo)

        x = QWidget.scale(geo["x"])
        y = QWidget.scale(geo["y"])
        w = QWidget.scale(geo["width"])
        h = QWidget.scale(geo["height"])

        self.write_line('<property name="geometry">')
        self.write_line(' <rect>')
        self.write_line('  <x>{x}</x>'.format(x=x))
        self.write_line('  <y>{y}</y>'.format(y=y))
        self.write_line('  <width>{w}</width>'.format(w=w))
        self.write_line('  <height>{h}</height>'.format(h=h))
        self.write_line(' </rect>')
        self.write_line('</property>')

        self.write_line('<property name="font">')
        self.write_line(' <font>')
        self.write_line('  <pointsize>{ps}</pointsize>'.format(ps=QWidget.font_size))
        self.write_line(' </font>')
        self.write_line('</property>')

        # Write widget specific properties
        #
        self.write_properties()

        # write xml tail
        #
        self._level = save_level
        self.write_line("</widget>")

    # Must be overriden.
    #
    def write_properties(self):
        raise NotImplementedError(self.classname + ".write_properties()")

    # -------------------------------------------------------------------------------
    # Utility functions
    #
    def write_string(self, name, text):
        self.write_line('<property name="' + name + '">')
        self.write_line(' <string>' + escape(text) + '</string>')
        self.write_line('</property>')

    def write_stdset_string(self, name, text):
        self.write_line('<property name="' + name + '" stdset="0">')
        self.write_line(' <string>' + escape(text) + '</string>')
        self.write_line('</property>')

    def write_string_list(self, name, text_list):
        self.write_line('<property name="' + name + '">')
        self.write_line(' <stringlist>')
        for text in text_list:
            self.write_line('    <string>' + escape(text) + '</string>')
        self.write_line(' </stringlist>')
        self.write_line('</property>')

    def write_enum(self, name, text):
        self.write_line('<property name="' + name + '">')
        self.write_line(' <enum>' + escape(text) + '</enum>')
        self.write_line('</property>')

    def write_number(self, name, value):
        text = str(value)
        self.write_line('<property name="' + name + '">')
        self.write_line(' <number>' + escape(text) + '</number>')
        self.write_line('</property>')

    def write_double(self, name, value):
        text = str(value)
        self.write_line('<property name="' + name + '">')
        self.write_line(' <double>' + escape(text) + '</double>')
        self.write_line('</property>')

    def write_bool(self, name, value):
        if value:
            text = "true"
        else:
            text = "false"
        self.write_line('<property name="' + name + '">')
        self.write_line(' <bool>' + escape(text) + '</bool>')
        self.write_line('</property>\n')

    def write_colour(self, name, r, g, b, a=None):
        self.write_line('<property name="' + name + '" stdset="0">')
        if a is None:
            self.write_line(' <color>')
        else:
            self.write_line(' <color alpha="{a}">'.format(a=int(a)))
        self.write_line('  <red>{r}</red>'.       format(r=int(r)))
        self.write_line('  <green>{g}</green>'.   format(g=int(g)))
        self.write_line('  <blue>{b}</blue>'.     format(b=int(b)))
        self.write_line(' </color>')
        self.write_line('</property>')

    def write_pv_name(self, kind):
        """ Suitable for essentially single variable widgets.
        kind is control or monitor
        """
        common = self.adl.get(kind, None)
        if common is not None:
            if "chan" in common:
                pv_name = common["chan"]
                if QWidget.macro_name is not None:
                    find = "$(%s)" % QWidget.macro_name
                    replace = "$(%s):" % QWidget.macro_name
                    pv_name = pv_name.replace(find, replace)

                self.write_stdset_string("variable", pv_name)

    def write_alarm_and_style(self, kind, prefix=None):

        if prefix is None:
            if self.qe_version == FrameworkVersion.v3:
                prefix = self.classname
            elif self.qe_version == FrameworkVersion.v4:
                prefix = "QE"
            else:
                raise ValueError(f"QELabel: unexpected version {self.qe_version}")

        daso_inuse = True  # hypothesize displayAlarmStateOption in use

        # Alarm state handling
        #
        if QWidget.alarm_state_option == AlarmMode.when_in_alarm:
            self.write_enum("displayAlarmStateOption", "%s::WhenInAlarm" % prefix)

        elif QWidget.alarm_state_option == AlarmMode.widget_default:
            # No need to set the displayAlarmStateOption,
            # just use the widget default what ever it is.
            #
            pass

        elif QWidget.alarm_state_option == AlarmMode.medm_mode:
            clrmod = self.adl.get("clrmod", "static")
            lookup = {"static": "Never",
                      "alarm": "Always",
                      "discrete": "Never"}
            option = lookup[clrmod]
            self.write_enum("displayAlarmStateOption", "%s::%s" % (prefix, option))
            daso_inuse = (lookup == "Always")

        else:
            print("Warning: un-handled alarm state option: %s" % QWidget.alarm_state_option)

        # Style
        #
        common = self.adl.get(kind, None)
        if common is not None:
            fcn = common.get("clr", None)
            bcn = common.get("bclr", None)

            if daso_inuse:
                # Always set forground to black
                #
                fcn = 14

            # If default colours specified, do NOT set colours based on the
            # original medm adl file.
            #
            if not QWidget.default_colours:
                defaultStyle = adl2colour.get_style(bcn, fcn)
                self.write_stdset_string("defaultStyle", defaultStyle)

    def write_alignment(self, name, value):
        assert isinstance(value, str), "write_alignment: value is not a string"

        if value == "horiz. left":
            text = "Qt::AlignLeft"
        elif value == "horiz. right":
            text = "Qt::AlignRight"
        elif value == "horiz. centered":
            text = "Qt::AlignCenter"
        else:
            return

        self.write_line('<property name="' + name + '">')
        self.write_line(' <set>' + escape(text) + '</set>')
        self.write_line('</property>')


# ------------------------------------------------------------------------------
#
class QESubstitutedLabel (QWidget):

    def write_properties(self):
        attributes = self.adl.get("basic attribute", None)
        if attributes is not None:
            fcn = attributes.get("clr", None)
        else:
            fcn = adl2colour.RGB(0, 0, 0)

        bcn = adl2colour.RGBA(0, 0, 0, 0)  # see through
        styleSheet = adl2colour.get_style(bcn, fcn)

        # If default colours specified, do NOT set colours based on the
        # original medm adl file.
        #
        if QWidget.default_colours:
            # Not strictly default, but sensible.
            #
            self.write_string("styleSheet", "")
        else:
            self.write_string("styleSheet", styleSheet)

        text = self.adl.get("textix", "")
        self.write_stdset_string("labelText", text)

        align = self.adl.get("align", None)
        if align is not None:
            self.write_alignment("alignment", align)


# ------------------------------------------------------------------------------
#
class QSimpleShape (QWidget):

    def write_properties(self):

        class_type = self.adl.get("class_type", None)
        lookup = {"rectangle": "QSimpleShape::rectangle",
                  "oval": "QSimpleShape::ellipse",
                  "arc": "QSimpleShape::pie"}
        self.write_enum("shape", lookup[class_type])

        if class_type == "arc":
            start = self.adl.get("begin", None)
            span = self.adl.get("path", None)
            if start is not None and span is not None:
                # convert to degrees
                #
                start_angle = int(start) // 64
                span_angle = int(span) // 64
                centre_angle = 90 - (start_angle + (span_angle // 2))
                self.write_number("centreAngle", centre_angle)
                self.write_number("spanAngle", span_angle)

        attributes = self.adl.get("basic attribute", None)
        if attributes is not None:
            edge_width = attributes.get("width", 1)
            fill_mode = attributes.get("fill", "solid")

            colour_number = attributes.get("clr", -1)
            colour = adl2colour.get_rgb(colour_number)

            r = colour[0]
            g = colour[1]
            b = colour[2]

            if fill_mode == "solid":
                self.write_number("edgeWidth", 0)
                self.write_colour("colour0", r, g, b, None)
            else:
                # must be outline
                self.write_number("edgeWidth", edge_width)
                self.write_colour("edgeColour", r, g, b, None)
                self.write_colour("colour0", 0, 0, 0, 0)   # see through

            edge_style = attributes.get("style", None)
            if edge_style == "dash":
                self.write_enum("edgeStyle", "Qt::DotLine")


# ------------------------------------------------------------------------------
# We use a QFrame (as opposed to a QWidget and this allows the user to define
# a boarder manually if they wish.
#
class QFrame (QWidget):

    def write_properties(self):
        self.write_enum("frameShape", "QFrame::NoFrame")
        self.write_enum("frameShadow", "QFrame::Plain")

#       image_type = self.adl.get("type", None)
        image_name = self.adl.get("image name", None)

        if image_name is not None:
            parts = os.path.splitext(image_name)
            url_name = parts[0] + ".png"

            if parts[1] != ".png":
                print("note: run convert %s %s" % (image_name, url_name))

            self.write_string("styleSheet", "QFrame#%s { border-image: url(%s); }" %
                              (self.object_name, url_name))


# ------------------------------------------------------------------------------
#
class QELabel (QWidget):

    def write_properties(self):

        if self.qe_version == FrameworkVersion.v3:
            enum_prefix = "QELabel"
        elif self.qe_version == FrameworkVersion.v4:
            enum_prefix = "QE"
        else:
            raise ValueError(f"QELabel: unexpected version {self.qe_version}")

        self.write_pv_name("monitor")
        self.write_alarm_and_style("monitor", prefix=enum_prefix)

        align = self.adl.get("align", "horiz. left")
        self.write_alignment("alignment", align)


        format = self.adl.get("format", "decimal")
        lookup = {"decimal": f"{enum_prefix}::Fixed",
                  "exponential": f"{enum_prefix}::Scientific",
                  "engr. notation": f"{enum_prefix}::Scientific",
                  "compact": f"{enum_prefix}::Automatic"}
        nval = lookup.get(format, f"{enum_prefix}::Fixed")
        self.write_enum("notation", nval)


# ------------------------------------------------------------------------------
#
class QEAnalogProgressBar (QWidget):

    def write_properties(self):
        self.write_pv_name("monitor")
        self.write_alarm_and_style("monitor")
        self.write_enum("alarmSeverityDisplayMode", "QEAnalogProgressBar::foreground")
        self.write_bool("useDbDisplayLimits", True)

        class_type = self.adl.get("class_type", None)
        if class_type == "meter":
            mode = "Meter"
        elif class_type == "bar":
            mode = "Bar"
        elif class_type == "indicator":
            mode = "Scale"
        self.write_enum("mode", mode)


# ------------------------------------------------------------------------------
#
class QEBitStatus (QWidget):

    def write_properties(self):

        self.write_pv_name("monitor")
        self.write_alarm_and_style("monitor")

        sbit = self.adl.get("sbit", 15)
        ebit = self.adl.get("ebit", 0)
        direction = self.adl.get("direction", "right")

        number_of_bits = sbit - ebit + 1
        shift = ebit

        self.write_number("shift", shift)
        self.write_number("numberOfBits", number_of_bits)

        if self.qe_version == FrameworkVersion.v3:
            if direction == "right":
                orientation = "QBitStatus::LSB_On_Right"
            elif direction == "down":
                orientation = "QBitStatus::LSB_On_Bottom"
            elif direction == "left":
                orientation = "QBitStatus::LSB_On_Left"
            elif direction == "up":
                orientation = "QBitStatus::LSB_On_Top"
            self.write_enum("Orientation", orientation)

        elif self.qe_version == FrameworkVersion.v4:
            if direction == "right":
                orientation = "Qt::Horizontal"
                invertedAppearance = False
            elif direction == "down":
                orientation = "Qt::Vertical"
                invertedAppearance = False
            elif direction == "left":
                orientation = "Qt::Horizontal"
                invertedAppearance = True
            elif direction == "up":
                orientation = "Qt::Vertical"
                invertedAppearance = True
            self.write_enum("orientation", orientation)
            self.write_bool("invertedAppearance", invertedAppearance)

        else:
            raise ValueError(f"QEBitStatus: unexpected version {self.qe_version}")


# ------------------------------------------------------------------------------
#
class QEPlot(QWidget):

    def write_properties(self):
        self.write_enum("frameShape", "QFrame::Box")
        self.write_enum("frameShadow", "QFrame::Sunken")
        self.write_stdset_string("defaultStyle",
                                 "QWidget { background-color: #e0e0e0; color: #000000; }")

        if self.qe_version == FrameworkVersion.v3:
            self.write_enum("displayAlarmStateOption", "QEFrame::Never")
        elif self.qe_version == FrameworkVersion.v4:
            self.write_enum("displayAlarmStateOption", "QE::Never")
        else:
            raise ValueError(f"QEPlot: unexpected version {self.qe_version}")

        plotcom = self.adl.get("plotcom", None)
        if plotcom is not None:
            title = plotcom.get("title", None)
            if title:
                self.write_string("title", title)

            xUnit = plotcom.get("xlabel", None)
            if xUnit:
                self.write_string("xUnit", xUnit)

            yUnit = plotcom.get("ylabel", None)
            if yUnit:
                self.write_string("yUnit", yUnit)

        period = self.adl.get("period", None)
        units = self.adl.get("units", None)
        if period:
            if units == "minute":
                period = period * 60.0
            elif units == "milli-second":
                period = period / 1000.0

            # The time span specified as an integer number of seconds.
            #
            timeSpan = int(period + 0.5)
            self.write_number("timeSpan", timeSpan)

        for slot in range(8):
            var = slot + 1

            pen = self.adl.get("pen[%s]" % slot, None)
            if pen is not None:
                if slot >= 8:
                    print("warning - too many strip chart PVs")
                    continue

                if "chan" in pen:
                    pv_name = pen["chan"]
                    self.write_stdset_string("variable%s" % var, pv_name)

                colour_number = pen.get("clr", -1)
                colour = adl2colour.get_rgb(colour_number)

                r = colour[0]
                g = colour[1]
                b = colour[2]
                self.write_colour("traceColor%s" % var, r, g, b, None)


# ------------------------------------------------------------------------------
#
class QEPlotter(QWidget):

    def write_properties(self):
        self.write_enum("frameShape", "QFrame::Box")
        self.write_enum("frameShadow", "QFrame::Sunken")

        plotcom = self.adl.get("plotcom", None)
        if plotcom is not None:
            fcn = plotcom.get("clr", None)
            bcn = plotcom.get("bclr", None)
            defaultStyle = adl2colour.get_style(bcn, fcn)
            self.write_stdset_string("defaultStyle", defaultStyle)

        self.write_bool("toolBarIsVisible", False)
        self.write_bool("pvItemsIsVisible", False)
        self.write_bool("statusIsVisible", False)

        axis = self.adl.get("x_axis", None)
        if axis is not None:
            axis_style = axis.get("axisStyle", None)
            self.write_bool("xLogarithmic", axis_style == "log10")
            range_style = axis.get("rangeStyle", None)
            if range_style == "user-specified":
                value = axis.get("minRange", None)
                self.write_double("xMinimum", value)
                value = axis.get("maxRange", None)
                self.write_double("xMaximum", value)

        # Ditto, but ONLY for y1
        #
        axis = self.adl.get("y1_axis", None)
        if axis is not None:
            axis_style = axis.get("axisStyle", None)
            self.write_bool("yLogarithmic", axis_style == "log10")
            range_style = axis.get("rangeStyle", None)
            if range_style == "user-specified":
                value = axis.get("minRange", None)
                self.write_double("yMinimum", value)
                value = axis.get("maxRange", None)
                self.write_double("yMaximum", value)

        pv_name = self.adl.get("countPvName", None)
        if pv_name is not None:
            self.write_stdset_string("SizeVariableX", pv_name)

        # We use the x sata from first trace
        #
        trace = self.adl.get("trace[0]", None)
        if trace is not None:
            pv_name = trace.get("xdata", None)
            if pv_name is not None:
                self.write_stdset_string("DataVariableX", pv_name)

        for t, y in enumerate("ABCDEFGH"):
            key = "trace[%d]" % t
            trace = self.adl.get(key, None)
            if trace is not None:
                pv_name = trace.get("ydata", None)
                self.write_stdset_string("DataVariable%s" % y, pv_name)
                colour_number = trace.get("data_clr", None)
                if colour_number is not None:
                    colour = adl2colour.get_rgb(colour_number)
                    r = colour[0]
                    g = colour[1]
                    b = colour[2]
                    self.write_colour("Colour%s" % y, r, g, b, None)


# ------------------------------------------------------------------------------
#
class QELineEdit(QWidget):

    def write_properties(self):
        if self.qe_version == FrameworkVersion.v3:
            enum_prefix1 = "QEGenericEdit"
            enum_prefix2 = "QELineEdit"
        elif self.qe_version == FrameworkVersion.v4:
            enum_prefix1 = "QE"
            enum_prefix2 = "QE"
        else:
            raise ValueError(f"QELineEdit: unexpected version {self.qe_version}")

        self.write_pv_name("control")
        self.write_alarm_and_style("control", prefix=enum_prefix1)

        format = self.adl.get("format", "decimal")
        lookup = {"decimal": f"{enum_prefix2}::Fixed",
                  "exponential": f"{enum_prefix2}::Scientific",
                  "engr. notation": f"{enum_prefix2}::Scientific",
                  "compact": f"{enum_prefix2}::Automatic"}
        self.write_enum("notation", lookup.get(format, f"{enum_prefix2}::Fixed"))
        self.write_bool("allowDrop", True)
        self.write_enum("dropOption", f"{enum_prefix1}::DropToTextAndWrite")


# ------------------------------------------------------------------------------
#
class QENumericEdit(QWidget):

    def write_properties(self):
        if self.qe_version == FrameworkVersion.v3:
            enum_prefix = "QEAbstractWidget"
        elif self.qe_version == FrameworkVersion.v4:
            enum_prefix = "QE"
        else:
            raise ValueError(f"QENumericEdit: unexpected version {self.qe_version}")

        self.write_pv_name("control")
        self.write_alarm_and_style("control", prefix=enum_prefix)
        self.write_bool("autoScale", True)

        # Hopefully the database designed as defined control min, max and precision
        # Define, hopefully, workable fallbacks
        #
        self.write_number("leadingZeros", 6)
        self.write_number("precision", 6)
        self.write_double("minimum", 999999.999999)
        self.write_double("maximum", 999999.999999)
        self.write_bool("addUnits", False)


# ------------------------------------------------------------------------------
#
class QEAnalogSlider(QWidget):

    def write_properties(self):
        self.write_enum("frameShape", "QFrame::Box")
        self.write_enum("frameShadow", "QFrame::Sunken")
        self.write_pv_name("control")
        self.write_alarm_and_style("control")
        self.write_bool("showSaveRevert", False)
        self.write_bool("showApply", False)
        self.write_bool("continuousWrite", True)


# ------------------------------------------------------------------------------
# PV writer
class QEPushButton(QWidget):

    def write_properties(self):
        if self.qe_version == FrameworkVersion.v3:
            enum_prefix = "QEPushButton"
        elif self.qe_version == FrameworkVersion.v4:
            enum_prefix = "QE"
        else:
            raise ValueError(f"QELabel: unexpected version {self.qe_version}")

        self.write_pv_name("control")
        self.write_alarm_and_style("control")

        label = self.adl.get("label", None)
        if label is not None:
            self.write_stdset_string("labelText", label)

        press_text = self.adl.get("press_msg", None)
        self.write_bool("writeOnPress", press_text is not None)
        if press_text is not None:
            self.write_string("pressText", press_text)

        release_text = self.adl.get("release_msg", None)
        self.write_bool("writeOnRelease", release_text is not None)
        if release_text is not None:
            self.write_string("releaseText", release_text)

        # MEDM does not support click
        # Help manual change-aroo by prefilling in click text
        #
        self.write_bool("writeOnClick", False)
        if release_text is not None:
            self.write_string("clickText", release_text)

        # Examine pres/release messages.
        # Are they both integer or floating.
        #
        format = f"{enum_prefix}::Default"

        if press_text is not None or release_text is not None:
            # At leat one defined.
            # Check integer first
            #
            if format == f"{enum_prefix}::Default":
                try:
                    if press_text is not None:
                        int(press_text)
                    if release_text is not None:
                        int(release_text)

                    # No exception
                    format = f"{enum_prefix}::Integer"
                except BaseException:
                    # Not int - so try float.
                    pass

            if format == f"{enum_prefix}::Default":
                try:
                    if press_text is not None:
                        float(press_text)
                    if release_text is not None:
                        float(release_text)

                    # No exception
                    format = f"{enum_prefix}::Floating"
                except BaseException:
                    # Not float - so stick with default.
                    pass

        self.write_enum("format", format)


# ------------------------------------------------------------------------------
#
class QEComboBox(QWidget):

    def write_properties(self):
        self.write_pv_name("control")
        self.write_alarm_and_style("control")


# ------------------------------------------------------------------------------
#
class QERadioGroup(QWidget):

    def write_properties(self):
        if self.qe_version == FrameworkVersion.v3:
            enum_prefix = "QERadioGroup"
            ep2 = "QEAbstractWidget"
        elif self.qe_version == FrameworkVersion.v4:
            enum_prefix = "QE"
            ep2 = "QE"
        else:
            raise ValueError(f"QERadioGroup: unexpected version {self.qe_version}")

        self.write_pv_name("control")
        self.write_alarm_and_style("control", prefix=ep2)

        stacking = self.adl.get("stacking", "row")
        lookup = {"row": 1,
                  "column": 16,
                  # medm is dynamic 2 to 4, 3 is a good balance
                  "row column": 3}

        self.write_stdset_string("title", "")
        self.write_number("columns", lookup[stacking])
        self.write_number("spacing", 0)
        self.write_enum("buttonStyle", "QRadioGroup::Push")
        self.write_enum("buttonOrder", f"{enum_prefix}::colMajor")


# ------------------------------------------------------------------------------
#
class QEMenuButton (QWidget):

    @property
    def _is_singular_item(self):
        # Look for display entries or command entires, we  expect one or the other
        #
        total = 0

        # Look for related displays.
        #
        for index in range(16):
            key = f"display[{index}]"
            item = self.adl.get(key, None)
            if item is None:
                continue

            # Allow empty labels

            filename = item.get("name", None)
            if filename is None:
                continue

            # Found an valid entry
            #
            total += 1

        # Similar - look for run commands.
        #
        for index in range(16):
            key = f"command[{index}]"
            item = self.adl.get(key, None)
            if item is None:
                continue

            # Allow empty labels

            command = item.get("name", None)
            if command is None:
                continue

            # Found an entry
            #
            total += 1

        return total == 1

    @property
    def classname(self):
        if self._is_singular_item:
            return "QEPushButton"

        return self.__class__.__name__

    def write_properties(self):
        if self._is_singular_item:
            self.write_push_button_properties()
        else:
            self.write_menu_button_properties()

    def write_menu_button_properties(self):
        button_label = self.adl.get("label", "")
        if button_label is not None:
            #
            if button_label.startswith("-"):
                button_label = button_label[1:]
            else:
                # Add "icon" - QEMenuButton has not icon option use use #
                button_label = "#" + button_label

            # QEMenuButton does not like null strings - see ACC 155
            #
            if len(button_label) == 0:
                button_label = " "

            self.write_stdset_string("labelText", button_label)

        fcn = self.adl.get("clr", None)
        bcn = self.adl.get("bclr", None)
        defaultStyle = adl2colour.get_style(bcn, fcn)
        self.write_stdset_string("defaultStyle", defaultStyle)

        menuEntries = '<MenuButton Version="1">\n'

        # We expect one or the other
        #
        for index in range(16):
            key = f"display[{index}]"
            item = self.adl.get(key, None)
            if item is None:
                continue

            label = item.get("label", None)
            if label is None:
                # Allow emptpy labels
                label = button_label

            filename = item.get("name", None)
            if filename is None:
                continue

            parts = os.path.splitext(filename)
            uifile = parts[0] + ".ui"
            subtitutions = item.get("args", "")
            policy = item.get("policy", None)
            if policy == "replace display":
                policy = "Open"
            else:
                policy = "NewWindow"

            element = """\
    <Item Name="{label}">
        <Window>
            <UiFile>{uifile}</UiFile>
            <MacroSubstitutions>{subtitutions}</MacroSubstitutions>
            <Customisation></Customisation>
            <Create_Option>{policy}</Create_Option>
        </Window>
    </Item>
"""
            menuEntries += element.format(label=escape(label),
                                          uifile=escape(uifile),
                                          subtitutions=escape(subtitutions),
                                          policy=policy)

        # end loop

        # Similar
        #
        for index in range(16):
            key = f"command[{index}]"
            item = self.adl.get(key, None)
            if item is None:
                continue

            label = item.get("label", None)
            if label is None:
                # Allow emptpy labels
                label = button_label
            command = item.get("name", None)
            if command is None:
                continue
            args = item.get("args", "")

            element = """\
    <Item Name="{label}">
        <Program>
            <Name>{command}</Name>
            <Arguments>{args}</Arguments>
            <Start_Option>StdOut</Start_Option>
        </Program>
    </Item>
"""
            menuEntries += element.format(label=escape(label),
                                          command=escape(command),
                                          args=escape(args))
        # end loop

        menuEntries += "</MenuButton>"
        self.write_stdset_string("menuEntries", menuEntries)

    def write_push_button_properties(self):
        # The first part is essentially the same.
        #
        button_label = self.adl.get("label", "")
        if button_label is not None:
            #
            if button_label.startswith("-"):
                button_label = button_label[1:]
            else:
                # Add "icon" - QEMenuButton has not icon option use use #
                button_label = "#" + button_label

            # QEMenuButton does not like null strings - see ACC 155
            #
            if len(button_label) == 0:
                button_label = " "

            self.write_stdset_string("text", button_label)

        fcn = self.adl.get("clr", None)
        bcn = self.adl.get("bclr", None)
        defaultStyle = adl2colour.get_style(bcn, fcn)
        self.write_stdset_string("defaultStyle", defaultStyle)

        # We expect one or the other
        #
        for index in range(16):
            key = f"display[{index}]"
            item = self.adl.get(key, None)
            if item is None:
                continue

            label = item.get("label", None)
            if label is None:
                # Allow emptpy labels
                label = button_label

            filename = item.get("name", None)
            if filename is None:
                continue

            # Found it
            #
            parts = os.path.splitext(filename)
            uifile = parts[0] + ".ui"
            subtitutions = item.get("args", "")
            policy = item.get("policy", None)
            if policy == "replace display":
                policy = "Open"
            else:
                policy = "NewWindow"

            self.write_string("guiFile", uifile)
            self.write_string("creationOption", policy)
            self.write_string("prioritySubstituins", subtitutions)

            break

        # end loop

        # Similar
        #
        for index in range(16):
            key = f"command[{index}]"
            item = self.adl.get(key, None)
            if item is None:
                continue

            label = item.get("label", None)
            if label is None:
                # Allow emptpy labels
                label = button_label

            command = item.get("name", None)
            if command is None:
                continue
            args = item.get("args", "")
            args = args.split()

            # Found it
            #
            self.write_string("program", command)
            self.write_string_list("arguments", args)
            self.write_string("programStartupOption", "QEPushButton::StdOutput")

            break

        # end loop


# ------------------------------------------------------------------------------
# We use a QEFrame as opposed to just a QFrame - more flexible post conversion
# composite may also be am embedded file
#
class QEFrame (QWidget):

    def write_properties(self):

        self.write_enum("frameShape", "QFrame::NoFrame")
        self.write_enum("frameShadow", "QFrame::Plain")

        own_geo = self.adl.get("object", None)
        children = self.adl.get("children", None)

        if children is not None:
            for key, child_adl in children.items():

                child_type = child_adl.get("class_type", None)
                child_class = _widget_map.get(child_type, None)

                if child_class is None:
                    print("QEFrame: unknown child type: %s %-8s - ignored" % (key, child_type))
                else:
                    item = child_class(child_adl, self.target, self.level + 1)
                    item.write_widget(own_geo)


# ------------------------------------------------------------------------------
#
class QEForm (QWidget):

    def write_properties(self):
        composite_file = self.adl.get("composite file", "")
        if composite_file:
            # file name proper and any macros separated by a ';'
            #
            parts = composite_file.split(";")

            # Split on '.' as in xxxx.adl
            #
            name_parts = os.path.splitext(parts[0])
            uifile = name_parts[0] + ".ui"
            self.write_stdset_string("uiFile", uifile)

            if len(parts) >= 2:
                # Macros are defined.
                #
                subs = parts[1]
                self.write_stdset_string("variableSubstitutions", subs)


# ------------------------------------------------------------------------------
#
def select_frame_form(adl, target, level):
    """ Has the same signature, sans self, as the widget classes.
    """
    children = adl.get("children", None)
    composite_file = adl.get("composite file", None)
    if children is None and composite_file is not None:
        return QEForm(adl, target, level)

    if children is not None and composite_file is None:
        return QEFrame(adl, target, level)

    print("QEForm/QEFrame ambiguity")
    return None


# ------------------------------------------------------------------------------
#
class UiFile (QWidget):
    """ Quazi widget """

    def write_widget(self):

        header = """\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>{width}</width>
    <height>{height}</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>{title}</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <property name="leftMargin">
    <number>0</number>
   </property>
   <property name="topMargin">
    <number>0</number>
   </property>
   <property name="rightMargin">
    <number>0</number>
   </property>
   <property name="bottomMargin">
    <number>0</number>
   </property>
   <item>
    <widget class="QFrame" name="mainFormFrame">
     <property name="styleSheet">
      <string notr="true">{style}</string>
     </property>
     <property name="frameShape">
      <enum>QFrame::NoFrame</enum>
     </property>
     <property name="frameShadow">
      <enum>QFrame::Plain</enum>
     </property>
"""

        footer = """
    </widget>
   </item>
  </layout>
 </widget>
</ui>
"""

        object_name_reset()
        assert isinstance(self.adl, dict), "adl argument is not a dictionary"

        # Extract name
        #
        file_info = self.adl.get("file", None)
        if file_info:
            filename = file_info.get("name", None)
            filename = os.path.basename(filename)
            parts = os.path.splitext(filename)
            title = parts[0] + ".ui"
        else:
            title = "unknown.ui"

        # Process the colours
        #
        cmap = self.adl.get("color map", None)
        assert cmap is not None, "adl missing color map"

        colors = cmap.get("colors", None)
        assert isinstance(colors, list), "adl.color map missing colors or not a list"

        adl2colour.set_colour_map(colors)

        # Process the display size and colour parameters.
        #
        display = self.adl.get("display", None)
        assert display is not None, "adl missing display"

        geo = display.get("object", None)
        assert geo is not None, "adl.display missing object"

        width = QWidget.scale(geo["width"])
        height = QWidget.scale(geo["height"])

        fcn = display.get("clr", None)
        bcn = display.get("bclr", None)
        style = adl2colour.get_style(bcn, fcn)

        if QWidget.default_colours:
            style = ""

        self.target.write(header.format(title=title, width=width,
                                        height=height, style=style))

        # This bit similar to QEFrame
        #
        for key, value in self.adl.items():
            if key in ("file", "display", "color map"):
                # specials already handled
                continue

            if not isinstance(value, dict):
                print(f"value {value}")
                value = {}
            class_type = value.get("class_type", None)
            item_class = _widget_map.get(class_type, None)
            if item_class is None:
                print("UiFile:  unknown class_type: %s %-8s - ignored" % (key, class_type))
            else:
                item = item_class(value, self.target, self.level + 5)
                item.write_widget()

        self.target.write(footer)

    def write_properties(self):
        raise Exception(self.classname + ".write_properties() - unexpected call.")


# ------------------------------------------------------------------------------
#
def dump_to_file(filename, adl_dic, scale, font_size,
                 default_colours, alarm_state_option, macro_name,
                 qe_version):
    """
    filename : target ui file name
    adl_dic : dictionary from the adl file
    scale : scale factor (percentage)
    font_size : the required font size
    default_colours : when True use the QE framework default colours
                      exceptions are ...
    macro_name :
    qe_version : framework version.
    """
    try:
        out_file = open(filename, 'w')
    except IOError:
        print("Cannot create file: " + filename)
        return None

    # Quazi globals - stored in the QWidget class
    #
    QWidget.m = int(scale)
    QWidget.d = int(100)
    QWidget.font_size = font_size
    QWidget.default_colours = default_colours
    QWidget.alarm_state_option = alarm_state_option
    QWidget.macro_name = macro_name
    QWidget.qe_version = qe_version

    ui_file = UiFile(adl_dic, out_file, 0)
    ui_file.write_widget()
    out_file.close()


# ------------------------------------------------------------------------------
# autopep8: off
#
_widget_map = {
    "composite":       select_frame_form,
    "text":            QESubstitutedLabel,
    "rectangle":       QSimpleShape,
    "oval":            QSimpleShape,
    "arc":             QSimpleShape,
    "image":           QFrame,
    "text update":     QELabel,
    "byte":            QEBitStatus,
    "meter":           QEAnalogProgressBar,
    "bar":             QEAnalogProgressBar,
    "indicator":       QEAnalogProgressBar,
    "strip chart":     QEPlot,
    "cartesian plot":  QEPlotter,
    "text entry":      QELineEdit,
    "message button":  QEPushButton,
    "menu":            QEComboBox,
    "valuator":        QENumericEdit,
    "choice button":   QERadioGroup,
    "related display": QEMenuButton,
    "shell command":   QEMenuButton
}

# autopep8: on

# end
