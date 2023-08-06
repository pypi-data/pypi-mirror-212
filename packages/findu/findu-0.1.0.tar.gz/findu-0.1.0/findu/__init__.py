""" Sherlock Module

This module contains the main logic to search for usernames at social
networks.

"""

import sys

# Check if the user is using the correct version of Python
python_version = sys.version.split()[0]

if sys.version_info < (3, 6):
    print("Sherlock requires Python 3.6+\nYou are using Python %s, which is not supported by Sherlock" % (python_version))
    sys.exit(1)


from .findu import *
# import findu
findu.main()

