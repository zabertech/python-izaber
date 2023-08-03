#!/usr/bin/python

from izaber import config, initialize

def test_config():

    # Load without any arguments. This was throwing an error previously
    initialize()

if __name__ == "__main__":
    test_config()
