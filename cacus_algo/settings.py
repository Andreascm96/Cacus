import sys
import os
import site

BASE_DIR = os.path.join( os.path.dirname( __file__ ), '..' )

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Time to sleep between querying Yahoo for new data (seconds).
HEARTBEAT = 1

# Stop loss percentage
STOP_LOSS = 3

# Take home profits
TAKEHOME_PROFITS = 9