'''
Program to remove unwanted elements from XML.
(processes the whole input XML-file)

-------------------------------------------------------------------------------
 Naming, Notes...
-------------------------------------------------------------------------------
<ROOT_ELEMENT_NAME                  ATTRIBUTE_NAME=ATTRIBUTE_VALUE>
    <FIRST_LEVEL_ELEMENT_NAME       ATTRIBUTE_1="123" ATTRIBUTE_2="hello">
        <SECOND_LEVEL_ELEMENT_NAME  ATTRIBUTE_1="123" ATTRIBUTE_2="hello"> />
    </node>
</osm>

ROOT_ELEMENT_NAME is osm
FIRST_LEVEL_ELEMENT_NAME can be node, way, relation...
The SECOND_LEVEL_ELEMENT is a subelement from the FIRST_LEVEL_ELEMENT

For simplification, the first level element will be (mostly) called just "element"
and the second level element will be (mostly) called "subelement" (of the
first level element).

Note:
working with xpath...there ist no "get_parent()" function to get the parent
element of a subelement!

-------------------------------------------------------------------------------
TODOs:
-------------------------------------------------------------------------------
 - remove blank at element angle-bracket
   e.g. <tag k="building" v="yes" /> (save one byte per line)
 - use linux line endings (save one byte per line)
'''

import xml.etree.ElementTree as ET
import time
import pathlib


INPUT_FILE_NAME = "test2_formated.xml"
#INPUT_FILE_NAME = "Neuffen_unbearbeitet.osm"
#INPUT_FILE_NAME = "andorra-latest.osm"


#-------------------------------------------------------------------------------
# Class
#-------------------------------------------------------------------------------
class Timer:
    '''Timer for performance measurements'''
    function_name = ""
    time_begin = 0

    def __init__(self, function_name):
        """Init method"""        
        self.function_name = function_name
        self.time_begin = self.current_time_ms()

    def begin_time_ms(self):
        """Begin time"""        
        return self.time_begin

    def current_time_ms(self):
        """Get current time"""        
        return round(time.time() * 1000)

    def print_result(self, additional_information=""):
        """Print result"""        
        time_end = self.current_time_ms()
        print(self.function_name, " in ms:", time_end - self.time_begin, additional_information)


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    '''Configure elements to remove'''
    current_dir = str(pathlib.Path(__file__).parent.resolve())
    print("current_dir: ", current_dir)

    xml_file_in = current_dir + "\\..\\test\\" + INPUT_FILE_NAME
    xml_file_out = current_dir + "\\" + INPUT_FILE_NAME + ".output"
    print("xml_file_in: ", xml_file_in)
    print("xml_file_out: ", xml_file_out)

    tree = parse_input_file(xml_file_in)
    root = tree.getroot()

    attribute_list = ["timestamp", "user", "uid", "changeset", "visible"]
    remove_attributes_from_element(root, attribute_list)

    #format_input_file(tree, ml_file_out)
    #remove_subelement(root, "node", "tag", "power", "tower")
    #remove_elements_by_subelement(root, "node", "tag", "power", "tower")
    #remove_elements_by_subelement(root, "way", "tag", "building", "yes")
    #remove_subelement_by_wildcard(root, "node", "tag", "wiki")

    #remove_node_elements_with_no_reference(root, True)
    #performance_remove_node_elements_with_no_reference(root)

    #adapt_elements_with_negative_id(root)
    adapt_subelements_with_negative_references(root)
    #remove_buildings(root)

    write_outputfile_file(tree, xml_file_out)


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def remove_buildings(root):
    '''
    Get all "way" elements where the subelement name is "tag" and the subelement
    attribute "k" is "building".
    Get the referenced node IDs for this building (subelement name is "nd" and subelement
    attribute is "ref").
    Remove not referenced "node" elements.
    Remove this element ("way").
    '''
    timer = Timer("remove_buildings")
    for element in root.findall("way"):
        if attributes_contained_in_subelement_k(element, "tag", "building"):
            references = get_element_references(element, "nd")
            references.pop() #remove last list-element, because first and last are the same
            root.remove(element) #remove, otherwise the nodes are still referenced
            remove_nodes_if_not_referenced(root, references)
    timer.print_result()

#-------------------------------------------------------------------------------test
def remove_element_by_id(root, element_name, identifier):
    '''
    Remove all first level elements for the given "element_name" and the given "id"
    attribute value.
    '''
    for element in root.findall(element_name + "[@id='" + identifier + "']"):
        root.remove(element)

#-------------------------------------------------------------------------------
def remove_nodes_if_not_referenced(root, node_ids):
    '''
    Check for each node element ID whether the ID is part of a "relation" or a "way".
    If the node is not referenced, remove the node element.
    '''
    for node_id in node_ids:
        if not is_node_id_referenced(root, node_id):
            remove_element_by_id(root, "node", node_id)

#-------------------------------------------------------------------------------
def is_node_id_referenced(root, node_id):
    '''Check if the node element ID is part of a "relation" or a "way".'''
    result = False

    if number_of_relation_references(root, node_id) > 0:
        result = True
    else:
        if number_of_way_references(root, node_id) > 0:
            result = True

    return result

#-------------------------------------------------------------------------------
def get_element_references(element, subelement_name):
    '''
    Get a list of "ref" attribute values for all, with subelement_name specified,
    subelements of the given element.
    '''
    references = []

    for subelement in element.findall(subelement_name):
        references.append(subelement.attrib.get("ref"))

    return references

#-------------------------------------------------------------------------------
def attributes_contained_in_subelement_kv(element, subelement_name, k_attribute, v_attribute):
    '''
    Check whether a first level element contains a subelement with the given values
    for the attribute "k" and "v".
    '''
    result = False

    for subelement in element.findall(subelement_name):
        if (subelement.attrib.get("k") == k_attribute) and \
           (subelement.attrib.get("v") == v_attribute):
            result = True
            break

    return result

#-------------------------------------------------------------------------------
def attributes_contained_in_subelement_k(element, subelement_name, k_attribute):
    '''
    Check whether a first level element contains a subelement with the given value
    for the attribute "k".
    '''
    result = False

    for subelement in element.findall(subelement_name):
        if subelement.attrib.get("k") == k_attribute:
            result = True
            break

    return result

#-------------------------------------------------------------------------------
def adapt_elements_with_negative_id(root):
    '''
    Get all first level elements "node", "way" and "relation" with negativ IDs.
    Negate the ID.
    Replace action="modify" with version="1".
    '''
    timer = Timer("adapt_elements_with_negative_id")

    element_names = ["node", "way", "relation"]

    for element_name in element_names:
        for element in root.findall(element_name):
            attrib_id = int(element.attrib.get("id"))
            if attrib_id < 0:
                element.set("id", str(attrib_id * -1))
                if element.attrib.get("action") == "modify":
                    element.set("version", "1")
                    del element.attrib["action"]

    timer.print_result()

#-------------------------------------------------------------------------------
def adapt_subelements_with_negative_references(root):
    '''
    Get all first level elements "way" and "relation" with negativ references in their
    subelements.
    Negate the ID.
    For ways also remove the attribute "action".
    '''
    timer = Timer("adapt_subelements_with_negative_references")

    for element in root.findall("way"):
        for subelement in element.findall("nd"):
            ref = int(subelement.attrib.get("ref"))
            if ref < 0:
                #print(subelement.attrib["ref"])
                subelement.set("ref", str(ref * -1))
                if element.attrib.get("action") == "modify":
                    del element.attrib["action"]

#    change_negative_references_to_positive(root, "way/nd/[@ref]")
    change_negative_references_to_positive(root, "relation/member/[@ref]")

    timer.print_result()

#-------------------------------------------------------------------------------
def change_negative_references_to_positive(root, x_path):
    '''Negate negative reference IDs for the given xpath'''
    for element in root.findall(x_path):
        identifier = int(element.attrib.get("ref"))
        if id < 0:
            element.set("ref", str(identifier * -1))
            #print(element.attrib["ref"])

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
    timer = Timer("performance_remove_node_elements_with_no_reference")

    node_id_no_ref  = '64954477'   #andorra-latest.osm --> no references
    node_id_ref_way = '3020646532' #andorra-latest.osm --> reference to way
    node_id_ref_rel = '766150394'  #andorra-latest.osm --> reference to relation

    performance_number_of_way_references(root, node_id_no_ref,  "no_ref ")
    performance_number_of_way_references(root, node_id_ref_way, "ref_way")
    performance_number_of_way_references(root, node_id_ref_rel, "ref_rel")

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
    timer = Timer("performance_find_all_nodes")

    counter_nodes = 0
    counter_not_remove = 0
    for element in root.findall("node"):
        counter_nodes = counter_nodes + 1
        identifier = element.attrib.get("id")
        remove = can_node_be_removed(element)
        if not remove:
            counter_not_remove = counter_not_remove + 1
            print("node can NOT be removed. id: ", identifier)

    print("  number of checked nodes:      ", counter_nodes)
    print("  number of nodes not to remove:", counter_not_remove)

    timer.print_result()

#-------------------------------------------------------------------------------
def performance_number_of_relation_references(root, identifier):
    '''performance measurement - get number of relation references'''
    timer = Timer("performance_number_of_relation_references")
    number = number_of_relation_references(root, identifier)
    timer.print_result(create_key_value_string("found references", number))

#-------------------------------------------------------------------------------
def performance_number_of_way_references(root, identifier):
    '''Performance measurement - get number of way references'''
    timer = Timer("performance_number_of_way_references")
    number = number_of_way_references(root, identifier)
    timer.print_result(create_key_value_string("found references", number))

#-------------------------------------------------------------------------------
def create_key_value_string(text, int_value):
    '''Create key value string'''
    return "("+ text +": " + str(int_value) + ")"

#-------------------------------------------------------------------------------
def remove_node_elements_with_no_reference(root, print_removed_elements=False):
    '''Remove node elements with no reference'''
    timer = Timer("remove_node_elements_with_no_reference")
    counter_nodes = 0
    counter_remove_nodes = 0
    for element in root.findall("node"):
        counter_nodes = counter_nodes + 1

        # this information costs performance!
        if counter_nodes % 1000==0:
            print(counter_nodes, "nodes processed in", timer.current_time_ms() - \
            timer.get_begin_time_ms(), "ms")

        id = element.attrib.get("id")
        if can_node_be_removed(element) and not is_node_id_referenced(root, id):
            counter_remove_nodes = counter_remove_nodes + 1
            root.remove(element)
            if print_removed_elements:
                print("  no references, exceptions for id:", id, " =>element removed")

    print("  number of checked nodes:      ", counter_nodes)
    print("  number of nodes not to remove:", counter_remove_nodes)
    timer.print_result()

#-------------------------------------------------------------------------------
def can_node_be_removed(element):
    '''
    Check if a node can be removed or not. 
    Criteria can be e.g. attributes in tags
    '''
    result = True

    # check for exceptions
    for subelement in element.findall("tag"):
        # Example: do not remove peaks
        if subelement.attrib.get("k") == "natural" and \
           subelement.attrib.get("v") == "peak":
            result = False

    return result

#-------------------------------------------------------------------------------
def number_of_relation_references(root, identifier):
    '''Get number of relation references'''
    return len(root.findall("relation/member/[@ref='" + identifier + "']"))

#-------------------------------------------------------------------------------
def number_of_way_references(root, identifier):
    '''Get number of way references'''
    return len(root.findall("way/nd/[@ref='" + identifier + "']"))

#-------------------------------------------------------------------------------test
def remove_subelement_by_wildcard(root, element_name, subelement_name, k_attribute_wildcard):
    '''Remove subelement by wildcard'''
    timer = Timer("remove_subelement_by_wildcard")
    for element in root.findall(element_name):
        for subelement in element.findall(subelement_name):
            if k_attribute_wildcard in subelement.attrib.get("k"):
                element.remove(subelement)
    timer.print_result()

#-------------------------------------------------------------------------------
def format_input_file(tree, file_out):
    '''Format input file'''
    timer = Timer("format_input_file")
    write_outputfile_file(tree, file_out)
    timer.print_result()

#-------------------------------------------------------------------------------test
def remove_elements_by_subelement(root, element_name, subelement_name, k_attribute, v_attribute):
    '''Remove elements by subelement'''
    timer = Timer("remove_elements_by_subelement")
    for element in root.findall(element_name):
        if attributes_contained_in_subelement_kv(element, subelement_name, \
            k_attribute, v_attribute):
            root.remove(element)
    timer.print_result()

#-------------------------------------------------------------------------------test
def remove_subelement(root, element_name, subelement_name, k_attribute, v_attribute):
    '''Remove subelement by attributes'''
    timer = Timer("remove_subelement")
    for element in root.findall(element_name):
        for subelement in element.findall(subelement_name):
            if (subelement.attrib.get("k") == k_attribute) and \
                (subelement.attrib.get("v") == v_attribute):
                element.remove(subelement)
    timer.print_result()

#-------------------------------------------------------------------------------test
def remove_attribute_from_element(root, target_attribute):
    '''Remove attribute from element'''
    timer = Timer("remove_attribute_from_element")
    x_path = "./*[@" + target_attribute + "]"
    for element in root.findall(x_path):
        #print(element.attrib[target_attribute])
        del element.attrib[target_attribute]
    timer.print_result()

#-------------------------------------------------------------------------------test
def remove_attributes_from_element(root, target_attributes):
    '''Remove attributes from element'''
    timer = Timer("remove_attributes_from_element")
    for target_attribute in target_attributes:
        remove_attribute_from_element(root, target_attribute)
    timer.print_result()

#-------------------------------------------------------------------------------
def write_outputfile_file(tree, file_out):
    '''Export ElementTree object to file'''
    timer = Timer("write_outputfile_file")
    tree.write(file_out, encoding="utf-8", xml_declaration=True)
    timer.print_result()

#-------------------------------------------------------------------------------
def parse_input_file(file_in):
    '''Import file to ElementTree object'''
    timer = Timer("parse_input_file")
    tree = ET.parse(file_in)
    timer.print_result()
    return tree

#-------------------------------------------------------------------------------
if __name__== "__main__":
    '''Main function'''
    main()
