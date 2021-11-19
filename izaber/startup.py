import sys

app_config = {}
dependancies = {}
initialization_rack = {}

def initializer(key,before=[]):
    def rack(key,f):
        initialization_rack[key] = f
        if before:
            for b in before:
                dependancies.setdefault(b,[])
                dependancies[b].append(key)
        return f

    return lambda f: rack(key,f)

def initialize(name=None,**kwargs):
    """ Invokes the initialization code for all the izaber.* modules
        that are hanging off of the system.
    """
    if name is None:
        name = sys.argv[0] or ''
    kwargs['name'] = name
    app_config.update(kwargs)
    for key, func in dict(initialization_rack).items():
        if not initialization_rack[key]:
            continue
        if key in dependancies:
            for b in dependancies.get(key,[]):
                result = request_initialize(b,**kwargs)
                if result:
                    kwargs = result

        # Was getting a weird error with flask where
        # kwargs become None
        if not kwargs: kwargs = {}
        kwargs = request_initialize(key,**kwargs)
        initialization_rack[key] = None

def request_initialize(key,**kwargs):
    """ Force the initialization of another module tagged via `key`
    """
    if not initialization_rack[key]:
        return
    result = initialization_rack[key](**kwargs)
    initialization_rack[key] = None
    if result: return result
    return kwargs
