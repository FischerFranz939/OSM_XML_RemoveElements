# https://pythontest.com/framework/pytest/pytest-introduction/
# python.exe -m pytest -v d:/MeineProgramme/OSM_XML_RemoveElements/1/test_script1.py
import xml.etree.ElementTree as ET
from script1 import *


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def print_xmls(input, output, expected):
    print("xml_in:")
    print(input)
    print("xml_out:")
    print(output)
    print("xml_expected:")
    print(expected)


#-------------------------------------------------------------------------------
# Tests
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

    root         = ET.fromstring(xml_in)
    element_name = "node"
    id           = "60117350"

# When
    remove_element_by_id(root, element_name, id)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out,xml_expected)
    #assert False
    assert (xml_expected == xml_out)

#-------------------------------------------------------------------------------
def test_remove_attribute_from_element():
# Given
    xml_in = """<body>
    <bounds minlat='48.5297218' minlon='9.3489575' maxlat='48.5378919' maxlon='9.3748784' origin='CGImap 0.8.6 (3984174 spike-06.openstreetmap.org)' />
    <node id='31287590' timestamp='2016-07-06T01:21:43Z' uid='548288' user='WayneSchlegel' visible='true' version='3' changeset='40512409' lat='48.5288901' lon='9.3514616' />
    <node id='60117350' timestamp='2016-07-06T01:22:11Z' uid='548288' user='WayneSchlegel' visible='true' version='15' changeset='40512409' lat='48.5243657' lon='9.3493966' />
    <node id='60117351' timestamp='2016-07-06T01:22:11Z' uid='548288' user='WayneSchlegel' visible='true' version='14' changeset='40512409' lat='48.5249231' lon='9.3488887' />
    </body>"""

    xml_expected = """<body>
    <bounds minlat="48.5297218" minlon="9.3489575" maxlat="48.5378919" maxlon="9.3748784" origin="CGImap 0.8.6 (3984174 spike-06.openstreetmap.org)" />
    <node id="31287590" uid="548288" user="WayneSchlegel" visible="true" version="3" changeset="40512409" lat="48.5288901" lon="9.3514616" />
    <node id="60117350" uid="548288" user="WayneSchlegel" visible="true" version="15" changeset="40512409" lat="48.5243657" lon="9.3493966" />
    <node id="60117351" uid="548288" user="WayneSchlegel" visible="true" version="14" changeset="40512409" lat="48.5249231" lon="9.3488887" />
    </body>"""

    root             = ET.fromstring(xml_in)
    target_attribute = "timestamp"

# When
    remove_attribute_from_element(root, target_attribute)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out,xml_expected)
    #assert False
    assert (xml_expected == xml_out)

#-------------------------------------------------------------------------------
def test_remove_attributes_from_element():
# Given
    xml_in = """<body>
    <bounds minlat='48.5297218' minlon='9.3489575' maxlat='48.5378919' maxlon='9.3748784' origin='CGImap 0.8.6 (3984174 spike-06.openstreetmap.org)' />
    <node id='31287590' timestamp='2016-07-06T01:21:43Z' uid='548288' user='WayneSchlegel' visible='true' version='3' changeset='40512409' lat='48.5288901' lon='9.3514616' />
    <node id='60117350' timestamp='2016-07-06T01:22:11Z' uid='548288' user='WayneSchlegel' visible='true' version='15' changeset='40512409' lat='48.5243657' lon='9.3493966' />
    <node id='60117351' timestamp='2016-07-06T01:22:11Z' uid='548288' user='WayneSchlegel' visible='true' version='14' changeset='40512409' lat='48.5249231' lon='9.3488887' />
    </body>"""

    xml_expected = """<body>
    <bounds minlat="48.5297218" minlon="9.3489575" maxlat="48.5378919" maxlon="9.3748784" origin="CGImap 0.8.6 (3984174 spike-06.openstreetmap.org)" />
    <node id="31287590" timestamp="2016-07-06T01:21:43Z" visible="true" version="3" changeset="40512409" lat="48.5288901" lon="9.3514616" />
    <node id="60117350" timestamp="2016-07-06T01:22:11Z" visible="true" version="15" changeset="40512409" lat="48.5243657" lon="9.3493966" />
    <node id="60117351" timestamp="2016-07-06T01:22:11Z" visible="true" version="14" changeset="40512409" lat="48.5249231" lon="9.3488887" />
    </body>"""

    root                  = ET.fromstring(xml_in)
    target_attribute_list = ["user", "uid"]

# When
    remove_attributes_from_element(root, target_attribute_list)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out,xml_expected)
    #assert False
    assert (xml_expected == xml_out)

#-------------------------------------------------------------------------------
def test_remove_subelement():
    # Given
    xml_in = """<body>
    <node id='251665776' timestamp='2016-06-27T01:55:11Z' uid='548288' user='WayneSchlegel' visible='true' version='5' changeset='40311689' lat='48.5314869' lon='9.3497587' />
    <node id='343556624' timestamp='2012-10-05T18:32:53Z' uid='548288' user='WayneSchlegel' visible='true' version='3' changeset='13376550' lat='48.5518545' lon='9.2802616'>
        <tag k='power' v='tower' />
        <tag k='ref' v='517/90' />
        <tag k='source' v='survey;image' />
    </node>
    </body>"""

    xml_expected = """<body>
    <node id="251665776" timestamp="2016-06-27T01:55:11Z" uid="548288" user="WayneSchlegel" visible="true" version="5" changeset="40311689" lat="48.5314869" lon="9.3497587" />
    <node id="343556624" timestamp="2012-10-05T18:32:53Z" uid="548288" user="WayneSchlegel" visible="true" version="3" changeset="13376550" lat="48.5518545" lon="9.2802616">
        <tag k="ref" v="517/90" />
        <tag k="source" v="survey;image" />
    </node>
    </body>"""

    root            = ET.fromstring(xml_in)
    element_name    = "node"
    subelement_name = "tag"
    k_attribute     = "power"
    v_attribute     = "tower"

# When
    remove_subelement(root, element_name, subelement_name, k_attribute, v_attribute)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out,xml_expected)
    #assert False
    assert (xml_expected == xml_out)

#-------------------------------------------------------------------------------
def test_remove_elements_by_subelement():
    # Given
    xml_in = """<body>
    <node id='251665776' timestamp='2016-06-27T01:55:11Z' uid='548288' user='WayneSchlegel' visible='true' version='5' changeset='40311689' lat='48.5314869' lon='9.3497587' />
    <node id='343556624' timestamp='2012-10-05T18:32:53Z' uid='548288' user='WayneSchlegel' visible='true' version='3' changeset='13376550' lat='48.5518545' lon='9.2802616'>
        <tag k='power' v='tower' />
        <tag k='ref' v='517/90' />
        <tag k='source' v='survey;image' />
    </node>
    <node id='251665772' timestamp='2016-06-27T01:55:11Z' uid='548288' user='WayneSchlegel' visible='true' version='5' changeset='40311689' lat='48.5328829' lon='9.3450466' />
    </body>"""

    xml_expected = """<body>
    <node id="251665776" timestamp="2016-06-27T01:55:11Z" uid="548288" user="WayneSchlegel" visible="true" version="5" changeset="40311689" lat="48.5314869" lon="9.3497587" />
    <node id="251665772" timestamp="2016-06-27T01:55:11Z" uid="548288" user="WayneSchlegel" visible="true" version="5" changeset="40311689" lat="48.5328829" lon="9.3450466" />
    </body>"""

    root            = ET.fromstring(xml_in)
    element_name    = "node"
    subelement_name = "tag"
    k_attribute     = "power"
    v_attribute     = "tower"

# When
    remove_elements_by_subelement(root, element_name, subelement_name, k_attribute, v_attribute)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out,xml_expected)
    #assert False
    assert (xml_expected == xml_out)

#-------------------------------------------------------------------------------
def test_remove_subelement_wildcard():
    # Given
    #TODO: v='Pica d&apos;Estats' vs v="Pica d'Estats"
    xml_in = """<body>
    <node id="26864258" version="22" timestamp="2022-04-17T10:54:51Z" lat="42.666952" lon="1.3978986">
        <tag k="name" v="Pica d&apos;Estats"/>
        <tag k="name:en" v="Pique d&apos;Estats"/>
        <tag k="natural" v="peak"/>
        <tag k="source" v="Institut Cartogràfic de Catalunya"/>
        <tag k="source:prominence" v="https://en.wikipedia.org/wiki/List_of_Pyrenean_three-thousanders"/>
        <tag k="url:source" v="ftp://geofons.icc.cat/fitxes/100CIMS/271064006.pdf"/>
        <tag k="wikidata" v="Q1537733"/>
        <tag k="wikipedia" v="ca:Pica d&apos;Estats"/>
    </node>
    <way id='268645709' timestamp='2015-09-22T18:58:53Z' uid='548288' user='WayneSchlegel' visible='true' version='3' changeset='34190335'>
        <nd ref='2739790961' />
        <nd ref='2739790961' />
        <tag k='addr:city' v='Dettingen an der Erms' />
        <tag k='addr:street' v='Sperberweg' />
        <tag k='building' v='yes' />
    </way>
    <node id='2739790947' timestamp='2016-06-27T01:55:13Z' uid='548288' user='WayneSchlegel' visible='true' version='2' changeset='40311689' lat='48.5316081' lon='9.359028' />
    </body>"""

    xml_expected = """<body>
    <node id="26864258" version="22" timestamp="2022-04-17T10:54:51Z" lat="42.666952" lon="1.3978986">
        <tag k="name" v="Pica d'Estats" />
        <tag k="name:en" v="Pique d'Estats" />
        <tag k="natural" v="peak" />
        <tag k="source" v="Institut Cartogràfic de Catalunya" />
        <tag k="source:prominence" v="https://en.wikipedia.org/wiki/List_of_Pyrenean_three-thousanders" />
        <tag k="url:source" v="ftp://geofons.icc.cat/fitxes/100CIMS/271064006.pdf" />
        </node>
    <way id="268645709" timestamp="2015-09-22T18:58:53Z" uid="548288" user="WayneSchlegel" visible="true" version="3" changeset="34190335">
        <nd ref="2739790961" />
        <nd ref="2739790961" />
        <tag k="addr:city" v="Dettingen an der Erms" />
        <tag k="addr:street" v="Sperberweg" />
        <tag k="building" v="yes" />
    </way>
    <node id="2739790947" timestamp="2016-06-27T01:55:13Z" uid="548288" user="WayneSchlegel" visible="true" version="2" changeset="40311689" lat="48.5316081" lon="9.359028" />
    </body>"""

    root                 = ET.fromstring(xml_in)
    element_name         = "node"
    subelement_name      = "tag"
    k_attribute_wildcard = "wiki"

# When
    remove_subelement_by_wildcard(root, element_name, subelement_name, k_attribute_wildcard)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out,xml_expected)
    #assert False
    assert (xml_expected == xml_out)
