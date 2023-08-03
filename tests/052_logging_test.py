#!/usr/bin/python

import pathlib
import re
import sys
import subprocess

def run(*args, **kwargs):
    if sys.version_info.major == 3 and sys.version_info.minor == 6:
        res = subprocess.check_output(*args, **kwargs)
        assert res
        return res.decode('utf-8')
    else:
        res = subprocess.run(*args, **kwargs, capture_output=True, text=True)
        assert res
        return res.stdout


def test_config():

    # Test the file output based logging
    buf = run([sys.executable, "052_logging_test/filename.py"])
    output = re.search(r"TARGET=(.*)", buf)
    assert output
    target_fpath = pathlib.Path(output.group(1))
    assert target_fpath.exists()
    buf = target_fpath.open('r').read()
    assert re.search('IZABER_DATA', buf)

    # Test the stream output based logging
    buf = run([sys.executable, "052_logging_test/stream.py"])
    assert re.search('IZABER_DATA', buf)

    # Test that we get nothing when logging has not been configured
    buf = run([sys.executable, "052_logging_test/none.py"])
    assert not re.search('IZABER_DATA', buf)

if __name__ == "__main__":
    test_config()

