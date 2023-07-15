'''
Test script for script_01 (unit tests)

https://pythontest.com/framework/pytest/pytest-introduction/

python -m pytest -v test_script_01.py

!!!! PATH not supported !!!!
python -m pytest --cov=script_01 test_script_01.py
python -m pytest --cov-report term --cov-report xml:lcov.xml   --cov=script_01 test_script_01.py
python -m pytest --cov-report term --cov-report html:lcov_html --cov=script_01 test_script_01.py
python -m pytest --cov-report term --cov-report lcov:lcov.info --cov=script_01 test_script_01.py
'''
import xml.etree.ElementTree as ET
import filecmp
from pathlib import Path
import script_01


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
def test_remove_element_by_id():
    '''Test - remove_element_by_id'''
# Given
    xml_in = """<body>
    <node id='119044' timestamp='2019-11-10T18:18:34Z' uid='83501' user='riiga' visible='true' version='5' changeset='76875955' lat='59.3211049' lon='18.0549223' />
    <way id='1186083653' timestamp='2023-06-30T21:25:21Z' uid='13583335' user='segikip544' visible='true' version='1' changeset='137974638'>
        <nd ref='11016755871' />
        <nd ref='11016755870' />
        <nd ref='11016755869' />
        <tag k='waterway' v='ditch' />
    </way>
    <relation id='15636238' timestamp='2023-03-24T08:46:20Z' uid='76269' user='Snusmumriken' visible='true' version='1' changeset='134055375'>
        <member type='node' ref='4970897646' role='target' />
        <member type='node' ref='1787546752' role='address' />
        <tag k='type' v='provides_feature' />
    </relation>
    </body>"""

    xml_expected = """<body>
    <node id="119044" version="5" lat="59.3211049" lon="18.0549223" />
    <way id="1186083653" version="1">
        <nd ref="11016755871" />
        <nd ref="11016755870" />
        <nd ref="11016755869" />
        <tag k="waterway" v="ditch" />
    </way>
    <relation id="15636238" version="1">
        <member type="node" ref="4970897646" role="target" />
        <member type="node" ref="1787546752" role="address" />
        <tag k="type" v="provides_feature" />
    </relation>
    </body>"""
    root           = ET.fromstring(xml_in)
    attribute_list = ["timestamp", "user", "uid", "changeset", "visible"]

# When
    script_01.remove_attributes_from_element(root, attribute_list)
    xml_out = ET.tostring(root, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out
