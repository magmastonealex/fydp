#!/usr/bin/python3

import argparse
import subprocess

from lib.config import CONFIG_DATA


def upCommand(args, unknownArgs):
    print("Fake creating environment")
    print(args, unknownArgs)


def downCommand(args, unknownArgs):
    print("Fake turning off environment")
    print(args, unknownArgs)


def nukeCommand(args, unknownArgs):
    print("Fake nuking environment")
    print(args, unknownArgs)


def runScript(_, unknownArgs, script):
    # TODO run this in the container once it exists
    subprocess.run("{} {}".format(script, " ".join(unknownArgs)), shell=True)


def buildCustomCommandParser(subparsers, name, info):
    parser_custom = subparsers.add_parser(
        name, help=info.get("help"), description=info.get("description")
    )
    parser_custom.set_defaults(
        func=lambda args, unknownArgs: runScript(args, unknownArgs, info["script"])
    )


def getParser(actions):
    parser = argparse.ArgumentParser(description="ENVY DESCRIPTION TODO")
    subparsers = parser.add_subparsers(dest="subparser_name")
    # Create 'up' parser
    parserUp = subparsers.add_parser("up", help="ENVY UP HELP")
    parserUp.set_defaults(func=upCommand)

    # Create 'down' parser
    parserDown = subparsers.add_parser("down", help="ENVY DOWN HELP")
    parserDown.set_defaults(func=downCommand)

    # Create 'nuke' parser
    parserNuke = subparsers.add_parser("nuke", help="ENVY NUKE HELP")
    parserNuke.set_defaults(func=nukeCommand)

    # Create parsers for arbitrary custom commands
    for action in actions:
        buildCustomCommandParser(subparsers, action["name"], action)

    return parser


def main():
    parser = getParser(CONFIG_DATA["actions"])
    args, unknown = parser.parse_known_args()
    if args.subparser_name:
        args.func(args, unknown)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
