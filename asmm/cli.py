import argparse
import os


from . import initialise, build


def main():
    parser = argparse.ArgumentParser(
        description="utility for managing build, test and modularisation of ArmA mods"
    )
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers()
    init_parser = subparsers.add_parser('init', help='initialise a new project directory')
    init_parser.add_argument('path', help='where to create the new project folder')
    init_parser.set_defaults(func=_initialise)
    build_parser = subparsers.add_parser('build', help='combines missions & assets ready for play or test')
    build_parser.add_argument(
        '-C', '--directory',
        help='configure where project folder to build is, defaults to current directory'
    )
    build_parser.set_defaults(func=_build)
    args = parser.parse_args()

    if args.func is None:
        parser.print_usage()
        return

    args.func(args)


def _initialise(args):
    initialise(args.path)


def _build(args):
    path = os.getcwd() if args.directory is None else args.directory
    build(path)


if __name__ == "__main__":
    main()
