'''
Script 02 to remove unwanted elements/attributes from XML.
- processes element by element of the input XML-file
- only operations per element are possible
'''
import xml.etree.ElementTree as ET
from pathlib import Path
import time
import datetime
import os


#INPUT_FILE_NAME =        "Daten_00.osm"            # for test purposes
INPUT_FILE_NAME =         "Daten_01.output"         # file: Daten_01
PATH = str(Path(__file__).parent.resolve()) + "\\"  # path to file Daten_01 (current directory)
FILE_IN_NAME  = PATH + INPUT_FILE_NAME
FILE_OUT_NAME = PATH    + "Daten_02.output"         # file: Daten_02
REPORT_FILE_NAME = PATH + "Daten_02-REPORT.output"


#-------------------------------------------------------------------------------
# Class
#-------------------------------------------------------------------------------
class Report:
    '''Report measurements'''
    function_name = ""
    file_name_in  = ""
    file_name_out  = ""
    file_report = ""
    file_size_begin = 0
    file_size_end = 0
    time_begin = 0
    time_end = 0

    def __init__(self, function_name, file_name_in, file_name_out, file_name_report):
        """Init method"""
        self.function_name = function_name
        self.file_name_in = file_name_in
        self.file_name_out = file_name_out
        self.file_size_begin = Path(file_name_in).stat().st_size
        self.file_report = open(file_name_report, "w")
        # start measurement
        self.time_begin = round(time.time() * 1000)

    def get_file_name_out(self):
        '''Get output file name '''
        return self.file_name_out

    def savings_byte(self):
        '''Difference between input- and output-file in byte'''
        return self.file_size_begin - self.file_size_end

    def savings_percent(self):
        '''Difference between input- and output-file in percent'''
        savings = 100 - (self.file_size_end/self.file_size_begin) * 100
        savings = round(savings, 1)
        return savings

    def time_used_ms(self):
        '''Time between start and end of measurement'''
        return self.time_end - self.time_begin

    def stop_measurement(self):
        '''End of measurement, stop time and get file size'''
        self.time_end = round(time.time() * 1000)
        self.file_size_end = Path(self.file_name_out).stat().st_size

    def convert_ms(self):
        time_used = datetime.datetime.fromtimestamp(self.time_used_ms()/1000.0,
                                                    tz=datetime.timezone.utc)
        return "time used      :   " + time_used.strftime('%H:%M:%S.%f') + "\n"

    def convert_bytes(self, bytes, indent=True):
        '''Convert bytes to kB or MB'''
        result = ""
        kilo = 1024
        indent_x ="           "

        # return bytes
        if bytes < kilo:
            result = "byte:   " + str(bytes) + "\n"
        # return kilo bytes
        elif bytes >= kilo and bytes < (kilo*kilo):
            kb = round(bytes/kilo, 1)
            result = "  kB:   " + str(kb) + "\n"
        # return mega bytes
        else:
            mb = round(bytes/(kilo*kilo), 1)
            result = "  MB:   " + str(mb) + "\n"

        if indent:
            result = indent_x + result
        return result

    def write_report(self):
        '''Write result into report file'''
        self.stop_measurement()

        self.file_report.write(">>>>>> " + self.function_name + " <<<<<<\n")
        #directory = os.path.dirname(self.file_name_in)
        file_in = os.path.basename(self.file_name_in)
        #file_out = os.path.basename(self.file_name_out)
        #self.file_report.write("directory:         " + directory + "\n")
        self.file_report.write("input file name:   " + file_in + "\n")
        self.file_report.write(self.convert_bytes(self.file_size_begin))
        #self.file_report.write("output file name:  " + file_out + "\n")
        #self.file_report.write(self.convert_bytes(self.file_size_end))
        self.file_report.write("Savings    ")
        self.file_report.write(self.convert_bytes(self.savings_byte(), False))
        self.file_report.write("     in percent:   " + str(self.savings_percent()) + "\n")
        self.file_report.write(self.convert_ms() + "\n")
        self.file_report.close()

#-------------------------------------------------------------------------------
class Counter:
    '''Counts all first level elements per type'''
    def __init__(self):
        """Init method"""
        self.counters = dict()

    def count_elements_per_type(self, element):
        '''Count elements per first level element type'''
        if element.tag in self.counters.keys():
            # increase counter
            current_value = self.counters[element.tag]
            self.counters[element.tag] = current_value + 1
        else:
            # add to dictionary and increase counter
            self.counters[element.tag] = 1

    def print_counter_results(self):
        '''Print number of first level elements per type'''
        number_elements = 0
        for key, value in self.counters.items():
            print("number of " + key + ": " + str(value))
            number_elements = number_elements + value

        print("number of elements: " + str(number_elements))

#-------------------------------------------------------------------------------
class Timer:
    '''Timer for performance measurements'''
    def __init__(self, function_name):
        """Init method"""
        self.function_name = function_name
        self.time_begin = self.current_time_ms()

    def begin_time_ms(self):
        """Begin time"""
        return self.time_begin

    def current_time_ms(self):
        """Get current time"""
        return round(time.time() * 1000)

    def print_result(self, additional_information=""):
        """Print result"""
        time_end = self.current_time_ms()
        time_used = time_end - self.time_begin
        print(self.function_name, " in ms:", time_used, additional_information)
        return time_used


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    '''At a first step just count the first level elements per type'''
    report = Report(str("script_02"), FILE_IN_NAME, FILE_OUT_NAME, REPORT_FILE_NAME)
    timer = Timer("script_02")
    counter = Counter()

    print("FILE_IN_NAME:     " + FILE_IN_NAME)
    print("FILE_OUT_NAME:    " + FILE_OUT_NAME)
    print("REPORT_FILE_NAME: " + REPORT_FILE_NAME)

    number_of_deleted_relations = 0
    with open(FILE_OUT_NAME, mode="w", encoding="utf-8") as file:
        file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        file.write("<osm version='0.6' generator='JOSM'>\n  ")

        add_blank = False
        for element in get_next_first_level_element(FILE_IN_NAME):
            counter.count_elements_per_type(element)

            ################ actions ################
            route_list = ['bus','train','railway','bicycle','hiking','ferry','subway']
            restriction_list = ['no_left_turn','no_right_turn','only_left_turn',
                                'only_right_turn','only_straight_on','no_u_turn']
            type_list = ['addr:postcode','addr:city']

            tags_to_remove = dict([
                ("route", route_list),
                ("restriction", restriction_list),
                ("type", type_list)
                ])

            remove_element = is_relation_with_tag(element, tags_to_remove)
            ################ actions ################

            if remove_element:
                number_of_deleted_relations = number_of_deleted_relations + 1
            else:
                element_string = ET.tostring(element, encoding='unicode', method='xml')
                element_string, add_blank = fix_line_breaks(element_string, add_blank)

                # replace " with ' (orginal setting)
                #element_string = element_string.replace("\"", "'")
                # <tag k='operator' v='McDonald&apos;s' />   original
                # <tag k='operator' v='McDonald's' />        output
                #
                # now:
                # <tag k="operator" v="McDonald's" />        output

                file.write(element_string)
                file.flush()

        file.write('</osm>' + "\n")
        file.close()
    counter.print_counter_results()
    print("deleted relations: " + str(number_of_deleted_relations))
    timer.print_result()
    report.write_report()


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def fix_line_breaks(element_string, add_blank):
    # add blank for the right indentation
    if add_blank:
        element_string = "  " + element_string
        add_blank = False

    # sometimes no line break is added to the element_string
    index = element_string[-4:].find("\n")
    if index == -1:
        # add line break
        element_string = element_string + "\n"
        # make sure the next element_string has the right indentation
        add_blank = True

    return element_string, add_blank

#-------------------------------------------------------------------------------
def get_next_first_level_element(file_in):
    '''
    Incrementally parse XML document into ElementTree.
    Return one "first level"-element after the other, until end of file.
    '''
    context = ET.iterparse(file_in, events=("start", "end"))
    for event, element in context:
        # do not stop for subelements
        if event == 'end' and (element.tag != "tag" and
                               element.tag != "nd" and
                               element.tag != "member" and
                               element.tag != "osm"):
            yield element

#-------------------------------------------------------------------------------
    '''
    Check given list for relations to be removed
    '''
def is_relation_with_tag(element, tags_to_remove):
    found = False
    if element.tag == "relation":
        # for each tag in relation
        for subelement in element.findall("tag"):
            # is the key in the dictionary and
            # is the value in the list?
            list = tags_to_remove.get(subelement.attrib.get("k"))
            if (list != None) and (subelement.attrib.get("v") in list):
                found = True
                break
    return found

#-------------------------------------------------------------------------------
if __name__== "__main__":
    main()
