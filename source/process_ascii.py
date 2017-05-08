"""Process .asc files to .dat files.

Read .asc files and convert to numpy arrays.
Write arrays to file as .dat files.

Author: Maxwell Grady
Date: May 2017

Usage:
python process_ascii.py inputdirectory outputdirectory
"""
import numpy as np
import os
import sys


def main():
    """Run from the commandline - user arguments passed into sys.argv."""
    if len(sys.argv) < 3:
        print("Error: Invalid number of command line arguments")
        print("Usage: python process_ascii.py inputdirectory outputdirectory")
        return

    indir = sys.argv[1]
    if not os.path.exists(indir):
        print("Error: input directory, {}, does not exist.".format(indir))
        return

    outdir = sys.argv[2]
    if not os.path.exists(outdir):
        try:
            os.mkdir(outdir)
        except FileNotFoundError:
            print("Error: output directory, {}, does not exist.".format(outdir))
            print("Attempt to create directory failed.")
            return

    asc = [name for name in os.listdir(indir) if name.endswith('.asc')]
    if not asc:
        print("Error: no .asc files found in input directory, {}".format(indir))
        return
    print("Found {} .asc files to process.".format(len(asc)))
    for fl in asc:
        with open(os.path.join(indir, fl), 'rb') as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            if line == b'Datasection\r\n':
                di = idx + 1
                break
        data = []
        text = lines[di:]
        for line in text:
            data.append(line.decode().split(' ')[:-1])
        data = np.array(data, np.uint16)
        outfile = os.path.join(outdir, fl.split('.')[0] + '.dat')
        with open(outfile, 'wb') as o:
            data.tofile(o)
            print("Writing raw data to file, {}".format(outfile))


if __name__ == '__main__':
    sys.exit(main())
