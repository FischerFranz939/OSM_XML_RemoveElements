'''
Test script for script1

https://pythontest.com/framework/pytest/pytest-introduction/
python -m pytest -v 1/test_script1.py
python -m pytest --cov=script1 test_script1.py    --> NO PATH !!!!
python -m pytest --cov-report term --cov-report xml:coverage.xml --cov=script1 test_script1.py
python -m pytest --cov-report term --cov-report html:coverage.html --cov=script1 test_script1.py


VSC 
- Code Coverage

Generate .lcov coverage files using your language's code coverage tools
Set the coverage location setting markiscodecoverage.searchCriteria, default: coverage/lcov*.info


- py-coverage-view

'''
import xml.etree.ElementTree as ET
import pathlib
import filecmp


from script1 import remove_element_by_id
from script1 import remove_attribute_from_element
from script1 import remove_attributes_from_element
from script1 import remove_subelement
from script1 import remove_elements_by_subelement
from script1 import remove_subelement_by_wildcard
from script1 import parse_input_file
from script1 import write_outputfile_file
from script1 import number_of_way_references


TEST_PATH = str(pathlib.Path(__file__).parent.resolve()) + "\\..\\test\\"


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def print_xmls(xml_in, xml_out, xml_expected):
    '''Print in, out and expected'''
    print("xml_in:")
    print(xml_in)
    print("xml_out:")
    print(xml_out)
    print("xml_expected:")
    print(xml_expected)


#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------
def test_remove_element_by_id():
    '''Test - remove_element_by_id'''
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
    identifier   = "60117350"

# When
    remove_element_by_id(root, element_name, identifier)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    #assert False
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_attribute_from_element():
    '''Test - remove_attribute_from_element'''
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
    print_xmls(xml_in, xml_out, xml_expected)
    #assert False
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_attributes_from_element():
    '''Test - remove_attributes_from_element'''
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
    print_xmls(xml_in, xml_out, xml_expected)
    #assert False
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_subelement():
    '''Test - remove_subelement'''
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
    print_xmls(xml_in, xml_out, xml_expected)
    #assert False
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_elements_by_subelement():
    '''Test - remove_elements_by_subelement'''
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
    print_xmls(xml_in, xml_out, xml_expected)
    #assert False
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_subelement_by_wildcard():
    '''Test - remove_subelement_by_wildcard'''
    # Given
    #Note: v='Pica d&apos;Estats' vs v="Pica d'Estats"
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
    print_xmls(xml_in, xml_out, xml_expected)
    #assert False
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_parse_input_file():
    '''Test - parse_input_file'''
# Given
    xml_expected = """<osm version="0.6" generator="JOSM">
  <node id="31287590" timestamp="2016-07-06T01:21:43Z" uid="548288" user="WayneSchlegel" visible="true" version="3" changeset="40512409" lat="48.5288901" lon="9.3514616" />
  <bounds minlat="48.5297218" minlon="9.3489575" maxlat="48.5378919" maxlon="9.3748784" origin="CGImap 0.8.6 (3984174 spike-06.openstreetmap.org)" />
  <node id="60117358" timestamp="2020-05-05T13:16:49Z" uid="10056196" user="NVBWSeifert" visible="true" version="10" changeset="84698245" lat="48.5278879" lon="9.3443126">
    <tag k="ele" v="397" />
    <tag k="name" v="Dettingen Erms Mitte" />
    <tag k="network" v="Naldo" />
    <tag k="official_name" v="Dettingen-Mitte" />
    <tag k="operator" v="Erms-Neckar-Bahn AG" />
    <tag k="public_transport" v="station" />
    <tag k="railway" v="halt" />
    <tag k="railway:ref" v="TDTU" />
    <tag k="ref:IFOPT" v="de:08415:28235" />
    <tag k="start_date" v="27.12.1873" />
    <tag k="uic_ref" v="8070679" />
    <tag k="wheelchair" v="yes" />
  </node>
</osm>"""

    xml_file_in = TEST_PATH + "test3.xml"

# When
    tree = parse_input_file(xml_file_in)
    root = tree.getroot()
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls("", xml_out, xml_expected)
    #assert False
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_write_outputfile_file():
    '''Test - write_outputfile_file'''
# Given
    xml_file_in = TEST_PATH + "test3.xml"
    xml_file_out = TEST_PATH + "test3.output"
    xml_file_expected = TEST_PATH + "test3.expected"
    tree = parse_input_file(xml_file_in)

# When
    write_outputfile_file(tree, xml_file_out)

# Then
    result = filecmp.cmp(xml_file_expected, xml_file_out, shallow=False)
    assert result == True

#-------------------------------------------------------------------------------
def test_number_of_way_references():
    '''Test - number_of_way_references'''
    # Given
    xml_in = """<body>
    <way id="371149002" version="1" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="3747488458" />
        <nd ref="3747488457" />
        <nd ref="3747486122" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    <way id="371149333" version="1" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3723434116" />
        <nd ref="3747488458" />
        <nd ref="3747457057" />
        <nd ref="3734586122" />
        <nd ref="3747488821" />
        <tag k="highway" v="path" />
    </way>
    <node id='2739790947' timestamp='2016-06-27T01:55:13Z' uid='548288' user='WayneSchlegel' visible='true' version='2' changeset='40311689' lat='48.5316081' lon='9.359028' />
    </body>"""

    root       = ET.fromstring(xml_in)
    identifier = "3747488458"

  # When
    result = number_of_way_references(root, identifier)

# Then
    assert result == 2
