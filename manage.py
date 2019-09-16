import os
import sys

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

import commands
import app


def command(method, *args):
    if method == 'task':
        commands.run(*args)
    elif method == 'dev_server':
        app.run_dev()
    else:
        print("unknown command {0}".format(method))


def usage():
    print("{0} task".format( sys.argv[0]))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command(*sys.argv[1:])
    else:
        usage()
