'''
Test script for script_03 (unit tests)

https://pythontest.com/framework/pytest/pytest-introduction/

python -m pytest -v test_script_03.py

!!!! PATH not supported !!!!
python -m pytest --cov=script_03 test_script_03.py
python -m pytest --cov-report term --cov-report xml:lcov.xml   --cov=script_03 test_script_03.py
python -m pytest --cov-report term --cov-report html:lcov_html --cov=script_03 test_script_03.py
python -m pytest --cov-report term --cov-report lcov:lcov.info --cov=script_03 test_script_03.py
'''
import xml.etree.ElementTree as ET
from pathlib import Path
from io import StringIO
import script_03


TEST_PATH = str(Path(__file__).parent.resolve()) + "/"


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
def test_remove_node_whitelist():
    '''Test - remove_node_whitelist'''
# Given
    xml_in = """<body>
    <node id="10971457805" version="1" lat="59.3314797" lon="18.058734">
        <tag k="amenity" v="bench" />
    </node>
    <node id="16864088" version="1" lat="59.3156252" lon="17.9881616">
        <tag k="amenity" v="ferry_terminal" />
        <tag k="ferry" v="yes" />
        <tag k="name" v="Ekensberg" />
        <tag k="network" v="SL" />
        <tag k="network:wikidata" v="Q970452" />
        <tag k="public_transport" v="station" />
        <tag k="ref" v="8018" />
        <tag k="route_ref" v="89" />
    </node>
    </body>"""

    xml_expected = """<node id="16864088" version="1" lat="59.3156252" lon="17.9881616">
        <tag k="amenity" v="ferry_terminal" />
        <tag k="ferry" v="yes" />
        <tag k="name" v="Ekensberg" />
        <tag k="network" v="SL" />
        <tag k="network:wikidata" v="Q970452" />
        <tag k="public_transport" v="station" />
        <tag k="ref" v="8018" />
        <tag k="route_ref" v="89" />
    </node>
    """

    amenity_white_list = ['biergarten','cafe','restaurant','bus_station','ferry_terminal',
                      'parking,clinic','hospital','ranger_station','drinking_water','shelter',
                      'shower,toilets','water_point','dive_centre','grave_yard','monastery',
                      'place_of_worship','public_bath']
    tags = dict([
        ("amenity", amenity_white_list)
        ])
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_03.get_next_first_level_element(input_file):
        if element.tag != "body":
            remove = script_03.remove_node_whitelist(element, tags)
            if remove == False:
                xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_node_by_tag_key():
    '''Test - remove_node_by_tag_key'''
# Given
    xml_in = """<body>
    <node id="2949394270" version="1" lat="59.3193809" lon="18.0655601">
        <tag k="craft" v="jeweller" />
        <tag k="email" v="smideochform@gmail.com" />
        <tag k="name" v="Smide och Form" />
        <tag k="opening_hours" v="Mo-Fr 10:00-18:00;Sa 11:00-15:00" />
        <tag k="phone" v="+46-8-6414781" />
        <tag k="shop" v="jewelry" />
        <tag k="website" v="https://www.smideochform.se/" />
    </node>
    <node id="10940046167" version="1" lat="59.3261145" lon="18.0614215">
        <tag k="highway" v="street_lamp" />
    </node>
    </body>"""

    xml_expected = """<node id="10940046167" version="1" lat="59.3261145" lon="18.0614215">
        <tag k="highway" v="street_lamp" />
    </node>
    """

    tag_key_list = ["craft"]
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_03.get_next_first_level_element(input_file):
        if element.tag != "body":
            remove = script_03.remove_node_by_tag_key(element, tag_key_list)
            if remove == False:
                xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_node_by_tag_kv_01():
    '''Test - remove_node_by_tag_kv_01'''
# Given
    xml_in = """<body>
    <node id="2949394270" version="1" lat="59.3193809" lon="18.0655601">
        <tag k="craft" v="jeweller" />
        <tag k="email" v="smideochform@gmail.com" />
        <tag k="name" v="Smide och Form" />
        <tag k="opening_hours" v="Mo-Fr 10:00-18:00;Sa 11:00-15:00" />
        <tag k="phone" v="+46-8-6414781" />
        <tag k="shop" v="jewelry" />
        <tag k="website" v="https://www.smideochform.se/" />
    </node>
    <node id="10940046167" version="1" lat="59.3261145" lon="18.0614215">
        <tag k="highway" v="street_lamp" />
    </node>
    </body>"""

    xml_expected = """"""

    key_value_pair1 = ['highway','street_lamp']
    key_value_pair2 = ['shop','jewelry']
    kv_list = [key_value_pair1, key_value_pair2]
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_03.get_next_first_level_element(input_file):
        if element.tag != "body":
            remove = script_03.remove_node_by_tag_kv(element, kv_list)
            if remove == False:
                xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_node_by_tag_kv_02():
    '''Test - remove_node_by_tag_kv_02'''
# Given
    xml_in = """<body>
    <node id="2949394270" version="1" lat="59.3193809" lon="18.0655601">
        <tag k="craft" v="jeweller" />
        <tag k="email" v="smideochform@gmail.com" />
        <tag k="name" v="Smide och Form" />
        <tag k="opening_hours" v="Mo-Fr 10:00-18:00;Sa 11:00-15:00" />
        <tag k="phone" v="+46-8-6414781" />
        <tag k="shop" v="jewelry" />
        <tag k="website" v="https://www.smideochform.se/" />
    </node>
    <node id="10940046167" version="1" lat="59.3261145" lon="18.0614215">
        <tag k="highway" v="street_lamp" />
    </node>
    </body>"""

    xml_expected = """<node id="10940046167" version="1" lat="59.3261145" lon="18.0614215">
        <tag k="highway" v="street_lamp" />
    </node>
    """

    key_value_pair1 = ['power','tower']
    key_value_pair2 = ['shop','jewelry']
    kv_list = [key_value_pair1, key_value_pair2]
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_03.get_next_first_level_element(input_file):
        if element.tag != "body":
            remove = script_03.remove_node_by_tag_kv(element, kv_list)
            if remove == False:
                xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_tags():
    '''Test - remove_tags'''
# Given
    xml_in = """<body>
    <node id='119663' version='1' lat='59.3281848' lon='18.0629158'>
        <tag k='button_operated' v='yes' />
        <tag k='crossing' v='traffic_signals' />
        <tag k='highway' v='crossing' />
        <tag k='source' v='survey' />
        <tag k='traffic_signals:sound' v='yes' />
    </node>
    </body>"""

    xml_expected = """<node id="119663" version="1" lat="59.3281848" lon="18.0629158">
        <tag k="button_operated" v="yes" />
        <tag k="crossing" v="traffic_signals" />
        <tag k="highway" v="crossing" />
        <tag k="traffic_signals:sound" v="yes" />
    </node>
    """
    tag_keys = ['source','survey:date','created_by','wikidata','wikipedia']
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_03.get_next_first_level_element(input_file):
        if element.tag != "body":
            script_03.remove_tags(element, tag_keys)
            xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_remove_tags_whitelist():
    '''Test - remove_tags_whitelist'''
# Given
    xml_in = """<body>
    <node id='25929985' version='91' changeset='1' lat='59.3251172' lon='18.0710935'>
        <tag k='admin_level' v='2' />
        <tag k='alt_name:fit' v='Tokholmi' />
        <tag k='alt_name:gl' v='Stockholm' />
        <tag k='alt_name:he' v='שטוקהולם' />
        <tag k='capital' v='yes' />
        <tag k='name' v='Stockholm' />
        <tag k='name:am' v='ስቶኮልም' />
        <tag k='name:an' v='Estocolmo' />
        <tag k='name:de' v='Stockholm' />
        <tag k='name:diq' v='Stokholm' />
        <tag k='name:el' v='Στοκχόλμη' />
        <tag k='name:en' v='Stockholm' />
        <tag k='name:se' v='Stockholbma' />
        <tag k='name:sju' v='Tjåsskasulla' />
        <tag k='place' v='city' />
        <tag k='population' v='984748' />
        <tag k='population:date' v='2022' />
        <tag k='ref:se:pts:postort' v='STOCKHOLM' />
        <tag k='ref:se:scb' v='0336' />
        <tag k='short_name' v='Sthlm' />
        <tag k='source:name:br' v='ofis publik ar brezhoneg' />
        <tag k='source:population' v='https://citypopulation.de/en/sweden/admin/01__stockholm/' />
        <tag k='wikidata' v='Q1754' />
        <tag k='wikipedia' v='sv:Stockholm' />
    </node>
    <node id="1198849315" version="1" lat="59.3200076" lon="18.0669833">
        <tag k="addr:city" v="Stockholm" />
        <tag k="addr:country" v="SE" />
        <tag k="addr:housenumber" v="15" />
        <tag k="addr:street" v="Brännkyrkagatan" />
        <tag k="entrance" v="yes" />
    </node>
    </body>"""

    xml_expected = """<node id="25929985" version="91" changeset="1" lat="59.3251172" lon="18.0710935">
        <tag k="admin_level" v="2" />
        <tag k="alt_name:fit" v="Tokholmi" />
        <tag k="alt_name:gl" v="Stockholm" />
        <tag k="alt_name:he" v="שטוקהולם" />
        <tag k="capital" v="yes" />
        <tag k="name" v="Stockholm" />
        <tag k="name:de" v="Stockholm" />
        <tag k="name:en" v="Stockholm" />
        <tag k="name:se" v="Stockholbma" />
        <tag k="place" v="city" />
        <tag k="population" v="984748" />
        <tag k="population:date" v="2022" />
        <tag k="ref:se:pts:postort" v="STOCKHOLM" />
        <tag k="ref:se:scb" v="0336" />
        <tag k="short_name" v="Sthlm" />
        <tag k="source:name:br" v="ofis publik ar brezhoneg" />
        <tag k="source:population" v="https://citypopulation.de/en/sweden/admin/01__stockholm/" />
        <tag k="wikidata" v="Q1754" />
        <tag k="wikipedia" v="sv:Stockholm" />
    </node>
    <node id="1198849315" version="1" lat="59.3200076" lon="18.0669833">
        <tag k="addr:housenumber" v="15" />
        <tag k="entrance" v="yes" />
    </node>
    """
    name_white_list = ['name','name:de','name:en','name:se']
    addr_whit_list = ['addr:housenumber']
    tags = dict([
        ("name", name_white_list),
        ("addr", addr_whit_list)
        ])
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_03.get_next_first_level_element(input_file):
        if element.tag != "body":
            script_03.remove_tags_whitelist(element, tags)
            xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out
