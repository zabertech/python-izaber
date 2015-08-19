app_config = {}
initialization_rack = {}

def initializer(key):
    def rack(key,f):
        initialization_rack[key] = f
        return f

    return lambda f: rack(key,f)

def initialize(name,**kwargs):
    kwargs['name'] = name
    app_config.update(kwargs)
    for key, func in dict(initialization_rack).iteritems():
        if not initialization_rack[key]:
            continue
        func(**kwargs)
        initialization_rack[key] = None

def request_initialize(key,**kwargs):
    if not initialization_rack[key]:
        return
    initialization_rack[key](**kwargs)
    initialization_rack[key] = None
