import time
import sys

import logging

log = logging.getLogger(__name__)

print("now = %f" % (time.time()))
print("args = %s" % (sys.argv))

log.info("now = %f", time.time())
log.info("args = %s", sys.argv)
