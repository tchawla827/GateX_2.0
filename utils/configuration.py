def load_yaml(path):
    """Load a YAML file and expand environment variables in string values."""
    import yaml
    import os

    def _expand(value):
        if isinstance(value, str):
            return os.path.expandvars(value)
        if isinstance(value, dict):
            return {k: _expand(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_expand(v) for v in value]
        return value

    with open(path, "r") as file:
        data = yaml.load(file, yaml.SafeLoader)
    return _expand(data)
