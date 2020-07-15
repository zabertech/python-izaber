import izaber
from izaber.startup import request_initialize, initializer

MYGLOBALVAR = {}

# This decorator puts this function into the izaber library 
# initialiation system
@initializer('module1') # This gives a name to this module
def my_initialize(**kwargs):
    print("Module 1 about to initialize")
    for i in range(1000):
        MYGLOBALVAR[i] = f"Hi! {i}"
    print("Module 1 initialization complete!")





