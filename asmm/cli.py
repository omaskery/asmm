import argparse
import os


import asmm


def main():
    parser = argparse.ArgumentParser(
        description="utility for managing build, test and modularisation of ArmA mods"
    )
    parser.set_defaults(func=None)
    subparsers = parser.add_subparsers()
    init_parser = subparsers.add_parser('init', help='initialise a new project directory')
    init_parser.add_argument('path', help='where to create the new project folder')
    init_parser.set_defaults(func=_initialise, parser=init_parser)
    build_parser = subparsers.add_parser('build', help='combines missions & assets ready for play or test')
    build_parser.add_argument(
        '-C', '--directory',
        help='configure where project folder to build is, defaults to current directory'
    )
    build_parser.set_defaults(func=_build, parser=build_parser)
    deps_parser = subparsers.add_parser('deps', help='manage project dependencies')
    deps_parser.add_argument(
        '-C', '--directory',
        help='configure where project folder to build is, defaults to current directory'
    )
    deps_parser.set_defaults(func=_deps, parser=deps_parser)
    deps_subparsers = deps_parser.add_subparsers()
    deps_list_parser = deps_subparsers.add_parser('list', help='list project dependencies')
    deps_list_parser.set_defaults(func=_deps_list, parser=deps_list_parser)
    deps_add_parser = deps_subparsers.add_parser('add', help='add a project dependency')
    deps_add_parser.add_argument(
        'dependency', help='URI of the dependency to add'
    )
    deps_add_parser.set_defaults(func=_deps_add, parser=deps_add_parser)
    deps_remove_parser = deps_subparsers.add_parser('rm', help='remove a project dependency')
    deps_remove_parser.add_argument(
        'dependency', help='URI of the dependency to remove'
    )
    deps_remove_parser.set_defaults(func=_deps_rm, parser=deps_remove_parser)
    args = parser.parse_args()

    if args.func is None:
        parser.print_help()
        return

    try:
        args.func(args)
    except asmm.AsmmError as error:
        print(f"error: {error}")


def _initialise(args):
    asmm.initialise(args.path)


def _build(args):
    path = os.getcwd() if args.directory is None else args.directory
    asmm.build(path)


def _deps(args):
    args.parser.print_help()


def _deps_list(args):
    path = os.getcwd() if args.directory is None else args.directory
    dependencies = asmm.list_dependencies(path)
    for dependency in dependencies:
        print(f"{dependency}")


def _deps_add(args):
    path = os.getcwd() if args.directory is None else args.directory
    asmm.add_dependency(path, args.dependency)


def _deps_rm(args):
    path = os.getcwd() if args.directory is None else args.directory
    asmm.remove_dependency(path, args.dependency)


if __name__ == "__main__":
    main()
