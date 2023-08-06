from typing import Dict, List
import re


def dsaf_parse_node(part: str) -> Dict[str, any]:
    """
    keys : text, id, rcpNo, dcmNo, eleId, offset, length, dtd, tocNo
    {'text': '2. 계열회사 현황(상세)', 'id': '51', 'rcpNo': '20220318000989', 'dcmNo': '8479041', 'eleId': '51', 'offset': '863891', 'length': '3225', 'dtd': 'dart3.xsd', 'tocNo': '49'}
    :param part:
    :return:
    """
    matches = re.finditer(r"\['(.*)'\]\s*=\s*\"(.*)\";", part)
    data = {}
    for matchNum, match in enumerate(matches, start=1):
        groups = match.groups()
        if len(groups) < 2:
            continue
        data[groups[0]] = groups[1]
    return data

def dsaf_parse_nodes(html) -> List[Dict[str, any]]:
    regex = r"var node\d{1,2}[\s\S]*?cnt\+\+;"
    matches = re.finditer(regex, html)
    nodes = [dsaf_parse_node(match.group()) for match in matches]
    return nodes

