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

def change_starting_point_dict(state_parts):
    starting_point = []
    transaction_count = len(state_parts['UML:StateVertex.outgoing']['UML:Transition'])
    if transaction_count == 1:
        xml = state_parts['UML:StateVertex.outgoing']['UML:Transition']['@xmi.idref']
        starting_point.append({ 'xmi': xml })
    else:
        for state_part in state_parts['UML:StateVertex.outgoing']['UML:Transition']:
            starting_point.append({ 'xmi': state_part['@xmi.idref'] })
    return starting_point

def change_destination_dict(state_parts):
    destination = []
    transaction_count = len(state_parts['UML:StateVertex.incoming']['UML:Transition'])
    if transaction_count == 1:
        xml = state_parts['UML:StateVertex.incoming']['UML:Transition']['@xmi.idref']
        destination.append({ 'xmi': xml })
    else:
        for state_part in state_parts['UML:StateVertex.incoming']['UML:Transition']:
            destination.append({ 'xmi': state_part['@xmi.idref'] })
    return destination

def extraction_action_state(data_lists):
    # フロー図のstateのみ抽出
    for state_parts in data_lists['UML:Pseudostate']:
        if 'UML:StateVertex.outgoing' in state_parts:
            result_outgoing = change_starting_point_dict(state_parts)
        else:
            result_outgoing = [{ 'xmi': '' }]
        if 'UML:StateVertex.incoming' in state_parts:
            result_incoming = change_destination_dict(state_parts)
        else:
            result_incoming = [{ 'xmi': '' }]
        name = urllib.parse.unquote(state_parts['@name'])
        state_part = { 'from': result_outgoing, 'to': result_incoming , 'name': name }
        # ここ変えるかも appendじゃないほうがよい
        state_lists.append(state_part)

    for action_parts in data_lists['UML:ActionState']:
        if 'UML:StateVertex.outgoing' in state_parts:
            result_outgoing = change_starting_point_dict(state_parts)
        else:
            result_outgoing = [{ 'xmi': '' }]
        if 'UML:StateVertex.incoming' in state_parts:
            result_incoming = change_destination_dict(state_parts)
        else:
            result_incoming = [{ 'xmi': '' }]
        name = urllib.parse.unquote(action_parts['@name'])
        state_part = { 'from': result_outgoing, 'to': result_incoming , 'name': name }
        state_lists.append(state_part)

    last_parts = data_lists['UML:FinalState']
    if 'UML:StateVertex.incoming' in last_parts:
        result_incoming = change_destination_dict(last_parts)
    else:
        result_incoming = [{ 'xmi': '' }]
    name = urllib.parse.unquote(data_lists['UML:FinalState']['@name'])
    state_part = { 'from': { 'xmi': '' }, 'to': result_incoming , 'name': name }
    state_lists.insert(-1, state_part)

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
