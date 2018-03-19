#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Debug import pdb; pdb.set_trace()
import xmltodict
import urllib.parse
import sys

state_lists = []
flow_lists = []
output_flow_figure_list = []
initialData =[]

def extraction_action_state(data_lists):
    # フロー図のstateのみ抽出します
    for state_parts in data_lists['UML:Pseudostate']:
        try:
            if state_parts['UML:StateVertex.outgoing']:
                from_xmi = state_parts['UML:StateVertex.outgoing']
                # ここが動かないので修正します！
                import pdb; pdb.set_trace()
            elif state_parts['UML:StateVertex.incoming']:
                to_xmi = state_parts['UML:StateVertex.incoming']
        except Exception as e:
            print(e)
        else:
            name = urllib.parse.unquote(state_parts['@name'])
        state_part = { 'root': { 'from_xmi': from_xmi }, 'name': name }
        state_lists.append(state_part)
    # 終点部分の処理
    last_part = urllib.parse.unquote(data_lists['UML:FinalState']['@name'])
    state_lists.insert(-1, last_part)
   # 中間部分の処理
    for action_parts in data_lists['UML:ActionState']:
        middle_part = urllib.parse.unquote(action_parts['@name'])
        state_lists.append(middle_part)

    return state_lists

def extraction_data_flow(data_lists):
    # フローの遷移からguardのみ抽出します
    for flow_parts in data_lists['UML:Transition']:
        try:
            if flow_parts['UML:Transition.guard']:
                gurad_part = urllib.parse.unquote(flow_parts['UML:Transition.guard']['UML:Guard']['@name'])
        except Exception as e:
            print(e)
        else:
            guard_info = { 'xmi_id': flow_parts['@xmi.id'], 'guard': gurad_part }
            flow_lists.append(guard_info)
    return flow_lists

def string_to_python_code(string_lines):
    # pythonに対応していないため書き換える
    for string_line in string_lines:
        if string_line.find('開始') != -1:
            # ここ不要です
            initialData = string_line.replace('開始', '')
        elif string_line.find('print') != -1:
            # ToDo 強引な置き換えなので直したい
            output_flow_figure_list.append(string_line.replace('+', '(')+ ')')
        elif string_line.find('int+') != -1:
            # 変数宣言はpythonに存在しないので、default値を置いちゃえ
            output_flow_figure_list.append(string_line.strip("int+") +"="+ initialData)
        elif string_line.find('++') != -1:
            output_flow_figure_list.append(string_line.replace('++', '+=1'))
        else:
            print("対応できません...")
    return output_flow_figure_list
# target_readなら問題ない　クラスにしたいね。

xml_path = "./%s" % (sys.argv[1])
with open(xml_path) as fd:
    doc = xmltodict.parse(fd.read())
    uml_model_doc = doc['XMI']['XMI.content']['UML:Model']['UML:Namespace.ownedElement']['UML:ActivityGraph']
    data_flow_part = uml_model_doc['UML:StateMachine.top']['UML:CompositeState']['UML:CompositeState.subvertex']
    data_transition =  uml_model_doc['UML:StateMachine.transitions']
    data_flow_part_list = extraction_action_state(data_flow_part)
    data_flow_list = extraction_data_flow(data_transition)
    new_data_flow_part_list = string_to_python_code(data_flow_part_list)
# pythonファイルへの出力
f = open('result.py', 'w')
str1 = '\n'.join(str(e) for e in new_data_flow_part_list)
f.write(str1)
f.close()
