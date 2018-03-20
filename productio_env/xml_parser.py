#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Debug import pdb; pdb.set_trace()
import xmltodict
import urllib.parse
import sys

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
    state_lists = []
    for state_parts in data_lists['UML:Pseudostate']:
        if 'UML:StateVertex.outgoing' in state_parts:
            result_outgoing = change_starting_point_dict(state_parts)
        else:
            result_outgoing = []
        if 'UML:StateVertex.incoming' in state_parts:
            result_incoming = change_destination_dict(state_parts)
        else:
            result_incoming = []
        name = urllib.parse.unquote(state_parts['@name'])
        state_part = { 'from': result_outgoing, 'to': result_incoming , 'name': name }
        # ここ変えるかも appendじゃないほうがよい
        state_lists.append(state_part)

    for action_parts in data_lists['UML:ActionState']:
        if 'UML:StateVertex.outgoing' in action_parts:
            result_outgoing = change_starting_point_dict(action_parts)
        else:
            result_outgoing = []
        if 'UML:StateVertex.incoming' in action_parts:
            result_incoming = change_destination_dict(action_parts)
        else:
            result_incoming = []
        name = urllib.parse.unquote(action_parts['@name'])
        state_part = { 'from': result_outgoing, 'to': result_incoming , 'name': name }
        state_lists.append(state_part)

    last_parts = data_lists['UML:FinalState']
    if 'UML:StateVertex.incoming' in last_parts:
        result_incoming = change_destination_dict(last_parts)
    else:
        result_incoming = []
    name = urllib.parse.unquote(data_lists['UML:FinalState']['@name'])
    state_part = { 'from': [], 'to': result_incoming , 'name': name }
    state_lists.append(state_part)

    return state_lists

def extraction_data_flow(data_lists):
    # フローの遷移からguardのみ抽出します
    flow_lists = []
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

def merge_action_and_flow(actions, flow):
    sort_flow_list = []
    xmi_key = []
    list_length = len(actions)
    # スタートの処理
    sort_flow_list.append(actions[0]['name'])
    if len(actions[0]['from']) == 1:
        xml = actions[0]['from'][0]['xmi']
        xmi_key.append(actions[0]['from'][0]['xmi'])
        # 先頭のactionを消す
        actions.pop(0)
    else:
        # 使わない
        for from_key in actions[0]['from']:
            xmi_key.append(from_key['xmi'])
    for index, action in enumerate(actions):
        if action['to'][0]['xmi'] == ''.join(xmi_key):
            sort_flow_list.append(action['name'])
            xmi_key = [] # リセット作業
            xmi_key.append(action['from'][0]['xmi'])
            # popにするとまずいかも
            actions.pop(index)

    for index, action in enumerate(actions):
        if action['to'][0]['xmi'] == ''.join(xmi_key):
            sort_flow_list.append(action['name'])
            xmi_key = [] # リセット作業
            # keyが二つあるパターンを検討する
            if len(action['from']) > 1:
                for s in action['from']:
                    if s['xmi'] ==  flow[1]['xmi_id']:
                        sort_flow_list.append(flow[1]['guard'])
                    xmi_key.append(s['xmi'])
            else:
                xmi_key.append(action['from'][0]['xmi'])
            actions.pop(index)
    if len(xmi_key) != 1:
        local_xmi_key = xmi_key
        xmi_key = []
        for index, action in enumerate(actions):
            if action['to'][0]['xmi'] == ''.join(local_xmi_key[0]):
                sort_flow_list.append(action['name'])
                # ToDo flowの中身もいれる
                if len(action['from']) > 0:
                    for s in action['from']:
                        xmi_key.append(s['xmi'])
                        actions.pop(index)
                else:
                    if len(action['from']) > 0:
                        xmi_key.append(action['from'][0]['xmi'])
            if action['to'][0]['xmi'] == ''.join(local_xmi_key[1]):
                sort_flow_list.append(action['name'])
                if len(action['from']) > 0:
                    for s in action['from']:
                        xmi_key.append(s['xmi'])
                        actions.pop(index)
                else:
                    if len(action['from']) > 0:
                        xmi_key.append(action['from'][0]['xmi'])
            if  len(actions) == 1 and len(actions[0]['from']) == 0:
                sort_flow_list.append(actions[0]['name'])
                break
    # 繰り返してlenが０になるまでやるとかあり
    return sort_flow_list

def string_to_python_code(string_lines):
    # pythonに対応していないため書き換える
    output_flow_figure_list = []
    for string_line in string_lines:
        if string_line.find('input+') != -1:
            string_line = "x = int(input())"
            output_flow_figure_list.append(string_line)
        elif string_line.find('デシジョンノード') != -1:
            string_line = "if"
            output_flow_figure_list.append(string_line)
        elif string_line.find('+1') != -1:
            string_line = '    ' + string_line.replace('+1', ' += 1')
            output_flow_figure_list.append(string_line)
        elif string_line.find('>' or '<') != -1:
            output_flow_figure_list.append(string_line)
    return output_flow_figure_list
# target_readなら問題ない　クラスにしたいね。

xml_path = "./%s" % (sys.argv[1])
with open(xml_path) as fd:
    doc = xmltodict.parse(fd.read())
    uml_model_doc = doc['XMI']['XMI.content']['UML:Model']['UML:Namespace.ownedElement']['UML:ActivityGraph']
    action_part = uml_model_doc['UML:StateMachine.top']['UML:CompositeState']['UML:CompositeState.subvertex']
    flow_part =  uml_model_doc['UML:StateMachine.transitions']
    # 変換する
    action_part_list = extraction_action_state(action_part)
    flow_part_list = extraction_data_flow(flow_part)
    # 統合
    flow_result = merge_action_and_flow(action_part_list, flow_part_list)
    new_data_flow_part_list = string_to_python_code(flow_result)
    # print文だけ追加&if文の構築する
    for index, s in enumerate(new_data_flow_part_list):
        if s == 'if':
            judge = new_data_flow_part_list[index + 1]
            new_data_flow_part_list[index] = 'if '+ str(judge) + ":"
            new_data_flow_part_list.pop(index + 1)
    new_data_flow_part_list.append('print(x)')
# pythonファイルへの出力
f = open('result.py', 'w')
str1 = '\n'.join(str(e) for e in new_data_flow_part_list)
f.write(str1)
f.close()
