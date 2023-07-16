'''
Test script for script_02 (unit tests)

https://pythontest.com/framework/pytest/pytest-introduction/

python -m pytest -v test_script_02.py

!!!! PATH not supported !!!!
python -m pytest --cov=script_02 test_script_02.py
python -m pytest --cov-report term --cov-report xml:lcov.xml   --cov=script_02 test_script_02.py
python -m pytest --cov-report term --cov-report html:lcov_html --cov=script_02 test_script_02.py
python -m pytest --cov-report term --cov-report lcov:lcov.info --cov=script_02 test_script_02.py
'''
import xml.etree.ElementTree as ET
from pathlib import Path
from io import StringIO
import script_02


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
def test_is_relation_with_tag():
    '''Test - is_relation_with_tag'''
# Given
    xml_in = """<body>
    <node id='119044' timestamp='2019-11-10T18:18:34Z' uid='83501' user='riiga' visible='true' version='5' changeset='76875955' lat='59.3211049' lon='18.0549223' />
    <relation id='3464444' version='1'>
        <member type='way' ref='465901030' role='' />
        <member type='way' ref='803487169' role='' />
        <member type='node' ref='2071677724' role='stop' />
        <member type='node' ref='7515926986' role='stop' />
        <tag k='from' v='Duvnäs Utskog' />
        <tag k='route' v='keinbus' />
    </relation>
    <relation id='3468409' version='1'>
        <member type='way' ref='465901030' role='' />
        <member type='way' ref='803487169' role='' />
        <member type='node' ref='2071677724' role='stop' />
        <member type='node' ref='7515926986' role='stop' />
        <tag k='from' v='Duvnäs Utskog' />
        <tag k='route' v='bus' />
    </relation>
    </body>"""

    xml_expected = """<node id="119044" timestamp="2019-11-10T18:18:34Z" uid="83501" user="riiga" visible="true" version="5" changeset="76875955" lat="59.3211049" lon="18.0549223" />
    <relation id="3464444" version="1">
        <member type="way" ref="465901030" role="" />
        <member type="way" ref="803487169" role="" />
        <member type="node" ref="2071677724" role="stop" />
        <member type="node" ref="7515926986" role="stop" />
        <tag k="from" v="Duvnäs Utskog" />
        <tag k="route" v="keinbus" />
    </relation>
    """

    route_list = ['bus','train','railway','bicycle','hiking','ferry','subway']
    restriction_list = ['no_left_turn','no_right_turn','only_left_turn',
                        'only_right_turn','only_straight_on','no_u_turn']
    type_list = ['addr:postcode','addr:city']

    tags_to_remove = dict([
        ("route", route_list),
        ("restriction", restriction_list),
        ("type", type_list)
        ])
    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_02.get_next_first_level_element(input_file):
        if element.tag != "body":
            remove = script_02.is_relation_with_tag(element, tags_to_remove)
            # do not add releations with tags_to_remove
            if remove == False:
                xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out
