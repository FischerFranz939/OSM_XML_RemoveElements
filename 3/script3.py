'''
Script to remove unwanted elements/attributes from XML.
- processes element by element of the input XML-file
- currently: "only" count elements
- only operations per element are possible
'''
import xml.etree.ElementTree as ET
import pathlib


INPUT_FILE_NAME = "test3.xml"
#INPUT_FILE_NAME = "andorra-latest.osm"


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def getelements(xml_file, tag):
    '''Get elements'''
    context = iter(ET.iterparse(xml_file, events=('start', 'end')))
    _, root = next(context) # get root element
    for event, elem in context:
        if event == 'end' and (elem.tag != tag and elem.tag != "osm"):
            yield elem
            root.clear() # free memory


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
CURRENT_DIR = str(pathlib.Path(__file__).parent.resolve())
print("CURRENT_DIR: ", CURRENT_DIR)

XML_FILE_IN = CURRENT_DIR + "\\..\\test\\" + INPUT_FILE_NAME
XML_FILE_OUT = CURRENT_DIR + "\\" + INPUT_FILE_NAME + ".output"
print("XML_FILE_IN: ", XML_FILE_IN)
print("XML_FILE_OUT: ", XML_FILE_OUT)

COUNTER = 0
with open(XML_FILE_OUT, mode="w", encoding="utf-8", newline="\n") as file:
    file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    file.write("<osm version='0.6' generator='JOSM'>\n  ")

    for page in getelements(XML_FILE_IN, "tag"):
        file.write(ET.tostring(page, encoding='unicode', method='xml'))
        COUNTER = COUNTER + 1

    file.write("</osm>")

    print(COUNTER)
