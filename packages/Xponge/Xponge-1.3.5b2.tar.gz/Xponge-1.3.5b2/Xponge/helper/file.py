"""
    This **module** helps to process the files of molecular modelling
"""
import io
import re
import sys
from pathlib import Path
from importlib import import_module
from . import set_global_alternative_names, Xprint

__all__ = ["file_filter", "pdb_filter", "import_python_script"]

def import_python_script(path):
    if not isinstance(path, Path):
        path = Path(path)
    sys.path.append(str(path.parent))
    if path.suffix != ".py":
        raise TypeError(f"{path} should be a python script")
    import_module(path.stem)

def file_filter(infile, outfile, reg_exp, replace_dict):
    """
        This **function** finds the lines which contains any of the given regular expressions and replace some parts.

        :param infile: the input file or filename
        :param outfile: the output file or filename
        :param reg_exp: a list of regular expressions, if a line matches any of the regular expressions, the line will be kept.
        :param replace_dict: a dict of regular expressions and the replacement
    """
    if not isinstance(reg_exp, list):
        raise TypeError('reg_exp should be a list of regular expressions')
    if not isinstance(replace_dict, dict):
        raise TypeError('replace_dict should be a dict of regular expressions and the replacement')
    if isinstance(infile, io.IOBase):
        filename = "in-memory string"
    else:
        filename = infile
        infile = open(infile, "r")
    lines = ""
    with infile as f:
        for line in infile:
            for keyword in reg_exp:
                if not isinstance(keyword, str):
                    raise TypeError('reg_exp should be a list of regular expressions')
                if re.match(keyword, line):
                    for reg, rep in replace_dict.items():
                        line = re.sub(reg, rep, line)
                    lines += line
                    break
    if not isinstance(outfile, io.IOBase):
        outfile = open(outfile, "w")
    with outfile as f:
        f.write(lines)

def pdb_filter(infile, outfile, heads, hetero_residues, rename_ions=None):
    """
        This **function** finds the lines in pdb which meets the need

        :param infile: the input file or filename
        :param outfile: the output file or filename
        :param head: a list of heads which will be included
        :param hetero_residues: a list of hetero residue names which will be included
        :param rename_ions: a dict to rename the ions
    """
    if not isinstance(heads, list):
        raise TypeError("heads should be a list")
    if not isinstance(hetero_residues, list):
        raise TypeError("hetero_residues should be a list")
    if rename_ions is None:
        rename_ions = {}
    if not isinstance(rename_ions, dict):
        raise TypeError('replace_dict should be a dict of regular expressions and the replacement')
    replace_dict = {}
    for a, b in rename_ions.items():
        if len(a) == 1:
            aname = f"{a}   | {a}  |  {a} |   {a}"
            rname = f"{a}  | {a} |  {a}"
        elif len(a) == 2:
            aname = f"{a}  | {a} |  {a}"
            rname = f" {a}|{a} "
        elif len(a) == 3:
            aname = f"{a} | {a}"
            rname = a
        else:
            raise ValueError("The ion name in a pdb file should not be longer than 3 characters")
        replace_dict["(^HETATM [ 0-9]{4} )(%s)(.)(%s)"%(aname, rname)] = f"\g<1>{b:4s}\g<3>{b:3s}"
    reg_exp = []
    for head in heads:
        reg_exp.append(f"^{head}")
    for hetres in hetero_residues:
        if len(hetres) == 1:
            hetres = f"{hetres}  | {hetres} |  {hetres}"
        elif len(hetres) == 2:
            hetres = f" {hetres}|{hetres} "
        reg_exp.append("^HETATM.{11}%s"%(hetres))
    file_filter(infile, outfile, reg_exp, replace_dict)

set_global_alternative_names()