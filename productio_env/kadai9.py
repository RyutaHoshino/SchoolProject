#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Debug import pdb; pdb.set_trace()
import xmltodict
import urllib.parse

flow_figure_list = []
output_flow_figure_list = []
initialData =[]

def extraction_flow_figure(data_lists):
    # フロー図の必要な箇所のみ抽出します
    first_part = urllib.parse.unquote(data_lists['UML:Pseudostate']['@name'])
    flow_figure_list.insert(0, first_part)
    for action_state in data_lists['UML:ActionState']:
        middle_part = urllib.parse.unquote(action_state['@name'])
        flow_figure_list.append(middle_part)
    last_part = urllib.parse.unquote(data_lists['UML:FinalState']['@name'])
    flow_figure_list.insert(-1, last_part)
    return flow_figure_list

def string_to_python_code(string_lines):
    # pythonに対応していないため書き換える
    for string_line in string_lines:
        if string_line.find('開始') != -1:
            initialData = string_line.replace('開始', '')
        elif string_line.find('print') != -1:
            # ToDo 強引な置き換えなので直したい
            output_flow_figure_list.append(string_line.replace('+', '(')+ ')')
        elif string_line.find('int+') != -1:
            output_flow_figure_list.append(string_line.strip("int+") +"="+ initialData)
        elif string_line.find('++') != -1:
            output_flow_figure_list.append(string_line.replace('++', '+=1'))
        else:
            print("対応できません...")
    return output_flow_figure_list

with open('./target_read.xml') as fd:
    doc = xmltodict.parse(fd.read())
    uml_model_doc = doc['XMI']['XMI.content']['UML:Model']['UML:Namespace.ownedElement']
    data_flow_part = uml_model_doc['UML:ActivityGraph']['UML:StateMachine.top']['UML:CompositeState']['UML:CompositeState.subvertex']
    data_flow_part_list = extraction_flow_figure(data_flow_part)
    new_data_flow_part_list = string_to_python_code(data_flow_part_list)

# pythonファイルへの出力
f = open('text.py', 'w')
str1 = '\n'.join(str(e) for e in new_data_flow_part_list)
f.write(str1)
f.close()
