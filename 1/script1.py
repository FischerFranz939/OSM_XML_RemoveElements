'''
Script to remove unwanted elements/attributes from XML.
- processes the whole input XML-file

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
import inspect
import os
from pathlib import Path


INPUT_FILE_NAME = "test2_formated.xml"
#INPUT_FILE_NAME = "Neuffen_unbearbeitet.osm"
#INPUT_FILE_NAME = "Neuffen_unbearbeitet_formated_lin.osm"
#INPUT_FILE_NAME = "andorra-latest.osm"


#-------------------------------------------------------------------------------
# Class
#-------------------------------------------------------------------------------
class Timer:
    '''Timer for performance measurements'''
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
        time_used = time_end - self.time_begin
        print(self.function_name, " in ms:", time_used, additional_information)
        return time_used


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    '''Configure elements to remove'''
    test_path = get_current_dir() + "/../test/"

    file_name_in = test_path + INPUT_FILE_NAME
    file_name_out = file_name_in + ".output"
    print("file_name_in: ", file_name_in)
    print("file_name_out: ", file_name_out)

    tree = parse_input_file(file_name_in)
    root = tree.getroot()

    attribute_list = ["timestamp", "user", "uid", "changeset", "visible"]
    remove_attributes_from_element(root, attribute_list)

    #remove_subelement(root, "node", "tag", "power", "tower")
    #remove_elements_by_subelement(root, "node", "tag", "power", "tower")
    #remove_elements_by_subelement(root, "way", "tag", "building", "yes")
    #remove_subelement_by_wildcard(root, "node", "tag", "wiki")

    #remove_node_elements_with_no_reference(root, True)

    #adapt_elements_with_negative_id(root)
    #adapt_subelements_with_negative_references(root)
    #remove_buildings(root)

    write_outputfile_file(tree, file_name_out)


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def remove_buildings(root, remove_nodes=True):
    '''
    Get all "way" elements where the subelement name is "tag" and the subelement
    attribute "k" is "building".
    Get the referenced node IDs for this building (subelement name is "nd" and subelement
    attribute is "ref").
    Remove not referenced "node" elements.
    Remove this element ("way").
    '''
    timer = Timer(str(inspect.stack()[0][3]))
    for element in root.findall("way"):
        if attributes_contained_in_subelement_k(element, "tag", "building"):
            references = get_element_references(element, "nd")
            references.pop() #remove last list-element, because first and last are the same
            root.remove(element) #remove, otherwise the nodes are still referenced
            if remove_nodes:
                remove_nodes_if_not_referenced(root, references)
    timer.print_result()

#-------------------------------------------------------------------------------
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
    timer = Timer(str(inspect.stack()[0][3]))
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
    Get all first level elements "way" and "relation" with negativ references
    in their subelements.
    Negate the ID.
    For ways also remove the attribute "action".
    '''
    timer = Timer(str(inspect.stack()[0][3]))

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
        if identifier < 0:
            element.set("ref", str(identifier * -1))
            #print(element.attrib["ref"])

#-------------------------------------------------------------------------------
def remove_node_elements_with_no_reference(root, print_removed_elements=False):
    '''Remove node elements with no reference'''
    timer = Timer(str(inspect.stack()[0][3]))
    counter_nodes = 0
    counter_remove_nodes = 0
    for element in root.findall("node"):
        counter_nodes = counter_nodes + 1

        # this information costs performance!
        if counter_nodes % 1000==0:
            print(counter_nodes, "nodes processed in", timer.current_time_ms() - \
            timer.get_begin_time_ms(), "ms")

        identifier = element.attrib.get("id")
        if can_node_be_removed(element) and not is_node_id_referenced(root, identifier):
            counter_remove_nodes = counter_remove_nodes + 1
            root.remove(element)
            if print_removed_elements:
                print("  no references, exceptions for id:", identifier, " =>element removed")

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
    '''Get number how often identifier is referenced in relations'''
    return len(root.findall("relation/member/[@ref='" + identifier + "']"))

#-------------------------------------------------------------------------------
def number_of_way_references(root, identifier):
    '''Get number how often identifier is referenced in way elements'''
    return len(root.findall("way/nd/[@ref='" + identifier + "']"))

#-------------------------------------------------------------------------------
def remove_subelement_by_wildcard(root, element_name, subelement_name, k_attribute_wildcard):
    '''Remove subelement by wildcard'''
    timer = Timer(str(inspect.stack()[0][3]))
    for element in root.findall(element_name):
        for subelement in element.findall(subelement_name):
            if k_attribute_wildcard in subelement.attrib.get("k"):
                element.remove(subelement)
    timer.print_result()

#-------------------------------------------------------------------------------
def remove_elements_by_subelement(root, element_name, subelement_name, k_attribute, v_attribute):
    '''Remove elements by subelement'''
    timer = Timer(str(inspect.stack()[0][3]))
    for element in root.findall(element_name):
        if attributes_contained_in_subelement_kv(element, subelement_name, \
            k_attribute, v_attribute):
            root.remove(element)
    timer.print_result()

#-------------------------------------------------------------------------------
def remove_subelement(root, element_name, subelement_name, k_attribute, v_attribute):
    '''Remove subelement by attributes'''
    timer = Timer(str(inspect.stack()[0][3]))
    for element in root.findall(element_name):
        for subelement in element.findall(subelement_name):
            if (subelement.attrib.get("k") == k_attribute) and \
                (subelement.attrib.get("v") == v_attribute):
                element.remove(subelement)
    timer.print_result()

#-------------------------------------------------------------------------------
def remove_attribute_from_element(root, target_attribute):
    '''Remove attribute from element'''
    timer = Timer(str(inspect.stack()[0][3]))
    x_path = "./*[@" + target_attribute + "]"
    for element in root.findall(x_path):
        #print(element.attrib[target_attribute])
        del element.attrib[target_attribute]
    timer.print_result()

#-------------------------------------------------------------------------------
def remove_attributes_from_element(root, target_attributes):
    '''Remove attributes from element'''
    timer = Timer(str(inspect.stack()[0][3]))
    for target_attribute in target_attributes:
        remove_attribute_from_element(root, target_attribute)
    timer.print_result()

#-------------------------------------------------------------------------------
def write_outputfile_file(tree, file_out, linux_eol=True):
    '''
    Export ElementTree object to file
    '''
    timer = Timer(str(inspect.stack()[0][3]))
    tree.write(file_out, encoding="utf-8", xml_declaration=True)

    if linux_eol:
        file_name_tmp = file_out + ".tmp"
        os.rename(file_out, file_name_tmp)
        write_linux_line_endings(file_name_tmp, file_out)
        os.remove(file_name_tmp)

    timer.print_result()

#-------------------------------------------------------------------------------
def write_linux_line_endings(file_in, file_out):
    '''
    https://stackoverflow.com/questions/36422107/how-to-convert-crlf-to-lf-on-a-windows-machine-in-python
    https://stackoverflow.com/questions/20350305/python-read-crlf-text-file-as-is-with-crlf
    https://stackoverflow.com/questions/9184107/how-can-i-force-pythons-file-write-to-use-the-same-newline-format-in-windows
    https://stackoverflow.com/questions/70893097/how-to-preserve-the-original-encoding-and-line-endings-when-writing-to-a-file
    '''
    timer = Timer(str(inspect.stack()[0][3]))

    with open(file_in, 'rb') as open_file:
        content = open_file.read()

    # replacement strings; Windows --> Unix
    windows_line_endings = b'\r\n'
    linux_line_endings = b'\n'
    content = content.replace(windows_line_endings, linux_line_endings)

    # remove space
    space = b' />'
    no_space = b'/>'
    content = content.replace(space, no_space)

    with open(file_out, 'wb') as open_file:
        open_file.write(content)

    timer.print_result()

#-------------------------------------------------------------------------------
def parse_input_file(file_in):
    '''Import file to ElementTree object'''
    timer = Timer(str(inspect.stack()[0][3]))
    tree = ET.parse(file_in)
    timer.print_result()
    return tree

#-------------------------------------------------------------------------------
def get_current_dir():
    '''Get current directory'''
    return str(Path(__file__).parent.resolve())

#-------------------------------------------------------------------------------
if __name__== "__main__":
    main()
