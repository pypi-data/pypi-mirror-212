"""
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

import json
from typing import Any
# import numpy as np
from glob import glob
from os import path, environ, getcwd


# Use tomllib or tomli
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib



class dotdict(dict):
    """
    A dictionary supporting dot notation.
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = dotdict(v)

    def lookup(self, dotkey):
        """
        Lookup value in a nested structure with a single key, e.g. "a.b.c"
        """
        path = list(reversed(dotkey.split(".")))
        v = self
        try:
            while path:
                key = path.pop()
                if isinstance(v, dict):
                    v = v[key]
                elif isinstance(v, list):
                    v = v[int(key)]
                else:
                    raise KeyError(key)
                
        except Exception as e:
            raise KeyError(f"{dotkey} does not exist!")
            
        return v

def flatten(container):
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


class Config:
    data = {}

    def __init__(self, config_path=None) -> None:
        # set config path
        if config_path:
            # ensure we pick the directory
            if path.isfile(config_path):
                config_path = path.dirname(config_path)
                
            self.config_path = config_path
            
        else:
            
            self.config_path = path.join(getcwd(), "config")

        if not path.exists(self.config_path):
            raise Exception(f"The config path {self.config_path} does not exist!")

        # set environment
        self.env = environ["ENV"] if "ENV" in environ else "development"
        
        # load config
        self.__load_configs()

    def __load_configs(self):
        # load env config
        env_config_paths = [
            path.join(self.config_path, "default" + ".*"),
            path.join(self.config_path, self.env + ".*"),
        ]

        env_files = list(map(lambda p: glob(p), env_config_paths))
        # flatten
        env_files = list(flatten(env_files))
        
        self.data = {}

        for file in env_files:
            with open(file, "rb") as f:
                data = tomllib.load(f)

                # merge data
                self.data = {**self.data, **data}

        self.data = dotdict(self.data)

    def __str__(self) -> str:
        return json.dumps(self.data, indent=4)

    def __call__(self) -> Any:
        return self

    def get(self, key):
        return self.data.lookup(key)
