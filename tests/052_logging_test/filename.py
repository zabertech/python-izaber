#!/usr/bin/env python

import logging

from izaber import config, initialize
from izaber.log import log
import tempfile

root = logging.getLogger()
target_log = tempfile.NamedTemporaryFile(delete=False, suffix=".test")

initialize(
        config={
            'config_filename': 'data/izaber.yaml',
        },
        logging = {
            'filename': target_log.name,
        },
    )

log.warning("IZABER_DATA")

print(f"TARGET={target_log.name}")
print(root.handlers)
