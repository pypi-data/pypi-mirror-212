"""
This **package** helps to run the molecular dynamics simulation
"""
import os
import sys
from ..helper import Xopen, Xprint, set_global_alternative_names


def run(args):
    """
    call SPONGE to run the MD simulation

    :param args: a string or a list of arguments
    :return: None
    """
    if isinstance(args, str):
        args = args.split()
        args.insert(0, sys.argv[0])

    if len(args) < 2 or args[1] in ("-h", "--help"):
        Xprint(""" mdrun: run the SPONGE md simulation
        Usage:
            mdrun, mdrun -h, mdrun --help: see this help
            mdrun -set BIN_PATH: set the SPONGE path to BIN_PATH
                                 BIN_PATH can be an absolute path or a relative path to this module file
            mdrun -reset: reset the SPONGE path to ../../bin
            mdrun SPONGE*:  run SPONGE""")
        sys.exit()

    this_path = os.path.dirname(__file__)

    if args[1] == "-set":
        f = Xopen(os.path.join(this_path, "BIN_PATH.dat"), "w")
        f.write(args[2])
        f.close()
        sys.exit()
    elif args[1] == "-reset":
        f = Xopen(os.path.join(this_path, "BIN_PATH.dat"), "w")
        f.write("../../bin")
        f.close()
        sys.exit()

    f = Xopen(os.path.join(this_path, "BIN_PATH.dat"), "r")
    that_path = f.read().strip()
    f.close()

    if not os.path.isabs(that_path):
        that_path = os.path.join(this_path, that_path)

    cmd = os.path.join(that_path, args[1])
    if not (os.path.exists(cmd) or os.path.exists(cmd + ".exe")):
        t = os.system(args[1] + " -v")
        if t != 0:
            Xprint("No MD Engine found.\n" +
                  f"  There is no executable program named '{args[1]}' in '{that_path}' or PATH\n" +
                   "  Maybe you need to use Xponge.mdrun -set SPONGE_PATH to set the path to MD Engine, " +
                   "or add the path to your environment variables",
              "ERROR")
            sys.exit(1)
        else:
            cmd = args[1]
    if len(args) > 2:
        cmd += " " + " ".join(args[2:])
    return os.system(cmd)

set_global_alternative_names()
