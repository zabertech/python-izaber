# Initialization Hooking

When developing modules, it will often require an initialization function, especially if singletons are involved:

- Connections to WAMP
- Connections to databases to pull information
- Loading configuration data

The `iZaber` library offers a fairly straightforward way to manage initializations in a way that not only calls a module's initialization function but also respects dependancies and add some syntax sugar for users.

## Example:

In this example, there are 3 files:

- `main.py` which loads the modules with initialiations
- `module1.py` a module that has a custom initialization holding a global dict a singleton
- `module2.py` a module that relies upon module1 for data

...
