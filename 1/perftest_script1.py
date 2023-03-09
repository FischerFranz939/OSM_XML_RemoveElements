'''
Performnce test script for script1

python perftest_script1.py
'''
import script1


INPUT_FILE_NAME = "andorra-latest.osm"


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    '''Configure elements to remove'''
    current_dir = script1.get_current_dir(True)

    file_name_in = current_dir + "/../test/" + INPUT_FILE_NAME
    print("file_name_in: ", file_name_in)

    tree = script1.parse_input_file(file_name_in)
    root = tree.getroot()

    performance_remove_node_elements_with_no_reference(root)


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def create_key_value_string(text, int_value):
    '''Create key value string'''
    return "("+ text +": " + str(int_value) + ")"

#-------------------------------------------------------------------------------
def performance_remove_node_elements_with_no_reference(root):
    '''
    Results for andorra-latest.osm

    find relation reference for ONE node id --> ca.  30ms
    find way      reference for ONE node id --> ca. 100ms

    find ALL nodes and check for exceptions --> ca. 160ms
    number of checked nodes:       329767
    number of nodes not to remove: 228

    => 329767 * (30+100)ms = 11,9h

    calculated:
    --> 1000 * (30+100)ms = 130000 ms (2m 10s)
    program output:
    1000 nodes processed in 113689 ms
    2000 nodes processed in 231838 ms
    3000 nodes processed in 352840 ms
    4000 nodes processed in 470426 ms
    5000 nodes processed in 588397 ms

    !!!! Python kann nur eine CPU nutzen !!!!
    '''
    timer = script1.Timer("performance_remove_node_elements_with_no_reference")

    node_id_no_ref  = '64954477'   #andorra-latest.osm --> no references
    node_id_ref_way = '3020646532' #andorra-latest.osm --> reference to way
    node_id_ref_rel = '766150394'  #andorra-latest.osm --> reference to relation

    performance_number_of_way_references(root, node_id_no_ref)
    performance_number_of_way_references(root, node_id_ref_way)
    performance_number_of_way_references(root, node_id_ref_rel)

    performance_number_of_relation_references(root, node_id_no_ref)
    performance_number_of_relation_references(root, node_id_ref_way)
    performance_number_of_relation_references(root, node_id_ref_rel)

    performance_find_all_nodes(root)

    timer.print_result()

#-------------------------------------------------------------------------------
def performance_find_all_nodes(root):
    '''
    Count all nodes and all nodes which can not be removed.
    Criteria can be e.g. attributes in tags.
    '''
    timer = script1.Timer("performance_find_all_nodes")

    counter_nodes = 0
    counter_not_remove = 0
    for element in root.findall("node"):
        counter_nodes = counter_nodes + 1
        identifier = element.attrib.get("id")
        remove = script1.can_node_be_removed(element)
        if not remove:
            counter_not_remove = counter_not_remove + 1
            print("node can NOT be removed. id: ", identifier)

    print("  number of checked nodes:      ", counter_nodes)
    print("  number of nodes not to remove:", counter_not_remove)

    timer.print_result()

#-------------------------------------------------------------------------------
def performance_number_of_relation_references(root, identifier):
    '''performance measurement - get number of relation references'''
    timer = script1.Timer("performance_number_of_relation_references")
    number = script1.number_of_relation_references(root, identifier)
    timer.print_result(create_key_value_string("found references", number))

#-------------------------------------------------------------------------------
def performance_number_of_way_references(root, identifier):
    '''Performance measurement - get number of way references'''
    timer = script1.Timer("performance_number_of_way_references")
    number = script1.number_of_way_references(root, identifier)
    timer.print_result(create_key_value_string("found references", number))

#-------------------------------------------------------------------------------
if __name__== "__main__":
    main()
