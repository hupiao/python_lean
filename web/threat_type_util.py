# -*-coding: utf-8 -*-

import re
import json
import logging
import operator
from xml.dom.minidom import parse

logger = logging.getLogger(__name__)


def parse_xml():
    attack_type = {}
    sub_attack_type = {}

    try:
        doc = parse('./sandbox_type.xml')
        doc = doc.getElementsByTagName("attack_types")[0]
        for node in doc.getElementsByTagName("attack_type"):
            id_str = node.getAttribute("id")
            name_str = node.getAttribute("name")
            sub_attack_type[id_str] = name_str
            for n in node.getElementsByTagName("sub_attack_type"):
                sub_id_str = n.getAttribute("id")
                sub_name_str = n.getAttribute("name")
                if not sub_id_str:
                    continue
                attack_type[sub_id_str] = sub_name_str
    except Exception as e:
        logger.exception(e)
    return sub_attack_type, attack_type


def build_rule_map_v1():
    sub_attack_type, attack_type = parse_xml()
    load_dict = {}
    sub_type_priority = []
    try:
        with open('./sandbox_type.json', 'r') as f:
            load_dict = json.loads(f.read())
        for k, v in load_dict.items():
            # print(load_dict)
            # load_dict[k] = (sub_attack_type.get(v['sub_type'], u"其他恶意软件"), attack_type.get(v['type'], u"其他"))
            sub_type = sub_attack_type.get(v['sub_type'], u"其他恶意软件")
            ttype = attack_type.get(v['type'], u"其他")
            load_dict[k] = {"sub_type": sub_type, "ttype": ttype}
            if "priority" in v.keys():
                load_dict[k].update({
                    "priority": "" if not v['priority'] else v['priority']
                })
                sub_type_priority.append({"sub_type": sub_type,
                                          "priority": "" if not v['priority'] else v['priority']})
            # else:
            #     load_dict[k].update({
            #         "priority": "000"
            #     })
            #     sub_type_priority.append({"sub_type": sub_type,
            #                               "priority": "000"})
        try:
            print(load_dict.items())
            load_dict = sorted(load_dict.items(), key=lambda x: x[1]['priority'])
        except Exception as e:  # noqa
            load_dict = sorted(load_dict.items(), key=lambda x: str(x[1]))

        sub_type_priority = sorted(sub_type_priority, key=operator.itemgetter('priority'))

    except Exception as e:
        logger.exception(e)

    return load_dict, {}, sub_type_priority


static_rule_map, dynamic_rule_map, sub_type_priority = build_rule_map_v1()


def sorted_threat_type(threat_type_list):
    if not threat_type_list:
        return []

    if not sub_type_priority:
        return [threat_type_list[0]]

    try:
        for data in sub_type_priority:
            if data['sub_type'] in threat_type_list:
                return [data['sub_type']]
    except Exception as e:
        logger.exception(e)

    return [threat_type_list[0]]


def match_virus_type(virus):

    def _compile(s):
        s = s.replace(".", "\.").replace("*", ".*")
        if "/" not in s:
            return re.compile(s.lower())
        s = "(" + s.replace("/", "|") + ")"
        return re.compile(s.lower())

    for rule in static_rule_map:
        r = _compile(rule[0])
        if r.search(virus.lower()):
            return rule[1]['sub_type']
    return ''


def convert_threat_type(static_report):
    # static_report: dict instance
    result = []
    for k, v in static_report.items():
        if k == "sign_info":  # 签名信息不检测
            continue
        if k == "ioc_info":
            continue
        if k == 'webshell_info':
            continue
        if k == 'yara_info':
            continue

        for virus in v:
            threat_type = match_virus_type(virus)
            result.append({
                'name': virus,
                'threat_type': threat_type
            })
    return result
