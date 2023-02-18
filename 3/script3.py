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
def getelements(xml_file_in, tag):
    '''Get elements'''
    context = iter(ET.iterparse(xml_file_in, events=('start', 'end')))
    _, root = next(context) # get root element
    for event, elem in context:
        if event == 'end' and (elem.tag != tag and elem.tag != "osm"):
            yield elem
            root.clear() # free memory


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
current_dir = str(pathlib.Path(__file__).parent.resolve())
print("current_dir: ", current_dir)

xml_file_in = current_dir + "\\..\\test\\" + INPUT_FILE_NAME
xml_file_out = current_dir + "\\" + INPUT_FILE_NAME + ".output"
print("xml_file_in: ", xml_file_in)
print("xml_file_out: ", xml_file_out)


counter = 0
with open(xml_file_out, mode="w", encoding="utf-8", newline="\n") as file:
    file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    file.write("<osm version='0.6' generator='JOSM'>\n  ")

    for page in getelements(xml_file_in, "tag"):
        file.write(ET.tostring(page, encoding='unicode', method='xml'))
        counter = counter + 1

    file.write("</osm>")

    print(counter)
