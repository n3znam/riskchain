import json
import os

def load_abuse_lists(list_path='abuse_list.txt', tags_path='abuse_tags.json'):
    abuse_set = set()
    abuse_tags = {}

    if os.path.exists(list_path):
        with open(list_path, 'r') as f:
            abuse_set = set(line.strip() for line in f if line.strip())

    if os.path.exists(tags_path):
        with open(tags_path, 'r') as f:
            abuse_tags = json.load(f)

    return abuse_set, abuse_tags

def check_abuse(address, abuse_set, abuse_tags):
    result = {
        "is_abusive": False,
        "tag": None,
        "score": 0
    }

    if address in abuse_set:
        result["is_abusive"] = True
        result["score"] += 3  # base severity

    if address in abuse_tags:
        result["is_abusive"] = True
        result["tag"] = abuse_tags[address]
        result["score"] += 2  # additional severity for specific reason

    return result
