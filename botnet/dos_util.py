import sys

from commands.dos import Dos

# Creates a DoS Object, taking the command line args for the constructor
# Runs the attack and writes the details to a file
dos = Dos(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
dos.run()
dos.write_details()

