import yaml

def load_config(filepath):
    """Load a YAML configuration file."""
    with open(filepath, 'r') as file:
        config = yaml.safe_load(file)
    return config