from izaber import initialize

# Note that we import module2 before module1, however, due to 
# how the system allows initialization dependancies to be setup,
# module1's init will always be called before module2
import module2

from module1 import MYGLOBALVAR

# Now that all the initialization functions have been registered,
# this will initialize everything
initialize("example")

print("Initialization is done!")

# Let's see if we can use the global var
print(f"Found {len(MYGLOBALVAR.items())} items in module1")

