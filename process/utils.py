from yaml import safe_load as yaml_load


def read_cfg(cfg_path: str) -> dict:
    """
    Load a YAML configuration file and return its contents as a dictionary.

    Args:
        cfg_path (str): The path to the YAML configuration file.

    Returns:
        dict: A dictionary representation of the YAML configuration.
    """
    with open(cfg_path, "r") as fid:
        cfg = yaml_load(fid)

    return cfg
