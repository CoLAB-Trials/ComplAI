import yaml

def load_config(filepath: str) -> dict:
    """
    Load a YAML configuration file.

    Args:
        filepath (str): The path to the YAML configuration file.

    Returns:
        dict: The configuration data loaded from the YAML file.
    """
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config