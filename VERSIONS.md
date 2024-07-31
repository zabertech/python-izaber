# Versions

## 2.20210919

Update `pyproject.toml` to be a bit more strict about what python versions are being used:

- `python`: 2.7, then 3.6 and up
- `pyYAML`: >5.4
- `pytz`: >2021.1
- `Jinja2`: >2.11.3

## 2.20210111

1. Instead of searching for `izaber.yaml` in the following order:
    1. `appdirs.user_data_dir(_app_name, _app_author)`
    2. `os.path.expanduser('~')`
    3. `'.'`

    Reverse the order:

    1. `'.'`
    2. `os.path.expanduser('~')`
    3. `appdirs.user_data_dir(_app_name, _app_author)`

    In other words, search the local directory for the `izaber.yaml` first.
2. Added missing dependancies:
    - `lxml`
    - `bs4` (Beautiful Soup used by the `izaber.email`)
3. Migrated to using poetry for releases
4. Created Docker based container for testing

## 3.20211119

1. Removed python 2.7 support
2. No longer require argument to `initialize()`. This does mean at some point overlays will be required (no one used them anyways so it will not be missed)


## 3.20211119-2

1. Version of PyYAML set was unnecessarily high

## 3.20211119-3

1. Sigh. Was using `sys.args` rather than `sys.argv`

## 3.20220303

1. Add dot-notation support to zconfig.get

## 3.20220815

1. Move to using nox based testing framework
2. Update module loader in `izaber/__init__.py` to use importlib (current) vs imp (deprecated)
3. Improve Dockerfile
4. Add Python 3.11 to tests
5. Explicitly test magic submodule loading

## 3.20220819

1. Fix issues when `import a_b` and `import a.b` were being used

## 3.0.20220823

1. Fix issues when `import a_b` is called before `import a.b`

## 3.0.20220929

1. For some reason the noxfile tests were not breaking when doing an `import izaber` on Python 3.11. When invoked manually we see:

    ```python
    Python 3.11.0rc1 (main, Aug  8 2022, 18:31:54) [GCC 9.4.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import izaber
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/src/izaber/__init__.py", line 40, in <module>
        class IZaberFinderImportlib(importlib.abc.MetaPathFinder):
                                    ^^^^^^^^^^^^^
    AttributeError: module 'importlib' has no attribute 'abc'. Did you mean: '_abc'?
    ```

    Tweaked to fix.

## 3.0.20221124

1. When an `izaber.*` module was being imported, if the module did not exist, the error was vague and non-useful. Amend to
    to throw a `ModuleNotFoundError` that would allow the developer/user to identify what the issue might be

    ```python
    (izaber-py3.8) root@7ed4086c1bd9:/src/tests# python 300_import_test.py
    Traceback (most recent call last):
      File "300_import_test.py", line 43, in <module>
        test_submodule()
      File "300_import_test.py", line 36, in test_submodule
        import izaber.nonexistant
      File "<frozen importlib._bootstrap>", line 991, in _find_and_load
      File "<frozen importlib._bootstrap>", line 975, in _find_and_load_unlocked
      File "<frozen importlib._bootstrap>", line 655, in _load_unlocked
      File "<frozen importlib._bootstrap>", line 618, in _load_backward_compatible
      File "/src/izaber/__init__.py", line 28, in load_module
        if self.spec.name in sys.modules:
    AttributeError: 'NoneType' object has no attribute 'name'
    ```

## 3.0.20230207

1. Noted by @chead in [Bug 11](https://github.com/zabertech/python-izaber/issues/11). `PyYAML` v6.0 requires `yaml.load` to have a second argument. Switched to using `safe_load` to fix the argument issue as well as a potential security issue.

## 3.1.20230803

1. Made it so that logging module does not automatically create a `log.log` file
    - Providing a path to `env.logging.filename` will log to that file
    - If `env.logging` is present but no `filename` key, it will opt to send the data to stdout
    - If no `env.logging` structure is present, it will simply not create the izaber log handler
    - If `env.logging.disable_internal` is a true value, it will also simply not create the izaber log handler
2. Added support for python 3.12 by tweaking the izaber module loader
3. Cleanup docker image to not use root and ubuntu user instead

## 3.1.20230817

1. `python-xdist` should not be in dependancies (it is only for dev) as noted by @Hawk777

## 3.1.20230928

1. We don't anticipate any issues with PyYAML so let's loosen things up till the next major release

## 3.2.20231029

1. Added ENV support for `izaber.yaml` which may be useful in Docker deployments
  - Setting the `IZABER_YAML` ENV value to the same value as a normal `izaber.yaml`, it will be used instead if the file doesn't exist
  - Setting the `IZABER_ENVIRONMENT` ENV value will be used if no explicit environment has been defined for `initialize` (using `initialize`'s `environment` argument will take precedence over `IZABER_ENVIRONMENT`)

## 3.2.20240731

1. Added support for keyword argument `log_usage_to_file` in initialize function which will log system and config information to file
