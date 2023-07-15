'''
Script to remove unwanted elements/attributes from XML.
- processes element by element of the input XML-file
- currently: "only" count elements
- only operations per element are possible

TODO:
- sometimes line breaks are missing


'''
import xml.etree.ElementTree as ET
from pathlib import Path


#INPUT_FILE_NAME = "test2_formated.xml"
#INPUT_FILE_NAME = "test3.xml"
INPUT_FILE_NAME = "Neuffen_unbearbeitet.osm"
#INPUT_FILE_NAME = "Neuffen_unbearbeitet_formated_win.osm"
#INPUT_FILE_NAME = "Neuffen_unbearbeitet_formated_lin.osm"
#INPUT_FILE_NAME = "andorra-latest.osm"

TEST_PATH = str(Path(__file__).parent.resolve()) + "/../test/"
FILE_IN  = TEST_PATH + INPUT_FILE_NAME
FILE_OUT = FILE_IN + "-script3.output"


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

        print("number_elements: " + str(number_elements))


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    '''At a first step just count the first level elements per type'''
    counter = Counter()

    windows_line_endings = '\r\n'
    linux_line_endings = '\n'

    with open(FILE_OUT, mode="w", encoding="utf-8") as file:
        file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        file.write("<osm version='0.6' generator='JOSM'>\n  ")

        add_blancs = False
        for element in get_next_first_level_element(FILE_IN):
            counter.count_elements_per_type(element)

            element_string = ET.tostring(element, encoding='unicode', method='xml')

            # add blancs for the right indentation
            if add_blancs:
                element_string = "  " + element_string
                add_blancs = False

            # sometimes no line break is added to the element_string
            index = element_string.find("\n")
            if index == -1:
                # add line break
                element_string = element_string + "\n"
                # make sure the next element_string has the right indentation
                add_blancs = True

            # replace " with ' (orginal setting)
            element_string = element_string.replace("\"", "'")

            file.write(element_string)
            file.flush()

        file.write('</osm>' + "\n")
        file.close()
        counter.print_counter_results()

#-------------------------------------------------------------------------------
# Functions
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
if __name__== "__main__":
    main()
