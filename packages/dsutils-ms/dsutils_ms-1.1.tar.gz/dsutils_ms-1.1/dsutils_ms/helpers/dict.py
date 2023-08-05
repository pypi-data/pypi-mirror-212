def flatten_dict(dictionary, parent_key="", flattened_dict=None):
    if flattened_dict is None:
        flattened_dict = {}

    for key, value in dictionary.items():
        new_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict):
            flatten_dict(value, new_key, flattened_dict)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                item_key = f"{new_key}[{i}]"
                if isinstance(item, (dict, list)):
                    flatten_dict({str(i): item}, item_key, flattened_dict)
                else:
                    flattened_dict[item_key] = item
        else:
            flattened_dict[new_key] = value

    return flattened_dict
