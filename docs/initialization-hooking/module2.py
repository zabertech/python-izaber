from module1 import MYGLOBALVAR


from izaber.startup import request_initialize, initializer

# This decorator puts this function into the izaber library 
# initialiation system
@initializer('module2') # This gives a name to this module
def my_initialize(**kwargs):

    # We wish to ensure module1 has been initialized before
    # module 2
    request_initialize('module1',**kwargs)

    print("Module 2 about to initialize")
    print(f"Found {len(MYGLOBALVAR.items())} items in module1")
    print("Module 2 initialization complete!")


