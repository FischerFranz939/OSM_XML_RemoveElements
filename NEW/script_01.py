'''
Script to remove unwanted elements/attributes from XML.
- processes element by element of the input XML-file
- only operations per element are possible
'''
import xml.etree.ElementTree as ET
from pathlib import Path
import time
import inspect


INPUT_FILE_NAME = "test_00.osm"
TEST_PATH = str(Path(__file__).parent.resolve()) + "/"
FILE_IN  = TEST_PATH + INPUT_FILE_NAME
FILE_OUT = FILE_IN + ".output"


#-------------------------------------------------------------------------------
# Class
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
    counter = Counter()

    with open(FILE_OUT, mode="w", encoding="utf-8") as file:
        file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        file.write("<osm version='0.6' generator='JOSM'>\n  ")

        add_blank = False
        for element in get_next_first_level_element(FILE_IN):
            counter.count_elements_per_type(element)

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
def remove_attribute_from_element(root, target_attribute):
    '''Remove attribute from element'''
    timer = Timer(str(inspect.stack()[0][3]))
    x_path = "./*[@" + target_attribute + "]"
    for element in root.findall(x_path):
        #print(element.attrib[target_attribute])
        del element.attrib[target_attribute]
    timer.print_result()

#-------------------------------------------------------------------------------
def remove_attributes_from_element(root, target_attributes):
    '''Remove attributes from element'''
    timer = Timer(str(inspect.stack()[0][3]))
    for target_attribute in target_attributes:
        remove_attribute_from_element(root, target_attribute)
    timer.print_result()

#-------------------------------------------------------------------------------
if __name__== "__main__":
    main()
