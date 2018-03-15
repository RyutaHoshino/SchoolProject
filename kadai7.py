<<<<<<< HEAD
from xml.etree import ElementTree

# XML 文字列をパースして Element オブジェクトを生成
elem = ElementTree.fromstring('<tree name="hello"><trunk>...</trunk></tree>')
print(elem.tag)     #=> tree
print(elem.attrib)  #=> {'name': 'hello'}
=======
# coding:utf-8
from xml.dom import minidom
xmldoc = minidom.parse('sample.xml')
itemlist = xmldoc.getElementsByTagName('UML:ActionState')
# print(len(itemlist)) 個数が出る
# print(itemlist[0].attributes['oshikko'].value)
for s in itemlist:
    print(s.attributes['xmi.id'].value)
    print(s.attributes['name'].value)
>>>>>>> c1c024c5b49085b44741c66041c1d1eb430f2cc4
