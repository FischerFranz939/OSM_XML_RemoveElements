'''
Test script for script2

Calculate file size of outputfiles
'''
import xml.etree.ElementTree as ET
import script1


TEST_PATH = script1.get_current_dir(True) + "/../test/"


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def calculate_savings_in_byte(file_size_begin, file_size_end):
    '''File size in byte'''
    savings = file_size_begin - file_size_end
    print("file_size_begin: ", file_size_begin)
    print("file_size_end:   ", file_size_end)
    print("savings in byte: ", savings)
    return savings

#-------------------------------------------------------------------------------
def calculate_savings_in_percent(file_size_begin, file_size_end):
    '''File size in percent'''
    savings = 100 - (file_size_end/file_size_begin) * 100
    print("savings in percent: ", savings)
    return savings


#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------
def test_remove_buildings_and_nodes():
    '''Test - remove_buildings and not referenced nodes - file size'''
# Given
    file_in  = TEST_PATH + "Neuffen_unbearbeitet.osm"
    file_out = TEST_PATH + "Neuffen_unbearbeitet.output"

    timer = script1.Timer("test_remove_buildings_and_nodes")
    file_size_begin = script1.get_file_size(file_in)

    tree = script1.parse_input_file(file_in)
    root = tree.getroot()
    remove_nodes = True

# When
    script1.remove_buildings(root, remove_nodes)
    script1.write_outputfile_file(tree, file_out)

# Then
    timer.print_result()
    file_size_end = script1.get_file_size(file_out)
    savings_in_byte = calculate_savings_in_byte(file_size_begin, file_size_end)
    savings_in_percent = calculate_savings_in_percent(file_size_begin, file_size_end)
    assert savings_in_byte == 508275
    assert savings_in_percent > 30

#-------------------------------------------------------------------------------
def test_remove_buildings_only():
    '''Test - remove_buildings only (do not remove nodes) - file size'''
# Given
    file_in  = TEST_PATH + "Neuffen_unbearbeitet.osm"
    file_out = TEST_PATH + "Neuffen_unbearbeitet.output"

    timer = script1.Timer("test_remove_buildings_only")
    file_size_begin = script1.get_file_size(file_in)

    tree = script1.parse_input_file(file_in)
    root = tree.getroot()
    remove_nodes = False

# When
    script1.remove_buildings(root, remove_nodes)
    script1.write_outputfile_file(tree, file_out)

# Then
    timer.print_result()
    file_size_end = script1.get_file_size(file_out)
    savings_in_byte = calculate_savings_in_byte(file_size_begin, file_size_end)
    savings_in_percent = calculate_savings_in_percent(file_size_begin, file_size_end)
    assert savings_in_byte == 208563
    assert savings_in_percent > 10


# TODO: generate result file
