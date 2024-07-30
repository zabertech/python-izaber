import sys

app_config = {}
dependancies = {}

initializer_lookup = {}
initialization_rack = {}

def initializer(key,before=[]):
    def rack(key,f):
        initialization_rack[key] = f
        initializer_lookup[key] = f
        if before:
            for b in before:
                dependancies.setdefault(b,[])
                dependancies[b].append(key)
        return f

    return lambda f: rack(key,f)

def initialize(name=None, **kwargs):
    """ Invokes the initialization code for all the izaber.* modules
        that are hanging off of the system.
    """
    if name is None:
        name = sys.argv[0] or ''
    kwargs['name'] = name
    app_config.update(kwargs)

    # Reset load sequence if required
    if kwargs.get('force'):
        initialization_rack.update(initializer_lookup)

    # Go through load sequence handling dependancies as we go
    for key, func in dict(initializer_lookup).items():
        # If the initialization rack doesn't have the key, it means
        # we've already visited the initializer
        if not initialization_rack[key]:
            continue

        # Let's now ensure all the deps of this module are handled
        # (They need to be initialized before we can invoke this one)
        if key in dependancies:
            for b in dependancies.get(key,[]):
                result = request_initialize(b, **kwargs)
                if result:
                    kwargs = result

        # Was getting a weird error with flask where kwargs become None
        if not kwargs: kwargs = {}
        kwargs = request_initialize(key, **kwargs)
        initialization_rack[key] = None

    # Some of these steps are a bit hacky, accessing private variables
    #  in ways they may not expected, but there isn't a better way without
    #  intervention in multiple repositories
    if kwargs.get('log_usage_to_file'):
        import socket
        import inspect
        import datetime
        from pathlib import Path
        import socket

        # Get orignal call frame and filename
        stack = inspect.stack()
        orig_frame = stack[-1]
        orig_frame_file = Path(orig_frame.filename)

        try:
            # Get IP of machine, the connect address doesn't matter
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.255.255.255", 80))
            ip_addr = s.getsockname()[0]
            s.close()
        except:
            ip_addr = 'could not resolve'

        try:
            wamp_user = ''
            zerp_database = ''

            #It's okay to import here because it's already been initialized
            from .zconfig import config
            config_env = config._env
            config_dict = config._cfg_merged

            if 'wamp' in initializer_lookup:
                wamp_user = config_dict.get('wamp', {}).get('connection', {}).get('username', '')

            if 'wamp_zerp' in initializer_lookup:
                zerp_database = config_dict.get('wamp', {}).get('zerp', {}).get('database', '')

            logfile = Path(f'{orig_frame_file}.log')
            logfile_exists = logfile.exists()
            with open(logfile, 'a') as f:
                if not logfile_exists:
                    f.write('time, izaber environment, wamp_user, zerp_database, host, ip address, platform, python_version\n')
                f.write('{}, {}, {}, {}, {}, {}, {}, {}\n'.format(
                    datetime.datetime.now(),
                    config_env,
                    wamp_user,
                    zerp_database,
                    socket.gethostname(),
                    ip_addr,
                    sys.platform,
                    sys.version.split(' ')[0]
                ))
        except Exception as e:
            print(f"Something went wrong when trying to log usage to file. Error given: {e}")

def request_initialize(key, **kwargs):
    """ Force the initialization of another module tagged via `key`
    """

    # If the initialization rack doesn't have the key, it means
    # we've already visited the initializer
    if not initialization_rack[key]:
        return

    # Then invoke the initializer and log that we've completed
    replace_kwargs = initializer_lookup[key](**kwargs)
    initialization_rack[key] = None

    if replace_kwargs: return replace_kwargs
    return kwargs
