# coding: UTF-8
from xml.etree.ElementTree import *
tree = parse("sample.xml") # 返値はElementTree型
elem = tree.getroot() # ルート要素を取得(Element型)

# 要素のタグを取得
print elem.tag
# attributeの取得
"""print elem.get("xmi.id")
# デフォルトを指定してattributeを取得
print elem.get("height", "1200")
# attribute名のリスト取得
print elem.keys()
# (attribute, value)形式タプルのリスト取得
print elem.items()"""
