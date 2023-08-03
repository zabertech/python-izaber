#!/usr/bin/env python

import logging

from izaber import config, initialize
from izaber.log import log
import tempfile
import sys

root = logging.getLogger()
target_log = tempfile.NamedTemporaryFile(delete=False, suffix=".test")

initialize(
        config={
            'config_filename': 'data/izaber.yaml',
        },
        logging = {
            'stream': sys.stdout
        },
    )

log.warning("IZABER_DATA")

