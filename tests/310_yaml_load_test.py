"""
Test for: https://github.com/zabertech/python-izaber/issues/11

> In PyYAML 6, [the `pyyaml.load` function started requiring a second parameter](https://github.com/yaml/pyyaml/pull/561). `zconfig.YAMLConfig.load_config` calls that function if the `config_buffer` parameter is passed, and does not provide one, thus failing with PyYAML 6.

We will test this by creating an instance where this fails

There are two places in zconfig.py where we use the `load()` function:

1. In `load` config:

```python
        if config_buffer:
            self._config_full_filname = None
            self._cfg = yaml.load(config_buffer)
        else:
            self.config_fpath = self.config_find() \
                                          or os.path.join(self._config_dirs[0], \
                                             self._config_filename)
```

2. in `config_update_`:

```python
        if not isinstance(config_amend,dict):
            config_amend = yaml.load(config_amend)
```

We're going to replace the yaml.load with yaml.safe_load

"""

import izaber.zconfig

TEST_CONFIG = """
default:
   hello: "world"
"""

TEST_CONFIG_AMENDMENT = """
default:
   hi: "there"
"""

def test_load():

    # Test case 1.
    config = izaber.zconfig.YAMLConfig(
        config_buffer=TEST_CONFIG
    )
    assert config.hello == "world"

    # Test case 2. config_update_
    # Maybe we should get rid of this as it's only used in zaber-config
    config.config_update_(TEST_CONFIG_AMENDMENT)
    assert config.hi == "there"

if __name__ == "__main__":
    test_load()




