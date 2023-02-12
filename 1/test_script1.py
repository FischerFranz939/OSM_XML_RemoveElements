# https://pythontest.com/framework/pytest/pytest-introduction/
#& "C:/Program Files/Python39/python.exe" -m pytest -v d:/MeineProgramme/OSM_XML_RemoveElements/1/test_script1.py

import xml.etree.ElementTree as ET
from script1 import remove_element_by_id


#-------------------------------------------------------------------------------
def test_remove_element_by_id():
# Given
    xml_in = """<body>
    <bounds minlat='48.5297218' minlon='9.3489575' maxlat='48.5378919' maxlon='9.3748784' origin='CGImap 0.8.6 (3984174 spike-06.openstreetmap.org)' />
    <node id='31287590' timestamp='2016-07-06T01:21:43Z' uid='548288' user='WayneSchlegel' visible='true' version='3' changeset='40512409' lat='48.5288901' lon='9.3514616' />
    <node id='60117350' timestamp='2016-07-06T01:22:11Z' uid='548288' user='WayneSchlegel' visible='true' version='15' changeset='40512409' lat='48.5243657' lon='9.3493966' />
    <node id='60117351' timestamp='2016-07-06T01:22:11Z' uid='548288' user='WayneSchlegel' visible='true' version='14' changeset='40512409' lat='48.5249231' lon='9.3488887' />
    </body>"""

    xml_expected = """<body>
    <bounds minlat="48.5297218" minlon="9.3489575" maxlat="48.5378919" maxlon="9.3748784" origin="CGImap 0.8.6 (3984174 spike-06.openstreetmap.org)" />
    <node id="31287590" timestamp="2016-07-06T01:21:43Z" uid="548288" user="WayneSchlegel" visible="true" version="3" changeset="40512409" lat="48.5288901" lon="9.3514616" />
    <node id="60117351" timestamp="2016-07-06T01:22:11Z" uid="548288" user="WayneSchlegel" visible="true" version="14" changeset="40512409" lat="48.5249231" lon="9.3488887" />
    </body>"""
    
    root = ET.fromstring(xml_in)
    element_name = "node"
    id= "60117350"

# When
    remove_element_by_id(root, element_name, id)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print("xml_in:")
    print(xml_in)
    print("xml_expected:")
    print(xml_expected)
    print("xml_out:")
    print(xml_out)
    #assert False
    assert (xml_expected == xml_out)
