from xml.etree import ElementTree

# XML ファイルから ElementTree オブジェクトを生成
tree = ElementTree.parse('books.xml')

# 先頭要素を表す Element オブジェクトを取得
elem = tree.getroot()
print(elem.tag)     #=> tree
print(elem.attrib)  #=> {'name': 'hello'}
