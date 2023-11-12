import yaml


def load_yaml(file_path: str) -> dict:
    """
    Load a YAML file and return its content as a dictionary.

    Parameters:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The content of the YAML file as a dictionary.
    """
    with open(file_path) as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


def extract_items_from_yaml(data: dict, key: str) -> dict:
    """
    Extracts items from a YAML dictionary based on a specified key.

    Args:
        data (dict): The YAML dictionary to extract items from.
        key (str): The key to use for extracting items from the dictionary.

    Returns:
        dict: A dictionary containing the extracted items, with the item names as keys and the item fields as values.
    """
    items = {}
    for item in data[key]:
        items[item['name']] = {}
        for field in item:
            if field != 'name':
                items[item['name']][field] = item[field]
    return items


def extract_and_load_yaml(file: str, key: str) -> dict:
    """
    Extracts items from a YAML file based on a given key and returns them as a dictionary.

    Args:
        file (str): The path to the YAML file.
        key (str): The key to extract items from.

    Returns:
        dict: A dictionary containing the extracted items.
    """
    return extract_items_from_yaml(load_yaml(file), key)
