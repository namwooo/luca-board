import json
import re

from flask import jsonify


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name):
    return re.sub('_([a-zA-Z0-9])', lambda m: m.group(1).upper(), name)


def change_dict_naming_convention(d, convert_function):
    """
    Convert a nested dictionary from one convention to another.
    Args:
        d (dict): dictionary (nested or not) to be converted.
        convert_function (func): function that takes the string in one convention and returns it in the other one.
    Returns:
        Dictionary with the new keys.
    """
    new = {}
    for k, v in d.items():
        new_v = v
        if isinstance(v, dict):
            new_v = change_dict_naming_convention(v, convert_function)
        elif isinstance(v, list):
            new_v = list()
            for x in v:
                new_v.append(change_dict_naming_convention(x, convert_function))
        new[convert_function(k)] = new_v
    return new


def convert_dump(obj, schema):
    result = schema.dump(obj)
    if isinstance(result.data, list):
        converted_obj = []
        for item in result.data:
            converted_obj.append(change_dict_naming_convention(item, snake_to_camel))
        return jsonify(converted_obj)
    if isinstance(result.data, dict):
        result = change_dict_naming_convention(result.data, snake_to_camel)
    return jsonify(result)
