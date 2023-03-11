'''
Test script for script1 (unit tests)

https://pythontest.com/framework/pytest/pytest-introduction/

python -m pytest -v 1/test_script1.py

!!!! PATH not supported !!!!
python -m pytest --cov=script1 test_script1.py
python -m pytest --cov-report term --cov-report xml:lcov.xml   --cov=script1 test_script1.py
python -m pytest --cov-report term --cov-report html:lcov_html --cov=script1 test_script1.py
python -m pytest --cov-report term --cov-report lcov:lcov.info --cov=script1 test_script1.py
'''
import xml.etree.ElementTree as ET
import filecmp
import script1


TEST_PATH = script1.get_current_dir() + "/../test/"


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
    script1.remove_element_by_id(root, element_name, identifier)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out, xml_expected)
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
    script1.remove_attribute_from_element(root, target_attribute)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out, xml_expected)
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
    script1.remove_attributes_from_element(root, target_attribute_list)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out, xml_expected)
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
    script1.remove_subelement(root, element_name, subelement_name, k_attribute, v_attribute)
    xml_out = ET.tostring(root, encoding='unicode', method='xml')

# Then
    print_xmls(xml_in, xml_out, xml_expected)
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
    script1.remove_elements_by_subelement(root, element_name, subelement_name,
                                          k_attribute, v_attribute)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
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
    script1.remove_subelement_by_wildcard(root, element_name, subelement_name, k_attribute_wildcard)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
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
    tree = script1.parse_input_file(xml_file_in)
    root = tree.getroot()
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls("", xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_write_outputfile_file():
    '''Test - write_outputfile_file'''
# Given
    xml_file_in = TEST_PATH + "test3.xml"
    xml_file_out = xml_file_in + ".output"
    xml_file_expected = xml_file_in + ".expected"
    tree = script1.parse_input_file(xml_file_in)

# When
    script1.write_outputfile_file(tree, xml_file_out)

# Then
    result = filecmp.cmp(xml_file_expected, xml_file_out, shallow=False)
    assert result is True

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
    result = script1.number_of_way_references(root, identifier)

# Then
    assert result == 2

#-------------------------------------------------------------------------------
def test_can_node_be_removed_false():
    '''Test - can_node_be_removed - result: false'''
    # Given
    xml_in = """
    <node id="26864258" version="22" timestamp="2022-04-17T10:54:51Z" lat="42.666952" lon="1.3978986">
        <tag k="name" v="Pica d&apos;Estats"/>
        <tag k="name:en" v="Pique d&apos;Estats"/>
        <tag k="natural" v="peak"/>
        <tag k="source" v="Institut Cartogràfic de Catalunya"/>
        <tag k="source:prominence" v="https://en.wikipedia.org/wiki/List_of_Pyrenean_three-thousanders"/>
        <tag k="url:source" v="ftp://geofons.icc.cat/fitxes/100CIMS/271064006.pdf"/>
        <tag k="wikidata" v="Q1537733"/>
        <tag k="wikipedia" v="ca:Pica d&apos;Estats"/>
    </node>"""
    root = ET.fromstring(xml_in)

# When
    result = script1.can_node_be_removed(root)

# Then
    assert result is False

#-------------------------------------------------------------------------------
def test_can_node_be_removed_true():
    '''Test - can_node_be_removed - result: true'''
    # Given
    xml_in = """
    <node id="26864258" version="22" timestamp="2022-04-17T10:54:51Z" lat="42.666952" lon="1.3978986">
        <tag k="name" v="Pica d&apos;Estats"/>
        <tag k="name:en" v="Pique d&apos;Estats"/>
        <tag k="source" v="Institut Cartogràfic de Catalunya"/>
        <tag k="source:prominence" v="https://en.wikipedia.org/wiki/List_of_Pyrenean_three-thousanders"/>
        <tag k="url:source" v="ftp://geofons.icc.cat/fitxes/100CIMS/271064006.pdf"/>
        <tag k="wikidata" v="Q1537733"/>
        <tag k="wikipedia" v="ca:Pica d&apos;Estats"/>
    </node>"""
    root = ET.fromstring(xml_in)

# When
    result = script1.can_node_be_removed(root)

# Then
    assert result is True

#-------------------------------------------------------------------------------
def test_is_node_id_referenced_way_true():
    '''Test - is_node_id_referenced - way - result: true'''
    # Given
    xml_in = """<body>
    <way id="371149002" version="1" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="3747488457" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    </body>"""
    root    = ET.fromstring(xml_in)
    node_id = "3747486121"

# When
    result = script1.is_node_id_referenced(root, node_id)

# Then
    assert result is True

#-------------------------------------------------------------------------------
def test_is_node_id_referenced_way_false():
    '''Test - is_node_id_referenced - way - result: false'''
    # Given
    xml_in = """<body>
    <way id="371149002" version="1" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="3747488457" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    </body>"""
    root    = ET.fromstring(xml_in)
    node_id = "1111"

# When
    result = script1.is_node_id_referenced(root, node_id)

# Then
    assert result is False

#-------------------------------------------------------------------------------
def test_is_node_id_referenced_relation_true():
    '''Test - is_node_id_referenced - relation - result: true'''
    # Given
    xml_in = """<body>
    <relation id="18" version="3" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start"/>
        <member type="way" ref="521060220" role="both"/>
        <member type="way" ref="240509448" role="both"/>
        <tag k="ref" v="TET:EU:ES:GNR:02:Catalonia"/>
        <tag k="type" v="route"/>
    </relation>
    </body>"""
    root    = ET.fromstring(xml_in)
    node_id = "521060220"

# When
    result = script1.is_node_id_referenced(root, node_id)

# Then
    assert result is True

#-------------------------------------------------------------------------------
def test_is_node_id_referenced_relation_false():
    '''Test - is_node_id_referenced - relation - result: false'''
    # Given
    xml_in = """<body>
    <relation id="18" version="3" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start"/>
        <member type="way" ref="521060220" role="both"/>
        <member type="way" ref="240509448" role="both"/>
        <tag k="ref" v="TET:EU:ES:GNR:02:Catalonia"/>
        <tag k="type" v="route"/>
    </relation>
    </body>"""
    root    = ET.fromstring(xml_in)
    node_id = "1111"

# When
    result = script1.is_node_id_referenced(root, node_id)

# Then
    assert result is False

#-------------------------------------------------------------------------------
def test_number_of_relation_references_1():
    '''Test - number_of_relation_references - found 1'''
    # Given
    xml_in = """<body>
    <relation id="18" version="3" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start"/>
        <member type="way" ref="521060220" role="both"/>
        <member type="way" ref="240509448" role="both"/>
        <tag k="ref" v="TET:EU:ES:GNR:02:Catalonia"/>
        <tag k="type" v="route"/>
    </relation>
    </body>"""
    root    = ET.fromstring(xml_in)
    node_id = "521060220"

# When
    result = script1.number_of_relation_references(root, node_id)

# Then
    assert result == 1

#-------------------------------------------------------------------------------
def test_number_of_relation_references_0():
    '''Test - number_of_relation_references - found 0'''
    # Given
    xml_in = """<body>
    <relation id="18" version="3" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start"/>
        <member type="way" ref="521060220" role="both"/>
        <member type="way" ref="240509448" role="both"/>
        <tag k="ref" v="TET:EU:ES:GNR:02:Catalonia"/>
        <tag k="type" v="route"/>
    </relation>
    </body>"""
    root    = ET.fromstring(xml_in)
    node_id = "1111"

# When
    result = script1.number_of_relation_references(root, node_id)

# Then
    assert result == 0

#-------------------------------------------------------------------------------
def test_number_of_way_references_1():
    '''Test - number_of_way_references - found 1'''
    # Given
    xml_in = """<body>
    <way id="371149002" version="1" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="3747488457" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    </body>"""
    root    = ET.fromstring(xml_in)
    node_id = "3747488457"

# When
    result = script1.number_of_way_references(root, node_id)

# Then
    assert result == 1

#-------------------------------------------------------------------------------
def test_number_of_way_references_0():
    '''Test - number_of_way_references - found 0'''
    # Given
    xml_in = """<body>
    <way id="371149002" version="1" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="3747488457" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    </body>"""
    root    = ET.fromstring(xml_in)
    node_id = "1111"

# When
    result = script1.number_of_way_references(root, node_id)

# Then
    assert result == 0

#-------------------------------------------------------------------------------
def test_remove_buildings_and_nodes():
    '''Test - remove_buildings and not referenced nodes'''
    # Given
    xml_in = """<body>
    <node id="26864258" version="22" timestamp="2022-04-17T10:54:51Z" lat="42.666952" lon="1.3978986">
        <tag k="name" v="Pica d&apos;Estats"/>
    </node>
    <way id='268645709' timestamp='2015-09-22T18:58:53Z' uid='548288' user='WayneSchlegel' visible='true' version='3' changeset='34190335'>
        <nd ref='2739790961' />
        <nd ref='2739790947' />
        <nd ref='2739790961' />
        <tag k='addr:city' v='Dettingen an der Erms' />
        <tag k='addr:street' v='Sperberweg' />
        <tag k='building' v='yes' />
    </way>
    <node id='2739790947' timestamp='2016-06-27T01:55:13Z' uid='548288' user='WayneSchlegel' visible='true' version='2' changeset='40311689' lat='48.5316081' lon='9.359028' />
    <node id='2739790961' timestamp='2016-06-27T01:55:14Z' uid='548288' user='WayneSchlegel' visible='true' version='2' changeset='40311689' lat='48.531868' lon='9.357414' />
    </body>"""

    xml_expected = """<body>
    <node id="26864258" version="22" timestamp="2022-04-17T10:54:51Z" lat="42.666952" lon="1.3978986">
        <tag k="name" v="Pica d'Estats" />
    </node>
    </body>"""
    root         = ET.fromstring(xml_in)
    remove_nodes = True

# When
    script1.remove_buildings(root, remove_nodes)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_buildings_only():
    '''Test - remove_buildings only (do not remove nodes)'''
    # Given
    xml_in = """<body>
    <node id="26864258" version="22" timestamp="2022-04-17T10:54:51Z" lat="42.666952" lon="1.3978986">
        <tag k="name" v="Pica d&apos;Estats"/>
    </node>
    <way id='268645709' timestamp='2015-09-22T18:58:53Z' uid='548288' user='WayneSchlegel' visible='true' version='3' changeset='34190335'>
        <nd ref='2739790961' />
        <nd ref='2739790947' />
        <nd ref='2739790961' />
        <tag k='addr:city' v='Dettingen an der Erms' />
        <tag k='addr:street' v='Sperberweg' />
        <tag k='building' v='yes' />
    </way>
    <node id='2739790947' timestamp='2016-06-27T01:55:13Z' uid='548288' user='WayneSchlegel' visible='true' version='2' changeset='40311689' lat='48.5316081' lon='9.359028' />
    <node id='2739790961' timestamp='2016-06-27T01:55:14Z' uid='548288' user='WayneSchlegel' visible='true' version='2' changeset='40311689' lat='48.531868' lon='9.357414' />
    </body>"""

    xml_expected = """<body>
    <node id="26864258" version="22" timestamp="2022-04-17T10:54:51Z" lat="42.666952" lon="1.3978986">
        <tag k="name" v="Pica d'Estats" />
    </node>
    <node id="2739790947" timestamp="2016-06-27T01:55:13Z" uid="548288" user="WayneSchlegel" visible="true" version="2" changeset="40311689" lat="48.5316081" lon="9.359028" />
    <node id="2739790961" timestamp="2016-06-27T01:55:14Z" uid="548288" user="WayneSchlegel" visible="true" version="2" changeset="40311689" lat="48.531868" lon="9.357414" />
    </body>"""
    root         = ET.fromstring(xml_in)
    remove_nodes = False

# When
    script1.remove_buildings(root, remove_nodes)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_write_linux_line_endings():
    '''Test - write_linux_line_endings'''
# Given
    xml_file_in = TEST_PATH + "test2_formated.xml"
    xml_file_out = xml_file_in + ".output"
    xml_file_expected = xml_file_in + ".expected"

# When
    script1.write_linux_line_endings(xml_file_in, xml_file_out)

# Then
    result = filecmp.cmp(xml_file_expected, xml_file_out, shallow=False)
    assert result is True

#-------------------------------------------------------------------------------
def test_adapt_elements_with_negative_id():
    '''Test - adapt_elements_with_negative_id'''
    # Given
    xml_in = """<body>
    <node id="-117276" action="modify" lat="67.04228469059" lon="16.53687049956" />
    <way id='-268645799' action="modify" timestamp='2015-09-22T18:58:53Z' uid='548288' user='WayneSchlegel' visible='true' changeset='34190335'>
        <nd ref='2739790961' />
        <tag k='building' v='yes' />
    </way>
    <relation id="-18" action="modify" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start"/>
        <tag k="type" v="route"/>
    </relation>
    </body>"""
    xml_expected = """<body>
    <node id="117276" lat="67.04228469059" lon="16.53687049956" version="1" />
    <way id="268645799" timestamp="2015-09-22T18:58:53Z" uid="548288" user="WayneSchlegel" visible="true" changeset="34190335" version="1">
        <nd ref="2739790961" />
        <tag k="building" v="yes" />
    </way>
    <relation id="18" timestamp="2020-09-07T09:55:45Z" version="1">
        <member type="node" ref="53376950" role="start" />
        <tag k="type" v="route" />
    </relation>
    </body>"""
    root = ET.fromstring(xml_in)

# When
    script1.adapt_elements_with_negative_id(root)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_node_elements_with_no_reference():
    '''Test - remove_node_elements_with_no_reference'''
    # Given
    xml_in = """<body>
    <way id="371149002" version="1" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="3747488457" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    <relation id="18" version="3" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start"/>
        <member type="way" ref="521060220" role="both"/>
        <member type="way" ref="240509448" role="both"/>
        <tag k="ref" v="TET:EU:ES:GNR:02:Catalonia"/>
        <tag k="type" v="route"/>
    </relation>
    <node id="3747488457" timestamp="2016-07-06T01:21:43Z" visible="true" version="3" changeset="40512409" lat="48.5288901" lon="9.3514616" />
    <node id="521060220" timestamp="2016-07-06T01:22:11Z" visible="true" version="15" changeset="40512409" lat="48.5243657" lon="9.3493966" />
    <node id="60117351" timestamp="2016-07-06T01:22:11Z" visible="true" version="14" changeset="40512409" lat="48.5249231" lon="9.3488887" />
    <node id="31287590" timestamp="2016-07-06T01:21:43Z" visible="true" version="3" changeset="40512409" lat="48.5288901" lon="9.3514616" />
    </body>"""
    xml_expected = """<body>
    <way id="371149002" version="1" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="3747488457" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    <relation id="18" version="3" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start" />
        <member type="way" ref="521060220" role="both" />
        <member type="way" ref="240509448" role="both" />
        <tag k="ref" v="TET:EU:ES:GNR:02:Catalonia" />
        <tag k="type" v="route" />
    </relation>
    <node id="3747488457" timestamp="2016-07-06T01:21:43Z" visible="true" version="3" changeset="40512409" lat="48.5288901" lon="9.3514616" />
    <node id="521060220" timestamp="2016-07-06T01:22:11Z" visible="true" version="15" changeset="40512409" lat="48.5243657" lon="9.3493966" />
    </body>"""
    root = ET.fromstring(xml_in)

# When
    script1.remove_node_elements_with_no_reference(root)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_adapt_subelements_with_negative_references():
    '''Test - adapt_subelements_with_negative_references'''
    # Given
    xml_in = """<body>
    <way id="371149002" action="modify" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="-3747488457" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    <relation id="18" version="3" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start"/>
        <member type="way" ref="-521060220" role="both"/>
        <member type="way" ref="240509448" role="both"/>
        <tag k="ref" v="TET:EU:ES:GNR:02:Catalonia"/>
        <tag k="type" v="route"/>
    </relation>
    </body>"""
    xml_expected = """<body>
    <way id="371149002" timestamp="2015-09-17T10:44:37Z">
        <nd ref="3721534116" />
        <nd ref="3747488457" />
        <nd ref="3747486121" />
        <tag k="highway" v="path" />
    </way>
    <relation id="18" version="3" timestamp="2020-09-07T09:55:45Z">
        <member type="node" ref="53376950" role="start" />
        <member type="way" ref="521060220" role="both" />
        <member type="way" ref="240509448" role="both" />
        <tag k="ref" v="TET:EU:ES:GNR:02:Catalonia" />
        <tag k="type" v="route" />
    </relation>
    </body>"""
    root = ET.fromstring(xml_in)

# When
    script1.adapt_subelements_with_negative_references(root)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out
