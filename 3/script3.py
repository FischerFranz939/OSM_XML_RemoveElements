from tkinter import END
import xml.etree.ElementTree as ET


xml_file_in = "test1.xml"
#xml_file_in = "andorra-latest.osm"
xml_file_out = "output.xml"


def getelements(xml_file_in, tag):
    context = iter(ET.iterparse(xml_file_in, events=('start', 'end')))
    _, root = next(context) # get root element
    for event, elem in context:
        if event == 'end' and (elem.tag != tag and elem.tag != "osm"):
            yield elem
            root.clear() # free memory


counter = 0
with open(xml_file_out, mode="w", encoding="utf-8", newline="\n") as file:
    file.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    file.write("<osm version='0.6' generator='JOSM'>\n  ")

    for page in getelements(xml_file_in, "tag"):
        file.write(ET.tostring(page, encoding='unicode', method='xml'))
        counter = counter + 1

    file.write("</osm>")

    print(counter)
