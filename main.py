import sys
from AutoInstagram.AutoInastagram import AutoInastagram


def help():
   pass


if len(sys.argv) == 1:
   pass # TODO usage ...
elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
   help()
elif sys.argv[1] == '--version':
   pass # TODO print Version ...
else:
   ai = AutoInastagram(sys.argv[1:])
   ai.start()
