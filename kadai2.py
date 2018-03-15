# coding: UTF-8
import xml.etree.ElementTree as ET
def trace(parent):
    for node in list(parent):
        print(root.find(".//benki").text)
        trace(node)

tree = ET.parse("sample2.xml")
root = tree.getroot()
trace(root)
