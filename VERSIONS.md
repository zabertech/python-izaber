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
