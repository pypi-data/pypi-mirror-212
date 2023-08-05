<!--
 Copyright (c) 2023 Anthony Mugendi
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# TOMFIG - Toml Config
The simplest TOML config manager for python!

This module borrows a little from [config](https://www.npmjs.com/package/config). The only argument needed during initialization is the `config_path`. 

```python
from tomfig import Config

# defaults to [cwd]/config
config = Config(config_path='/dir/with/config_files')

```

The module then loads configuration files and merges down the configs in the following order.

1. **`default.toml`**
2. **[environment_config].toml** where environment is whatever you pass to your script via the `ENV` environment variable. Default is **`development.toml`**

## Accessing Config Values
There are two ways of accessing config values.

Imagine we have the following config file:
```toml
[APP]
name="My App"

[TOOLS.language-support]
python=">3.8"

[SERVER.API]
domain="localhost:3000/default"
```

### 1. Direct/Data Access
You can access config values directly using dot notation via the `data` property as follows.

```python
config.data.APP.name 
# "My App"
```

However, this method is discouraged on production. This is because, if a key is missing, it returns `None` instead of throwing an error. 

That behaviour is however intentional as it allows us an eay way to check is a config value exists. For example:

```python
# Check if our app has a name
if not config.data.APP.name:
    # Use AI to generate and set APP name 
```

### 2. Safe/Get Access

This is the preferred method to access config values.  This method immediately throws if a certain value is missing.

```python
config.get("SERVER.API.domain")
# "localhost:3000/development"
```

Have a look at the tests for examples.

# Thoughts
I have not implemented a `.set()` method and don't plan to. It is my considered view that configs should be static and only changed in the config files to ensure code functions in a predictable, easy to debug manner.