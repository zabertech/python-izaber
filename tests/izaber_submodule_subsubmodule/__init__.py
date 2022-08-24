from izaber import config, app_config, autoloader
from izaber.startup import request_initialize, initializer

autoloader.add_prefix('izaber.wamp')

CHECKS = {
  'executed': 0
}

class TestObject(dict):
    def poke(self, val):
        self['a'] = val

DATA = TestObject()

@initializer('subsubmodule')
def load_config(**kwargs):
    request_initialize('config',**kwargs)

    CHECKS['loaded'] = True
    CHECKS['executed'] += 1




