# coding:utf-8
from xml.dom import minidom
xmldoc = minidom.parse('sample.xml')
itemlist = xmldoc.getElementsByTagName('UML:ActionState')
# print(len(itemlist)) 個数が出る
# print(itemlist[0].attributes['oshikko'].value)
# import pdb; pdb.set_trace()
for s in itemlist:
    try:
        if s.attributes['xmi.id']:
            print(s.attributes['xmi.id'].value)
    except Exception as e:
        print ('何らかのエラー発生')
    else:
        # 成功したときの処理
        print("通過した。")
