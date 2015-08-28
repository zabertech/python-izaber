# Adds support for various templates
import jinja2
import datetime

from izaber.startup import initializer, request_initialize, app_config
from izaber.paths import paths
from izaber import config

compiled_templates = {}

template_loader = jinja2.FileSystemLoader(searchpath=[".","/"])
template_env = jinja2.Environment(loader=template_loader)

def parse(template,**tags):
    template_fpath = paths.full_fpath(template)
    now = datetime.datetime.now()
    tags.update({
        'now': now,
        'date': now.strftime('%Y-%m-%d'),
        'date_iso': now.isoformat(),
        'time': now.strftime('%H:%M:%S'),
        'dt': now.strftime('%Y-%m-%d_%H-%M-%S'),
        'config': config,
    })
    if template_fpath not in compiled_templates:
        compiled_templates[template_fpath] = \
            template_env.get_template(template_fpath)
    return compiled_templates[template_fpath].render(**tags)

@initializer('templates')
def initialize(**kwargs):
    request_initialize('config',**kwargs)

if __name__ == '__main__':

    test_config = {
        'paths': {
          'path': '/tmp',
          'log_path': '/tmp/log'
        },
        'log': {
          'filename': '{{log_path}}/app.log',
          'custom': {
            'filename': '{{log_path}}/custom.log'
          }
        }
    }

    import izaber.startup
    izaber.startup.initialize(**test_config)



