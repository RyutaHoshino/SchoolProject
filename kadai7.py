from xml.etree import ElementTree

# XML 文字列をパースして Element オブジェクトを生成
elem = ElementTree.fromstring('<tree name="hello"><trunk>...</trunk></tree>')
print(elem.tag)     #=> tree
print(elem.attrib)  #=> {'name': 'hello'}
