# -*- coding: utf-8 -*-

from xml.etree import ElementTree

x = 'sample.xml'               # 読み込むxmlファイルのパスを変数に記憶させる
tree = ElementTree.parse(x)    # xmlファイルを読み込む
root = tree.getroot()          # ルートを取得する
"""
print root.tag                 # fruit
print root.findtext('item002') # orange
"""

str1='{'
str2='}'

f = open('sample.txt', 'w') # 書き込みモードで開く
f.write(str1) # 引数の文字列をファイルに書き込
f.write('\n')
f.write(str2)
f.close() # ファイルを閉じる
