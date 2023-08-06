import argparse
import importlib.util
import json
import os
from yacs.config import CfgNode


def arg_parse():
    parser = argparse.ArgumentParser(description="Sync Config")
    parser.add_argument(
        "--desc", required=True, help="path to description.json", type=str
    )
    parser.add_argument("--config", required=True, help="path to config.py", type=str)
    parser.add_argument("--cfg_instance", required=True, help="instance name in config.py", type=str)
    parser.add_argument(
        "--adapter", required=True, help="path to ConfigAdapter.py", type=str
    )
    parser.add_argument("--adapter_instance", default="AdaptedConfig", type=str)
    args = parser.parse_args()
    return args


def load_config(config_path):
    # Import the config module
    try:
        spec = importlib.util.spec_from_file_location("config", config_path)
        if spec is not None:
            config = importlib.util.module_from_spec(spec)
            loader = getattr(spec, "loader", None)
            if loader is not None:
                loader.exec_module(config)
            else:
                raise ImportError(f"Could not load module from {config_path}")
        else:
            raise ImportError(f"Could not load module from {config_path}")

        return config.C  # assuming C is the name of the CfgNode object in config.py
    except ImportError:
        print(f"Error: Could not import config from {config_path}")
        return None


def get_relative_import_path(config_path):
    """
    Function to get the relative import path of a given module from the current working directory.

    Args:
        config_path (str): The absolute path of the module.

    Returns:
        str: The relative import path of the module.
    """

    # Get absolute path of the current working directory
    current_dir = os.path.abspath(os.getcwd())
    relative_path = current_dir

    # Get module path from config_path
    module_path = os.path.splitext(config_path)[0]  # remove '.py' at the end

    # Make sure both paths use the same slashes
    current_dir = current_dir.replace('\\', '/')
    module_path = module_path.replace('\\', '/')

    # Make sure the paths end with a slash
    if not current_dir.endswith('/'):
        current_dir += '/'

    # Get relative path
    if module_path.startswith(current_dir):
        relative_path = module_path[len(current_dir):]

    # Replace slashes with dots
    relative_path = relative_path.replace('/', '.')
    
    return relative_path

        
def write_adapter(config, adapter_path, config_path, descriptions, args):
    # Start writing the ConfigAdapter.py file
    with open(adapter_path, "w") as f:
        relative_path = get_relative_import_path(config_path)
        f.write(f"from {relative_path} import {args.cfg_instance}\n\n")
        f.write("class ConfigAdapter:\n")

        # For each class in the config
        for class_name in config.keys():
            f.write(f"    class {class_name}:\n")
            f.write(f"        def __init__(self, {args.cfg_instance}):\n")

            # For each attribute in the class
            for attr_name in config[class_name].keys():
                # Write the attribute to the file
                desc = descriptions.get(class_name, {}).get(attr_name.lower(), "")
                f.write(f"            # {desc}\n")
                f.write(f"            self.{attr_name} = {args.cfg_instance}.{class_name}.{attr_name}\n")

            # Close off the inner class definition
            f.write("\n")

        # Write the outer class's __init__ method
        f.write("\n    def __init__(self, C):\n")
        for class_name in config.keys():
            f.write(f"        self.{class_name.lower()} = self.{class_name}({args.cfg_instance})\n")
        f.write("        self.frozen = False\n")

        # Write the freeze method
        f.write("\n    def freeze(self):\n")
        f.write("        self.frozen = True\n")

        # Write the __setattr__ method
        f.write("\n    def __setattr__(self, name, value):\n")
        f.write("        if hasattr(self, name) and self.frozen:\n")
        f.write("            raise TypeError(f\"Can't modify attribute {name}\")\n")
        f.write("        else:\n")
        f.write("            super().__setattr__(name, value)\n")

        # Write the reload method
        f.write("\n    def reload(self, cfg):\n")
        f.write("        if self.frozen:\n")
        f.write("            raise TypeError(f\"Can't reload a frozen object\")\n")
        f.write("        else:\n")
        f.write(f"            {args.cfg_instance}.merge_from_file(cfg)\n")
        f.write(f"            self.__init__({args.cfg_instance})\n")
        f.write(f"            {args.cfg_instance}.freeze()\n")
        f.write("            self.freeze()\n")

        f.write(f"\n{args.adapter_instance} = ConfigAdapter({args.cfg_instance})\n")


def main():
    args = arg_parse()
    config_path = os.path.abspath(args.config)
    adapter_path = os.path.abspath(args.adapter)
    desc_path = os.path.abspath(args.desc)

    # Load the json descriptions
    with open(desc_path, "r") as f:
        descriptions = json.load(f)
    config = load_config(config_path)
    write_adapter(config, adapter_path, config_path, descriptions, args)


if __name__ == "__main__":
    main()
