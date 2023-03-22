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


#INPUT_FILE_NAME = "test2.xml"
#INPUT_FILE_NAME = "test3.xml"
#INPUT_FILE_NAME = "Neuffen_unbearbeitet.osm"
#INPUT_FILE_NAME = "Neuffen_unbearbeitet_formated_win.osm"
INPUT_FILE_NAME = "Neuffen_unbearbeitet_formated_lin.osm"
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
        for key, value in self.counters.items():
            print("number of " + key + ": " + str(value))


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    '''At a first step just count the first level elements per type'''
    numberOfElements = 0
    counter = Counter()

    #windows_line_endings = b'\r\n'
    #linux_line_endings = b'\n'
    space = b' />'
    no_space = b'/>'

    with open(FILE_OUT, mode="wb") as file:
    #with open(FILE_OUT, mode="wb", encoding="utf-8", newline="\n") as file:
        file.write(b"<?xml version='1.0' encoding='UTF-8'?>\n")
        file.write(b"<osm version='0.6' generator='JOSM'>\n  ")

        for element in get_next_first_level_element(FILE_IN):
            numberOfElements = numberOfElements + 1
            counter.count_elements_per_type(element)

            #print("----------------------")
            #print(element.tag)
            #print(element.attrib)
            #element_string = ET.tostring(element, encoding='unicode', method='xml')
            byte_str = ET.tostring(element)
            #byte_str = byte_str.replace(windows_line_endings, linux_line_endings)
            #byte_str = byte_str.replace(b'/><node', b'/>\n<node')
            byte_str = byte_str.replace(space, no_space)

            file.write(byte_str)
            file.flush()

        file.write(b'</osm>')
        file.close()
        counter.print_counter_results()
        print("numberOfElements: " + str(numberOfElements))


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def get_next_first_level_element(file_in):
    '''
    Incrementally parse XML document into ElementTree.
    Return one "first level"-element after the other, until end of file.
    '''
    context = iter(ET.iterparse(file_in, events=('start', 'end')))
    _, root = next(context) # get root element

    for event, element in context:
        # do not stop for subelements
        if event == 'end' and (element.tag != "tag" and
                               element.tag != "nd" and
                               element.tag != "member" and
                               element.tag != "osm"):
            yield element
            root.clear() # free memory

#-------------------------------------------------------------------------------
if __name__== "__main__":
    main()
