# coding: UTF-8
import xml.etree.ElementTree as ET
def trace(parent):
    for node in list(parent):
        print(root.find(".///UML:ActionState").text)
        trace(node)

tree = ET.parse("sample.xml")
root = tree.getroot()
trace(root)
