import sys

from commands.dos import Dos

dos = Dos(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
dos.run()
dos.write_details()

