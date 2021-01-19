# Versions

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

