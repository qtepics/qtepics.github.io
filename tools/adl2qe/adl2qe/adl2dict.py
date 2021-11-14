# $File: //ASP/tec/gui/qtepics.github.io/trunk/tools/adl2qe/adl2qe/adl2dict.py $
# $Revision: #2 $
# $DateTime: 2021/11/14 10:36:34 $
# Last checked in by: $Author: starritt $
#

""" This module converts an MEDM adl file to a dictionary.
"""

import os.path
import json


def no_quote_find(text, sub):
    """ This is like  text.find(sub) except that ingores sub if found within " "
        Note: not general purpose
    """
    result = text.find(sub)
    if result >= 0:
        quote1 = text.find('"')
        if quote1 >= 0:
            quote2 = text.find('"', quote1 + 1)
            if quote2 >= 0:
                if quote1 < result < quote2:
                    result = -1

    return result


def load_file(filename):
    """
    :param filename: source .adl file
    :return: dictionary or None

    Reads the contents of the file filename and converts this to a json string
    which is then converted to a dictionary using json.loads

    Note: much the input is of the form, e.g:

    text {
        object {
            x=40
            y=203
            width=200
            height=42
        }
        "basic attribute" {
            clr=22
        }
        textix="RED"
        align="horiz. right"
    }

    As 'text' is a class type name, it almost certainly not unique, and a
    "simple" conversion to json would not work. The corresponding
    generated json is:

    "10012": {
        "class_type": "text",
        "object": {
            "x": 40,
            "y": 203,
            "width": 200,
            "height": 42
        },
        "basic attribute": {
            "clr": 22
        },
        "textix": "RED",
        "align": "horiz. right"
    }

    The key "10012" is auto generated. The class type is emdedded within
    the sub-dictionary with key "class_type".

    """

    # phase 1 - read file as string and split into lines.
    #
    if (not os.path.isfile(filename)):
        print(filename + ": does not exists or is not a file")
        return None

    try:
        f = open(filename, 'r')
    except IOError:
        print("Cannot open file: " + filename)
        return None

    lines = f.read().splitlines()

    f.close()

    # phase 2 - convert to a json string, well strictly a list of
    # json stringlets
    #
    jsl = []
    jsl.append("{")
    lineno = 0
    number = 10000
    class_type = None
    indent = 3
    for line in lines:
        lineno += 1
        line = line.strip()

        if len(line) == 0:
            continue

        # lines are of the form:
        #
        #  classname  {    or "class name" {
        #  keyname=value, or keyname[index]=value  or "key name"=value  etc
        #  value,          -- color - the colour map
        #  (int,int)       -- points - the set of polyline/polygon points
        #  }
        #
        ps = no_quote_find(line, "{")
        pe = no_quote_find(line, "=")
        pf = no_quote_find(line, "}")

        if (ps >= 0 and pe >= 0) or (pe >= 0 and pf >= 0) or (pf >= 0 and ps >= 0):
            print("Two or more key chars on line %d: %s" % (lineno, line))
            return None

        if ps >= 0:
            class_type = line[:ps].replace('"', '').strip()
            if class_type in _class_type_names:

                # Not unique - need to allocate an id.
                #
                number += 1
                jsl.append('%s"%d": {' % (indent * " ", number))
                indent += 3
                jsl.append('%s"class_type": "%s",' % (indent * " ", class_type))

            elif class_type in ("colors", "points"):
                jsl.append('%s"%s": [' % (indent * " ", class_type))
                indent += 3

            else:
                # Just a regular sub dictionary
                jsl.append('%s"%s": {' % (indent * " ", class_type))
                indent += 3

            continue

        if pf >= 0:
            _comma_pop(jsl)
            indent -= 3
            if class_type in ("colors", "points"):
                jsl.append('%s],' % (indent * " "))
                class_type = None
            else:
                jsl.append('%s},' % (indent * " "))
            continue

        if pe >= 0:
            key_name = line[:pe].replace('"', '').strip()
            value = line[pe + 1:].strip()

            # The adl format is in generat what we hat, i.e. strings are
            # quotes, numers are not. There are some specials.
            #
            if key_name == "version":
                # Trim of leading zero 030107 => 030107
                #
                value = value[1:]

            if class_type == "file" and key_name == "name":
                # Convert windoze style to Linux style (or vice versa)
                #
                value = value.replace('\\', '/')

            # value may be a string,  where the quotes are part of the string,
            # something like:          " foo " bar"
            # We neet to update to be: " foo \" bar"
            # Also string may contain \ characters - replace with \\ pairs.
            #
            # Does value start and end with a '"'
            #
            if value[:1] == '"' and value[-1:] == '"':
                # Yes - dequote, escape - note the double \\ - and re-quote.
                #
                temp = value[1:-1]
                temp = temp.replace('\\', '\\\\')
                temp = temp.replace('"', '\\"')
                value = '"' + temp + '"'

            jsl.append('%s"%s": %s,' % (indent * " ", key_name, value))
            continue

        # just a line
        #
        if class_type == "colors":
            value = line.strip()[:-1]
            jsl.append('%s   "%s",' % (indent * " ", value))
            continue

        if class_type == "points":
            value = line.strip()
            value = value.replace("(", "[")
            value = value.replace(")", "]")
            jsl.append('%s   %s,' % (indent * " ", value))
            continue

        print("unmatched [%s] %s:%s  %s" % (class_type, filename, lineno, line))

    _comma_pop(jsl)
    jsl.append("}")

    # phase 3 - convert list of strings to a single string.
    #
    j_string = '\n'.join(jsl)

    # phase 4 - convert json string to a structure.
    #
    result = None
    try:
        result = json.loads(j_string)
    except Exception as e:
        print("failed to load %s\n%s" % (filename, j_string))
        print(str(e))
        result = None

    return result


def _comma_pop(the_list):
    """ We always add a separator after each item.
        Before a '}' we must remove the previous un-needed/erroneous ','
    """
    last = len(the_list) - 1
    if last > 0:
        prev = the_list[last]
        if len(prev) > 0 and prev[-1:] == ",":
            the_list[last] = the_list[last][0:-1]


# These are names that can appear more than once at any one level,
# so can't be used as dictionary keys as won't be unique.
# This therefore excludes thing like file, display, object, children
#
_class_type_names = (
    "composite",
    "text",
    "rectangle",
    "text update",
    "byte",
    "meter",
    "bar",
    "indicator",
    "strip chart",
    "cartesian plot",
    "text entry",
    "message button",
    "menu",
    "valuator",
    "choice button",
    "related display",
    "shell command",
    "oval",
    "arc",
    "image",
    "polyline",
    "polygon"
)

# end
