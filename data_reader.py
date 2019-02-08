import xml.etree.ElementTree as ET

XML_FILE_NAMES = ['Users', 'Posts', 'Comments', 'Votes']

def __read_xml_file__(file_name):
    return ET.parse(file_name).getroot()

def __get_xml_dict__(dir_path):
    xml_dict = dict()
    for file_name in XML_FILE_NAMES:
        path = f"{dir_path}/{file_name}.xml"
        xml_dict.update({file_name : __read_xml_file__(path)})
    return xml_dict

def get_stackoverflow_data(dir_path):
    return __get_xml_dict__(dir_path)