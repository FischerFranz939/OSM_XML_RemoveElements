'''
Test script for script_06 (unit tests)

https://pythontest.com/framework/pytest/pytest-introduction/

python -m pytest -v test_script_06.py

!!!! PATH not supported !!!!
python -m pytest --cov=script_06 test_script_06.py
python -m pytest --cov-report term --cov-report xml:lcov.xml   --cov=script_06 test_script_06.py
python -m pytest --cov-report term --cov-report html:lcov_html --cov=script_06 test_script_06.py
python -m pytest --cov-report term --cov-report lcov:lcov.info --cov=script_06 test_script_06.py
'''
import xml.etree.ElementTree as ET
from pathlib import Path
from io import StringIO
import script_06


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
def test_remove_action_delete_elements():
    '''Test - remove_action_delete_elements'''
# Given
    xml_in = """<body>
    <node id='119039' visible='true' version='1' lat='59.3206968' lon='18.0454426' />
    <way id='-148364' action='modify' visible='true'>
        <nd ref='2893802104' />
        <nd ref='-191378' />
        <nd ref='-191379' />
        <tag k='highway' v='path' />
    </way>
    <way id='4491173' action='delete' visible='true' version='1'>
        <tag k='highway' v='residential' />
        <tag k='name' v='Kungsgatan' />
    </way>
    <node id='257' timestamp='2008-12-30T04:35:26Z' uid='865' user='ken' visible='true' version='3' changeset='67' lat='59.20698' lon='18.2153434' />
    <node id='1907486936' action='delete' visible='true' version='1' lat='59.1921608' lon='18.2125616' />
    </body>"""

    xml_expected = """<node id="119039" visible="true" version="1" lat="59.3206968" lon="18.0454426" />
    <way id="-148364" action="modify" visible="true">
        <nd ref="2893802104" />
        <nd ref="-191378" />
        <nd ref="-191379" />
        <tag k="highway" v="path" />
    </way>
    <node id="257" timestamp="2008-12-30T04:35:26Z" uid="865" user="ken" visible="true" version="3" changeset="67" lat="59.20698" lon="18.2153434" />
    """
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_06.get_next_first_level_element(input_file):
        if element.tag != "body":
            remove = script_06.remove_action_delete_elements(element)
            if remove == False:
                xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out

#-------------------------------------------------------------------------------
def test_handle_action_modify_elements():
    '''Test - handle_action_modify_elements'''
# Given
    xml_in = """<body>
    <node id='-191378' action='modify' visible='true' lat='59.1935366274' lon='18.22534052721' />
    <node id='-191379' action='modify' visible='true' lat='59.19367836951' lon='18.22585254261' />
    <node id='119039' visible='true' version='1' lat='59.3206968' lon='18.0454426' />
    <way id='-148364' action='modify' visible='true'>
        <nd ref='2893802104' />
        <nd ref='-191378' />
        <nd ref='-191379' />
        <tag k='highway' v='path' />
    </way>
    <way id='4490189' action='modify' visible='true' version='1'>
        <nd ref='27527823' />
        <nd ref='300260246' />
        <nd ref='1617791942' />
        <nd ref='2023742470' />
        <nd ref='27527823' />
        <tag k='name' v='Kungsträdgården' />
    </way>
    <node id='257' timestamp='2008-12-30T04:35:26Z' uid='865' user='ken' visible='true' version='3' changeset='67' lat='59.20698' lon='18.2153434' />
    </body>"""

    xml_expected = """<node id="191378" lat="59.1935366274" lon="18.22534052721" version="1" />
    <node id="191379" lat="59.19367836951" lon="18.22585254261" version="1" />
    <node id="119039" visible="true" version="1" lat="59.3206968" lon="18.0454426" />
    <way id="148364" version="1">
        <nd ref="2893802104" />
        <nd ref="191378" />
        <nd ref="191379" />
        <tag k="highway" v="path" />
    </way>
    <way id="4490189" version="1">
        <nd ref="27527823" />
        <nd ref="300260246" />
        <nd ref="1617791942" />
        <nd ref="2023742470" />
        <nd ref="27527823" />
        <tag k="name" v="Kungsträdgården" />
    </way>
    <node id="257" timestamp="2008-12-30T04:35:26Z" uid="865" user="ken" visible="true" version="3" changeset="67" lat="59.20698" lon="18.2153434" />
    """
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_06.get_next_first_level_element(input_file):
        if element.tag != "body":
            script_06.handle_action_modify_elements(element)
            xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out
