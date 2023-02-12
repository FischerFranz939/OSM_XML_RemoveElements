import xml.etree.ElementTree as ET
import pathlib


input_file_name = "test3.xml"
#input_file_name = "andorra-latest.osm"


#-------------------------------------------------------------------------------
def getelements(xml_file_in, tag):
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
print("currentdir: ", current_dir)

xml_file_in = current_dir + "\\..\\test\\" + input_file_name
xml_file_out = current_dir + "\\" + input_file_name + ".output"
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
