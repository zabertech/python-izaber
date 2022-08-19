from izaber import config, app_config, autoloader
from izaber.startup import request_initialize, initializer

autoloader.add_prefix('izaber.wamp')

CHECKS = {}

@initializer('submodule')
def load_config(**kwargs):
    request_initialize('config',**kwargs)

    CHECKS['loaded'] = True




