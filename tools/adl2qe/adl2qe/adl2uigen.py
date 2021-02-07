# $File: //ASP/tec/gui/qtepics.github.io/trunk/tools/adl2qe/adl2qe/adl2uigen.py $
# $Revision: #5 $
# $DateTime: 2021/01/15 12:32:15 $
# Last checked in by: $Author: starritt $
#

"""
Note: we indent the generated xml, not because designer or qegui
needs it, but this helps with debugging.
"""

import os.path
import xml.sax.saxutils

from . import adl2colour

#------------------------------------------------------------------------------
#
class_object_counters = {}


def object_name_reset():
    global class_object_counters
    class_object_counters = {}


def gen_object_name(classname):
    assert type(classname) == str, "classname argument is not a string"

    if classname in class_object_counters:
        j = class_object_counters[classname] + 1
    else:
        j = 1

    class_object_counters.update({classname: j})
    return "%s_%03d" % (classname.lower(), j)


#-------------------------------------------------------------------------------
#
def escape(text):
    """ modified escape to do " as well as &, < and >
    """
    result = xml.sax.saxutils.escape(text)
    result = result.replace('"', "&quot;")
    return result


#------------------------------------------------------------------------------
# Python class names reflect Qt class names.
#
class QWidget (object):

    m = 10
    d = 10
    font_size = 8
    default_colours = False

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
        result = "  " * self._level
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
        self.write_line('  <rect>')
        self.write_line('    <x>{x}</x>'.format(x=x))
        self.write_line('    <y>{y}</y>'.format(y=y))
        self.write_line('    <width>{w}</width>'.format(w=w))
        self.write_line('    <height>{h}</height>'.format(h=h))
        self.write_line('  </rect>')
        self.write_line('</property>')

        self.write_line('<property name="font">')
        self.write_line('  <font>')
        self.write_line('    <pointsize>{ps}</pointsize>'.format(ps=QWidget.font_size))
        self.write_line('  </font>')
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
        self.write_line('  <string>' + escape(text) + '</string>')
        self.write_line('</property>')

    def write_stdset_string(self, name, text):
        self.write_line('<property name="' + name + '" stdset="0">')
        self.write_line('  <string>' + escape(text) + '</string>')
        self.write_line('</property>')

    def write_enum(self, name, text):
        self.write_line('<property name="' + name + '" stdset="0">')
        self.write_line('  <enum>' + escape(text) + '</enum>')
        self.write_line('</property>')

    def write_number(self, name, value):
        text = str(value)
        self.write_line('<property name="' + name + '">')
        self.write_line('  <number>' + escape(text) + '</number>')
        self.write_line('</property>')

    def write_double(self, name, value):
        text = str(value)
        self.write_line('<property name="' + name + '">')
        self.write_line('  <double>' + escape(text) + '</double>')
        self.write_line('</property>')

    def write_bool(self, name, value):
        if value:
            text = "true"
        else:
            text = "false"
        self.write_line('<property name="' + name + '">')
        self.write_line('  <bool>' + escape(text) + '</bool>')
        self.write_line('</property>\n')

    def write_colour(self, name, r, g, b, a=None):
        self.write_line('<property name="' + name + '">')
        if a is None:
            self.write_line('  <color>')
        else:
            self.write_line('  <color alpha="{a}">'.format(a=int(a)))
        self.write_line('    <red>{r}</red>'.       format(r=int(r)))
        self.write_line('    <green>{g}</green>'.   format(g=int(g)))
        self.write_line('    <blue>{b}</blue>'.     format(b=int(b)))
        self.write_line('  </color>')
        self.write_line('</property>')

    def write_pv_name(self, kind):
        """ Suitable for essentially single variable widgets.
        kind is control or monitor
        """
        common = self.adl.get(kind, None)
        if common is not None:
            if "chan" in common:
                pv_name = common["chan"]
                self.write_stdset_string("variable", pv_name)

    def write_alarm_and_style(self, kind, prefix=None):
        if prefix is None:
            prefix = self.classname

        clrmod = self.adl.get("clrmod", "static")
        lookup = {"static":   "%s::Never" % prefix,
                  "alarm":    "%s::Always" % prefix,
                  "discrete": "%s::Never" % prefix}
        self.write_enum("displayAlarmStateOption", lookup[clrmod])

        common = self.adl.get(kind, None)
        if common is not None:
            fcn = common.get("clr", None)
            bcn = common.get("bclr", None)

            if clrmod == "alarm":
                # Will set forground to black
                fcn = 14

            # If default colours specified, do NOT set colours based on the
            # original medm adl file.
            #
            if not QWidget.default_colours:            
                defaultStyle = adl2colour.get_style(bcn, fcn)
                self.write_stdset_string("defaultStyle", defaultStyle)

    def write_alignment(self, name, value):
        assert type(value) == str, "write_alignment: value is not a string"

        if value == "horiz. left":
            text = "Qt::AlignLeft"
        elif value == "horiz. right":
            text = "Qt::AlignRight"
        elif value == "horiz. centered":
            text = "Qt::AlignCenter"
        else:
            return

        self.write_line('<property name="' + name + '">')
        self.write_line('  <set>' + escape(text) + '</set>')
        self.write_line('</property>')


# ------------------------------------------------------------------------------
#
class QENoConversion (QWidget):

    class_type = "???"

    """ Default class used when no conversion is available.
    """
    @property
    def classname(self):
        # need to override the class name
        return "QLabel"

    def write_properties(self):
        self.write_string("styleSheet", "background-color: rgba(255, 160, 255, 100);")
        self.write_string("text", str(QENoConversion.class_type))
        self.write_string("alignment", "Qt::AlignCenter")


# ------------------------------------------------------------------------------
#
class QESubstitutedLabel (QWidget):

    def write_properties(self):
        text = self.adl.get("textix", "")
        self.write_stdset_string("labelText", text)

        align = self.adl.get("align", None)
        if align is not None:
            self.write_alignment("alignment", align)

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
        if not QWidget.default_colours:            
            self.write_stdset_string("styleSheet", styleSheet)


# ------------------------------------------------------------------------------
#
class QSimpleShape (QWidget):

    def write_properties(self):

        class_type = self.adl.get("class_type", None)
        lookup = {"rectangle": "QSimpleShape::rectangle",
                  "oval":      "QSimpleShape::ellipse",
                  "arc":       "QSimpleShape::pie"}
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

#------------------------------------------------------------------------------
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

            self.write_string(
                "styleSheet", "QFrame#%s { border-image: url(%s); }" % (self.object_name, url_name))


#------------------------------------------------------------------------------
#
class QELabel (QWidget):

    def write_properties(self):

        self.write_pv_name("monitor")
        self.write_alarm_and_style("monitor")

        align = self.adl.get("align", "horiz. left")
        self.write_alignment("alignment", align)

        format = self.adl.get("format", "decimal")
        lookup = {"decimal": "QELabel::Fixed",
                  "exponential": "QELabel::Scientific",
                  "engr. notation": "QELabel::Scientific",
                  "compact": "QELabel::Automatic"}
        self.write_enum("notation", lookup.get(format, "QELabel::Fixed"))


#------------------------------------------------------------------------------
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


#------------------------------------------------------------------------------
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

        if direction == "right":
            orientation = "QBitStatus::LSB_On_Right"
        elif direction == "down":
            orientation = "QBitStatus::LSB_On_Bottom"
        elif direction == "left":
            orientation = "QBitStatus::LSB_On_Left"
        elif direction == "up":
            orientation = "QBitStatus::LSB_On_Top"

        self.write_number("shift", shift)
        self.write_number("numberOfBits", number_of_bits)
        self.write_enum("Orientation", orientation)


# ------------------------------------------------------------------------------
#
class QEPlot(QWidget):

    def write_properties(self):
        self.write_enum("frameShape", "QFrame::Box")
        self.write_enum("frameShadow", "QFrame::Sunken")
        self.write_stdset_string("defaultStyle",
                                 "QWidget { background-color: #e0e0e0; color: #000000; }")
        self.write_enum("displayAlarmStateOption", "QEFrame::Never")

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
        self.write_pv_name("control")
        self.write_alarm_and_style("control", prefix="QEGenericEdit")

        format = self.adl.get("format", "decimal")
        lookup = {"decimal": "QELineEdit::Fixed",
                  "exponential": "QELineEdit::Scientific",
                  "engr. notation": "QELineEdit::Scientific",
                  "compact": "QELineEdit::Automatic"}
        self.write_enum("notation", lookup.get(format, "QELineEdit::Fixed"))
        self.write_enum("dropOption", "QEGenericEdit::DropToTextAndWrite")


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
#
class QEPushButton(QWidget):

    def write_properties(self):
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
        format = "QEPushButton::Default"

        if press_text is not None or release_text is not None:
            # At leat one defined.
            # Check integer first
            #
            if format == "QEPushButton::Default":
                try:
                    if press_text is not None:
                        int(press_text)
                    if release_text is not None:
                        int(release_text)

                    # No exception
                    format = "QEPushButton::Integer"
                except:
                    # Not int - so try float.
                    pass

            if format == "QEPushButton::Default":
                try:
                    if press_text is not None:
                        float(press_text)
                    if release_text is not None:
                        float(release_text)

                    # No exception
                    format = "QEPushButton::Floating"
                except:
                    # Not float - so stick with default.
                    pass

        self.write_enum("format", format)


# ------------------------------------------------------------------------------
#
class QEComboBox(QWidget):

    def write_properties(self):
        self.write_pv_name("control")
        self.write_alarm_and_style("control")


#------------------------------------------------------------------------------
#
class QERadioGroup(QWidget):

    def write_properties(self):
        self.write_pv_name("control")
        self.write_alarm_and_style("control", prefix="QEAbstractWidget")

        stacking = self.adl.get("stacking", "row")
        lookup = {"row": 1,
                  "column": 16,
                  # medm is dynamic 2 to 4, 3 is a good balance
                  "row column": 3}

        self.write_stdset_string("title", "")
        self.write_number("columns", lookup[stacking])
        self.write_number("spacing", 0)
        self.write_enum("buttonStyle", "QRadioGroup::Push")
        self.write_enum("buttonOrder", "QRadioGroup::colMajor")


#------------------------------------------------------------------------------
#
class QEMenuButton (QWidget):

    def write_properties(self):

        label = self.adl.get("label", "")
        if label is not None:
            #
            if label.startswith("-"):
                label = label[1:]
            else:
                # Add "icon" - QEMenuButton has not icon option use use #
                label = "#" + label

            # QEMenuButton does not like null strings - see ACC 155
            if len(label) == 0:
                label = " "

            self.write_stdset_string("labelText", label)

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
                continue
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
                continue
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


#------------------------------------------------------------------------------
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
                child_class = _widget_map.get(child_type, QENoConversion)

                if child_class is QENoConversion:
                    print("QEFrame: unknown child type: %s %s" % (key, child_type))
                    QENoConversion.class_type = child_class

                item = child_class(child_adl, self.target, self.level + 1)
                item.write_widget(own_geo)


#------------------------------------------------------------------------------
#
class QEForm (QWidget):

    def write_properties(self):
        composite_file = self.adl.get("composite file", "")
        if composite_file:
            parts = os.path.splitext(composite_file)
            uifile = parts[0] + ".ui"
            self.write_stdset_string("uiFile", uifile)


#------------------------------------------------------------------------------
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
    return QENoConversion(adl, target, level)


#------------------------------------------------------------------------------
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
        self.target.write(header.format(title=title, width=width,
                                        height=height, style=style))

        # This bit similar to QEFrame
        #
        for key, value in self.adl.items():
            if key in ("file", "display", "color map"):
                # specials already handled
                continue

            class_type = value.get("class_type", None)
            item_class = _widget_map.get(class_type, QENoConversion)
            if item_class is QENoConversion:
                print("UiFile:  unknown class_type: %s %s" % (key, class_type))
                QENoConversion.class_type = class_type

            item = item_class(value, self.target, self.level + 5)
            item.write_widget()

        self.target.write(footer)

    def write_properties(self):
        raise Exception(self.classname + ".write_properties() - unexpected call.")


#------------------------------------------------------------------------------
#
def dump_to_file(filename, adl_dic, scale, font_size, default_colours):
    """
    filename : target ui file name
    adl_dic : dictionary from the adl file
    scale : scale factor (percentage)
    font_size : the required font size
    default_colours : when True use the QE framework default colours
                      exceptions are ...
    """
    try:
        out_file = open(filename, 'w')
    except IOError:
        print("Cannot create file: " + filename)
        return None

    QWidget.m = int(scale)
    QWidget.d = int(100)
    QWidget.font_size = font_size
    QWidget.default_colours = default_colours

    ui_file = UiFile(adl_dic, out_file, 0)
    ui_file.write_widget()
    out_file.close()


#------------------------------------------------------------------------------
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
    "valuator":        QEAnalogSlider,
    "choice button":   QERadioGroup,
    "related display": QEMenuButton,
    "shell command":   QEMenuButton
}

# end
