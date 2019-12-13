#! /usr/bin/env python3
from ase.io import read, write
from pathlib import Path
from argparse import ArgumentParser


def _extract_single(infile):
    try:
        # Read first image
        atoms = read(infile, index=0)
        return atoms
    except Exception:
        raise

def main():
    parser = ArgumentParser()
    parser.add_argument("infile",
                        type=str,
                        help="Input file with images")
    parser.add_argument("--outfile", "-o",
                          default=None,
                          help="Output file for sorted images. If not specified, overwrite the input")
    args = parser.parse_args()
    infile = Path(args.infile)
    if args.outfile is None:
        outfile = infile.parent / "init.xyz"
    else:
        outfile = Path(outfile)
    
    atoms = _extract_single(infile.as_posix())
    try:
        write(outfile, atoms)
        print("Extracted first image")
    except Exception:
        print("Failed...")
        

if __name__ == '__main__':
    main()
