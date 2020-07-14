import sys
import importlib


def main():
    argv = sys.argv
    print argv
    module = importlib.import_module('test1')
    module.run(argv[1:])


if __name__ == '__main__':
    main()
