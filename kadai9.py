#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmltodict
import urllib.parse
flow_list = []
# debugの方法
def extraction_flow(data_list):
    # 先頭！
    first_point = urllib.parse.unquote(data_list['UML:Pseudostate']['@name'])
    flow_list.insert(0, first_point)
    # 真ん中 for 文で回すか
    for s in data_list['UML:ActionState']:
        middle_point = urllib.parse.unquote(s['@name'])
        flow_list.append(middle_point)
    # 最後
    end_point = urllib.parse.unquote(data_list['UML:FinalState']['@name'])
    flow_list.insert(-1, end_point)
    return flow_list

with open('./target_read.xml') as fd:
    doc = xmltodict.parse(fd.read())
    flow_chat_doc = doc['XMI']['XMI.content']['UML:Model']['UML:Namespace.ownedElement']
    data_flow = flow_chat_doc['UML:ActivityGraph']['UML:StateMachine.top']['UML:CompositeState']['UML:CompositeState.subvertex']
    # list.append(data_flow)
    list = extraction_flow(data_flow)

    # import pdb; pdb.set_trace()
# print(list)
# # 出力できた！
f = open('text.txt', 'w') # 書き込みモードで開く
str1 = '\n'.join(str(e) for e in list)
f.write(str1) # 引数の文字列をファイルに書き込む
f.close() # ファイルを閉じる
