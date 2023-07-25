'''
Test script for script_04 (unit tests)

https://pythontest.com/framework/pytest/pytest-introduction/

python -m pytest -v test_script_04.py

!!!! PATH not supported !!!!
python -m pytest --cov=script_04 test_script_04.py
python -m pytest --cov-report term --cov-report xml:lcov.xml   --cov=script_04 test_script_04.py
python -m pytest --cov-report term --cov-report html:lcov_html --cov=script_04 test_script_04.py
python -m pytest --cov-report term --cov-report lcov:lcov.info --cov=script_04 test_script_04.py
'''
import xml.etree.ElementTree as ET
from pathlib import Path
from io import StringIO
import script_04


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
def test_remove_nodes_outside_poligon():
    '''Test - remove_nodes_outside_poligon'''
# Given
    xml_in = """<body>
    <node id='119052' timestamp='2019-02-12T20:23:37Z' uid='76269' user='Snusmumriken' visible='true' version='6' changeset='67143140' lat='59.3238336' lon='18.0645859' />
    <node id='119053' timestamp='2011-05-25T12:43:56Z' uid='28775' user='StellanL' visible='true' version='5' changeset='8244422'      lat='59.3238915' lon='18.065482' />
    <node id='119050' timestamp='2019-05-10T20:39:58Z' uid='83501' user='riiga' visible='true' version='5' changeset='70124104'        lat='59.3243812' lon='18.0623317' />
    <node id='119046' timestamp='2019-05-10T20:39:58Z' uid='83501' user='riiga' visible='true' version='10' changeset='70124104'       lat='59.3246543' lon='18.0621385' />
    <node id='119047' timestamp='2018-11-14T09:47:02Z' uid='2168173' user='MicDK' visible='true' version='8' changeset='64475193'      lat='59.3252584' lon='18.0618811' />
    <node id='119048' timestamp='2011-04-18T18:54:30Z' uid='76269' user='Snusmumriken' visible='true' version='8' changeset='7900062'  lat='59.3257578' lon='18.0614448' />
    </body>"""

    xml_expected = """<node id="119050" timestamp="2019-05-10T20:39:58Z" uid="83501" user="riiga" visible="true" version="5" changeset="70124104" lat="59.3243812" lon="18.0623317" />
    <node id="119046" timestamp="2019-05-10T20:39:58Z" uid="83501" user="riiga" visible="true" version="10" changeset="70124104" lat="59.3246543" lon="18.0621385" />
    """

    #          longitude, latitude
    polygon = [(18.0621384, 59.3246544),  # top left
               (18.0623318, 59.3246544),  # top right
               (18.0621384, 59.3243811),  # bottom left
               (18.0623318, 59.3243811)]  # bottom right

    input_file = StringIO(xml_in)

# When
    xml_out = ""
    for element in script_04.get_next_first_level_element(input_file):
        if element.tag != "body":
            remove = script_04.remove_nodes_outside_poligon(element, polygon)
            if remove == False:
                xml_out =  xml_out + ET.tostring(element, encoding="unicode", method="xml")

# Then
    print_xmls(xml_in, xml_out, xml_expected)
    assert xml_expected == xml_out
