# YACS_Adapter

[YACS](https://github.com/rbgirshick/yacs) (Yet Another Configuration System) is an incredibly dynamic and lightweight library that provides a powerful tool for managing the configurations of machine learning experiments. However, due to its `__dict__` based type system, YACS introduces a minor flaw where IDEs such as Visual Studio Code cannot track the configuration variables.

The `YACS_Adapter` is designed to address this limitation by offering an adapter to YACS. It is a Python package designed to enhance the flexibility and readability of configuration management when working with machine learning experiments. The paradigm is: 

 `your code + a YACS config for experiment E (+ external dependencies + hardware + other nuisance terms ...) + YACS adapter (enhancing readability for readers and static variable trackability for developers) = reproducible experiment E` 

It leverages YACS's functionality while providing an interface that can be readily tracked by IDEs.

## Features
- Automatic generation of Python classes based on a YACS `CfgNode`.
- Inline descriptions for each configuration variable, improving readability.
- Immutable configuration classes after loading, preventing accidental modification.

## Getting Started

### Installation
```shell
pip install YACS_Adapter
```

### Usage

Before import `YACS_Adapter`to write codes, the `ConfigAdapter` class needs to be generated. 

`YACS_Adapter` works in two steps:

1. Generate the `ConfigAdapter` class: 

    The paths and variable names include:

    - `config_path`: Path to `config.py`.
    - `adapter_path`: Path to `description.json`.
    - `desc_path`: Path to `adapter.py`.
    - `cfg_instance`: The variable name of the cfg instance defined in `config.py`.
    - `adapter_instance`: The variable name of the adapter instance (default: `AdaptedConfig`) in `ConfigAdapter.py`.

    Then, run the `yacs_sync` in command line to generate the ConfigAdapter.py.
    
    ```shell
    # Remember to replace `sync_path`, `config_path`, `desc_path`, `adapter_path`, and `cfg_instance` with your actual paths and variable names.
    yacs_sync --config config_path --desc desc_path --adapter adapter_path --cfg_instance cfg_instance_var
    ```

2. Use the `ConfigAdapter` class in your code: After generating `ConfigAdapter.py`, you can import `AdaptedConfig(default name)` from `ConfigAdapter.py` in your Python scripts.

   ```python
   from ConfigAdapter import AdaptedConfig
   ```

   Use the reload() method in your code: The reload() method not only integrates the previous CfgNode merge and freeze operations but also introduces a freeze() method to AdaptedConfig. This prevents the modification of configuration variables after they've been loaded.

   ```python
   # cfg = get_cfg_defaults()
   # cfg.merge_from_file("experiment.yaml")
   # cfg.freeze()
   # -> (all integrated to AdaptedConfig.reload() function)
   AdaptedConfig.reload("experiment.yaml")
   ```