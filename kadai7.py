# coding:utf-8
from xml.dom import minidom
xmldoc = minidom.parse('sample.xml')
itemlist = xmldoc.getElementsByTagName('UML:ActionState')
# print(len(itemlist)) 個数が出る
# print(itemlist[0].attributes['oshikko'].value)
for s in itemlist:
    print(s.attributes['xmi.id'].value)
    print(s.attributes['name'].value)
