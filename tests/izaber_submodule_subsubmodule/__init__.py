from izaber import config, app_config, autoloader
from izaber.startup import request_initialize, initializer

autoloader.add_prefix('izaber.submodule.submodule')

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
    if kwargs['force']:
        CHECKS['executed'] = 0

    CHECKS['loaded'] = True
    CHECKS['executed'] += 1




