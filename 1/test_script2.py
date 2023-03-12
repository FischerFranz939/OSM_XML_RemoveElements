'''
Test script for script1 (report time and savings)

Calculate file size of outputfiles
'''
import xml.etree.ElementTree as ET
import script1
import os
import inspect
import time
from pathlib import Path


INPUT_FILE_NAME = "Neuffen_unbearbeitet.osm"
#INPUT_FILE_NAME = "andorra-latest.osm"
#INPUT_FILE_NAME = "test2_formated.xml"
#INPUT_FILE_NAME = "test3.xml"

TEST_PATH = script1.get_current_dir() + "/../test/"
FILE_IN  = TEST_PATH + INPUT_FILE_NAME
REPORT_FILE_NAME = TEST_PATH + "Report_test_script2.output"
REPORT_FILE = open(REPORT_FILE_NAME, "w")


#-------------------------------------------------------------------------------
# Class
#-------------------------------------------------------------------------------
class Report:
    '''Report measurements'''
    file_name_in  = ""
    file_name_out  = ""
    file_size_begin = 0
    file_size_end = 0
    time_begin = 0
    time_end = 0
    function_name = ""
    report_file = ""

    def __init__(self, function_name, file_name_in, report_file):
        """Init method"""
        self.function_name = function_name
        self.file_name_in = file_name_in
        self.file_name_out = self.create_file_name_out()
        self.report_file = report_file
        self.file_size_begin = Path(file_name_in).stat().st_size
        # start measurement
        self.time_begin = round(time.time() * 1000)

    def create_file_name_out(self):
        '''Create name of outputfile file  '''
        #file_name_in = os.path.splitext(self.file_name_in)[0]
        return self.file_name_in + "-" + self.function_name + ".output"

    def get_file_name_out(self):
        '''Get output file name '''
        return self.file_name_out

    def savings_byte(self):
        '''Difference between input- and output-file in byte'''
        return self.file_size_begin - self.file_size_end

    def savings_percent(self):
        '''Difference between input- and output-file in percent'''
        savings = 100 - (self.file_size_end/self.file_size_begin) * 100
        savings = round(savings, 1)
        return savings

    def time_used_ms(self):
        '''Time between start and end of measurement'''
        return self.time_end - self.time_begin

    def stop_measurement(self):
        '''End of measurement, stop time and get file size'''
        self.time_end = round(time.time() * 1000)
        self.file_size_end = Path(self.file_name_out).stat().st_size

    def convert_ms(self):
        '''Convert milliseconds to seconds'''
        result = ""
        milli = self.time_used_ms()
        # return milliseconds
        if milli < 1000:
            result = "time used in ms:   " + str(milli) + "\n"
        # return seconds
        else:
            seconds = round(milli/1000, 1)
            result = "time used in  s:   " + str(seconds) + "\n"
        return result

    def convert_bytes(self, bytes, indent=True):
        '''Convert bytes to kB or MB'''
        result = ""
        kilo = 1024
        indent_x ="           "

        # return bytes
        if bytes < kilo:
            result = "byte:   " + str(bytes) + "\n"
        # return kilo bytes
        elif bytes >= kilo and bytes < (kilo*kilo):
            kb = round(bytes/kilo, 1)
            result = "  kB:   " + str(kb) + "\n"
        # return mega bytes
        else:
            mb = round(bytes/(kilo*kilo), 1)
            result = "  MB:   " + str(mb) + "\n"

        if indent:
            result = indent_x + result
        return result

    def write_report(self):
        '''Write result into report file'''
        self.stop_measurement()

        self.report_file.write(">>>>>> " + self.function_name + " <<<<<<\n")
        #directory = os.path.dirname(self.file_name_in)
        file_in = os.path.basename(self.file_name_in)
        #file_out = os.path.basename(self.file_name_out)
        #self.report_file.write("directory:         " + directory + "\n")
        self.report_file.write("input file name:   " + file_in + "\n")
        self.report_file.write(self.convert_bytes(self.file_size_begin))
        #self.report_file.write("output file name:  " + file_out + "\n")
        #self.report_file.write(self.convert_bytes(self.file_size_end))
        self.report_file.write("Savings    ")
        self.report_file.write(self.convert_bytes(self.savings_byte(), False))
        self.report_file.write("     in percent:   " + str(self.savings_percent()) + "\n")
        self.report_file.write(self.convert_ms() + "\n")


#-------------------------------------------------------------------------------
# Fixture
#-------------------------------------------------------------------------------
#@pytest.fixture(scope="session")


#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------
def test_remove_buildings_and_nodes():
    '''Test - remove_buildings and not referenced nodes'''
# Given
    report = Report(str(inspect.stack()[0][3]), FILE_IN, REPORT_FILE)
    tree = script1.parse_input_file(FILE_IN)
    root = tree.getroot()
    remove_nodes = True

# When
    script1.remove_buildings(root, remove_nodes)
    script1.write_outputfile_file(tree, report.get_file_name_out())

# Then
    report.write_report()

#-------------------------------------------------------------------------------
def test_remove_buildings_only():
    '''Test - remove_buildings only (do not remove nodes)'''
# Given
    report = Report(str(inspect.stack()[0][3]), FILE_IN, REPORT_FILE)
    tree = script1.parse_input_file(FILE_IN)
    root = tree.getroot()
    remove_nodes = False

# When
    script1.remove_buildings(root, remove_nodes)
    script1.write_outputfile_file(tree, report.get_file_name_out())

# Then
    report.write_report()

#-------------------------------------------------------------------------------
def test_remove_attributes_from_element():
    '''Test - remove_attributes_from_element'''
# Given
    report = Report(str(inspect.stack()[0][3]), FILE_IN, REPORT_FILE)
    tree = script1.parse_input_file(FILE_IN)
    root = tree.getroot()
    attribute_list = ["timestamp", "user", "uid", "changeset", "visible"]

# When
    script1.remove_attributes_from_element(root, attribute_list)
    script1.write_outputfile_file(tree, report.get_file_name_out())

# Then
    report.write_report()

#-------------------------------------------------------------------------------
def test_remove_elements_by_subelement_power_tower():
    '''Test - remove_elements_by_subelement power_tower'''
# Given
    report = Report(str(inspect.stack()[0][3]), FILE_IN, REPORT_FILE)
    tree = script1.parse_input_file(FILE_IN)
    root = tree.getroot()

# When
    script1.remove_elements_by_subelement(root, "node", "tag", "power", "tower")
    script1.write_outputfile_file(tree, report.get_file_name_out())

# Then
    report.write_report()

#-------------------------------------------------------------------------------
def test_remove_subelement_by_wildcard_wiki():
    '''Test - remove_subelement_by_wildcard wiki'''
# Given
    report = Report(str(inspect.stack()[0][3]), FILE_IN, REPORT_FILE)
    tree = script1.parse_input_file(FILE_IN)
    root = tree.getroot()

# When
    script1.remove_subelement_by_wildcard(root, "node", "tag", "wiki")
    script1.remove_subelement_by_wildcard(root, "relation", "tag", "wiki")
    script1.remove_subelement_by_wildcard(root, "way", "tag", "wiki")
    script1.write_outputfile_file(tree, report.get_file_name_out())

# Then
    report.write_report()

#-------------------------------------------------------------------------------
def test_all():
    '''Test - all'''
# Given
    report = Report(str(inspect.stack()[0][3]), FILE_IN, REPORT_FILE)
    tree = script1.parse_input_file(FILE_IN)
    root = tree.getroot()
    remove_nodes = True
    attribute_list = ["timestamp", "user", "uid", "changeset", "visible"]

# When
    script1.remove_buildings(root, remove_nodes)

    script1.remove_attributes_from_element(root, attribute_list)

    script1.remove_elements_by_subelement(root, "node", "tag", "power", "tower")

    script1.remove_subelement_by_wildcard(root, "node", "tag", "wiki")
    script1.remove_subelement_by_wildcard(root, "relation", "tag", "wiki")
    script1.remove_subelement_by_wildcard(root, "way", "tag", "wiki")

    script1.remove_subelement_by_wildcard(root, "node", "tag", "wiki")
    script1.remove_subelement_by_wildcard(root, "relation", "tag", "wiki")
    script1.remove_subelement_by_wildcard(root, "way", "tag", "wiki")
    script1.write_outputfile_file(tree, report.get_file_name_out())

# Then
    report.write_report()

#-------------------------------------------------------------------------------
def test_close_report_file():
    REPORT_FILE.close()
