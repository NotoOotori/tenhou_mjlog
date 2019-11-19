from re import fullmatch
import xml.etree.ElementTree as ET
from element import *

TAGS = ('SHUFFLE', 'GO', 'UN')

def parse(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    for child in root:
        if child.tag in TAGS:
            print(globals()[child.tag.title()](child).to_string())
        if fullmatch('[D-G]([0-9]|[0-9][0-9]|[0-1][0-9][0-9])', child.tag):
            print(Draw(child).to_string())

def test():
    parse('get_mjlog/download/mjlog/2018010100gm-00a9-0000-0d318262.mjlog')

if __name__ == '__main__':
    test()
