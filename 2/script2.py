'''
Script to remove unwanted elements/attributes from XML.
- only string operations are possible (no XML operations)
- processes input XML-file in chunks

https://stackoverflow.com/questions/16669428/process-very-large-20gb-text-file-line-by-line
https://gist.github.com/iyvinjose/e6c1cb2821abd5f01fd1b9065cbc759d
https://stackoverflow.com/a/519653/5130720

'''
import time
import pathlib


INPUT_FILE_NAME = "test2.xml"
#INPUT_FILE_NAME = "andorra-latest.osm"
CHUNK_SIZE = 5000 #configure CHUNK_SIZE (data read at a time) based on your system RAM.


#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
def main():
    '''
    Configure callback function to remove strings from file.
    Process_lines_from_file: read file chunks and give one line after the other
    to the callback function
    callback function: process one single line of the file at a time
    '''
    time_begin = current_time_ms()
    current_dir = str(pathlib.Path(__file__).parent.resolve())
    print("current_dir: ", current_dir)

    xml_file_in = current_dir + "\\..\\test\\" + INPUT_FILE_NAME
    xml_file_out = current_dir + "\\" + INPUT_FILE_NAME + ".output"
    print("xml_file_in: ", xml_file_in)
    print("xml_file_out: ", xml_file_out)

    file_in = open(xml_file_in, mode="r", encoding="utf-8", newline="\n")
    file_out = open(xml_file_out, mode="w", encoding="utf-8", newline="\n")

    #1
    # chunk_counter = process_lines_from_file(file_in, file_out,
    # chunk_size=CHUNK_SIZE, callback=process_timestamps)

    #2
    chunk_counter = process_lines_from_file(file_in, file_out, chunk_size=CHUNK_SIZE, callback=process_tags)

    time_end = current_time_ms()
    print("time in ms: ", time_end - time_begin)
    print("chunk counter: ", chunk_counter)


#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
# callback function
def process_timestamps(data, eof, file_out):
    '''Callback function remove timestamps'''
    # check if end of file reached
    if not eof:
        # process data, data is one single line of the file
        data = remove_timestamp_from_string(data)
        file_out.write(data + "\n")
    #else:
        # end of file reached

#-------------------------------------------------------------------------------
# callback function
def process_tags(data, eof, file_out):
    '''Callback function remove tags'''
    # check if end of file reached
    if not eof:
        # process data, data is one single line of the file
        write_data = write_tag(data)
        if write_data:
            file_out.write(data + "\n")
    #else:
        # end of file reached

#-------------------------------------------------------------------------------
def write_tag(data):
    '''Configure tags to be removed'''
    remove_tags = ["source", "wiki", "url:", "ele", "created_by", "addr", "brand"]
    keep_name_tags = ["de", "en", "sv", "fi", "no"]
    write_data = True
    tag_found = False

    if is_subelement_tag(data):
        # check for tags to remove
        for tag in remove_tags:
            if target_found(data, tag):
                tag_found = True
                write_data = False
                break

        # check for name-tags to keep
        if not tag_found and is_name_tag(data):
            for tag in keep_name_tags:
                if target_found(data, tag, "name:"):
                    write_data = True
                    break
                else:
                    write_data = False

    return write_data

#-------------------------------------------------------------------------------
def is_name_tag(data):
    '''Returns true if tag has key name'''
    return target_found(data, "", k_name = "name:")

#-------------------------------------------------------------------------------
def target_found(data, tag, k_name = ""):
    '''Returns true if tag exists'''
    found = False

    index1 = data.find('<tag k="' + k_name + tag)
    index2 = data.find("<tag k='" + k_name + tag)
    if index1 > 0 or index2 > 0:
        found = True
        #print('<tag k="' + k_name + tag)

    return found

#-------------------------------------------------------------------------------
def is_subelement_tag(data):
    '''Returns true if tag is in subelement'''
    is_tag = False
    index = data.find("<tag k=")
    if index > 0:
        is_tag = True
    return is_tag

#-------------------------------------------------------------------------------
def remove_timestamp_from_string(data):
    '''Remove timestamp from string'''
    target = " timestamp" #search including the blanc!
    index_begin = data.find(target)
    if index_begin > 0:
        index_end = index_begin + len("timestamp='2020-05-05T13:16:49Z'") + 1
        data = data[0 : index_begin : ] + data[index_end : : ]
    return data

#-------------------------------------------------------------------------------
def read_in_chunks(file_obj, chunk_size=5000):
    '''read file in chunks'''
    print("chunk size: ", chunk_size, "bytes")

    while True:
        data = file_obj.read(chunk_size)
        if not data:
            break
        yield data

#-------------------------------------------------------------------------------
def process_lines_from_file(file_in, file_out, chunk_size, callback, return_whole_chunk=False):
    '''
    read file line by line regardless of its size
    :param chunk_size: size of data to be read at at time
    :param callback: callback method, prototype ----> def callback(data, eof, file_out)
    '''
    chunk_counter = 0
    data_left_over = None

    # loop through characters
    for chunk in read_in_chunks(file_in, chunk_size):
        chunk_counter = chunk_counter + 1

        # if uncompleted data exists
        if data_left_over:
            # print('\n left over found')
            current_chunk = data_left_over + chunk
        else:
            current_chunk = chunk

        # split chunk by new line
        lines = current_chunk.splitlines()

        # check if line is complete
        if current_chunk.endswith('\n'):
            data_left_over = None
        else:
            data_left_over = lines.pop()
        if return_whole_chunk:
            callback(data=lines, eof=False, file_out=file_out)
        else:
            for line in lines:
                callback(data=line, eof=False, file_out=file_out)
                pass

    if data_left_over:
        current_chunk = data_left_over
        if current_chunk is not None:
            lines = current_chunk.splitlines()
            if return_whole_chunk:
                callback(data=lines, eof=False, file_out=file_out)
            else:
                for line in lines:
                    callback(data=line, eof=False, file_out=file_out)
                    pass

    callback(data=None, eof=True, file_out=file_out)
    return chunk_counter

#-------------------------------------------------------------------------------
def current_time_ms():
    '''Get current time'''
    return round(time.time() * 1000)

#-------------------------------------------------------------------------------
if __name__== "__main__":
    main()
