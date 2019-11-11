import xml.etree.ElementTree as ET

def parse(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    for child in root:
        print(child.tag, child.attrib)

def test():
    parse('get_mjlog/download/mjlog/2018010100gm-00a9-0000-0d318262.mjlog')

if __name__ == '__main__':
    test()
