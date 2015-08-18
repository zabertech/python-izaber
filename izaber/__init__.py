import sys
import re
import imp

from izaber.startup import initialize, app_config
from izaber.zconfig import config

class IZaberFinder(object):

    def find_module(self, module_name, package_path=None):
        elements = module_name.split('.')
        if elements[0] != 'izaber':
            return

        # Extension modules are expected to be named:
        #
        # izaber_extensionname
        #
        # where extensionname is all alphabetical 
        try:
            elements[1] = "izaber_"+elements[1]
            found = None
            package_path = None
            for e in elements[1:]:
                found = imp.find_module(e,package_path)
                package_path = [found[1]]

            return IZaberLoader(*found)
        except ImportError:
            return

class IZaberLoader(object):

    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs

    def load_module(self, module_name):
        return imp.load_module(module_name, *self.args,**self.kwargs)

sys.meta_path.append(IZaberFinder())

