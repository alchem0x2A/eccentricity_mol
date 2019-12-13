#! /usr/bin/env python3
from .obabel.utils import run_job
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("infile",
                          type=str,
                          help="Input file with images")
    parser.add_argument("--outfile", "-o",
                          default=None,
                          help="Output file for sorted images. If not specified, overwrite the input")
    args = parser.parse_args()
    run_job(job="3D", infile=args.infile, outfile=args.outfile)

if __name__ == '__main__':
    main()
