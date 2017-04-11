"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: April, 2017

PLEASE provides a convienient Graphical User Interface for exploration and
analysis of Low Energy Electron Microscopy and Diffraction data sets.
Specifically, emphasis is placed on visualization of Intensity-Voltage data
sets and providing an easy popint and click method for extracting I(V) curves.

Analysis of LEEM-I(V) and LEED-I(V) data sets provides inisght with atomic
scale resolution to the surface structure of a wide array of materials from
semiconductors to metals in bulk or thin film as well as single layer 2D materials.

Config Info Generation:
    Methods in this file are used for generating as much information as possible
    regarding the User's runtime environment. This is useful for debugging problems
    related to installed libraries and the python runtime.
"""

import os
import platform
import pprint
import sys
import subprocess

# 3rd party imports
import pendulum


def output_environment_config():
    """Output a textfile containing runtime environment information.

    This can be used to help address issues that a User may face
    concerning problems with their installed libraries.
    """
    packagepath = os.path.join(os.getcwd(), os.pardir)
    outdir = os.path.join(packagepath, "config-info-output")
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    # outputpath = os.path.join(os.getcwd(), "config-info-output")

    conda = using_conda()
    pypath = check_python_path_set()
    platforminfo = get_platform_info()

    if conda:
        cmd = "conda env export > {}".format(os.path.join(outdir, "Environment.yaml"))
        os.system(cmd)

    with open(os.path.join(outdir, "configinfo" + get_date_string() + '.txt'), 'w') as f:
        f.write("# User Runtime Configuration Settings # \n")
        f.write("User Platform Info: \n\n")
        pp = pprint.PrettyPrinter(indent=4, stream=f)
        pp.pprint(platforminfo)

        if pypath is not None:
            f.write("User has $PYTHONPATH set to: {} \n".format(pypath))
        else:
            f.write("No $PYTHONPATH set\n\n")
        f.write("Using Anaconda Python or Miniconda from Continuum Analytics = " + str(conda)+"\n")
        f.write("Note- If Using Anaconda or Miniconda:")
        f.write("\tThe conda environment settings are written to a separate file: Environment.yaml\n\n")

        # Conda Environment.yaml should include pip instaleld modules
        # For clarity they are included here
        piptext = subprocess.check_output(["pip", "freeze"])  # returns bytes
        piptext = piptext.decode()  # should be string now
        f.write("Pip Installed Modules: \n")
        for module in piptext.split("\n"):
            f.write("\t" + module + "\n")
    return


def get_date_string():
    """Get Today's date to append to config filename."""
    today = pendulum.today()
    return str(today.month)+'-' + str(today.day) + '-' + str(today.year)


def get_platform_info():
    """Used by output_environment_config to get User platform information."""
    machine_type = platform.machine()
    cpu = platform.processor()
    system = platform.system()
    version = platform.version()
    pyversion = platform.python_version()

    return {'machine_type': machine_type,
            'cpu': cpu,
            'system': system,
            'system_version': version,
            'python_version': pyversion}


def using_conda():
    """Check if User's python runtime is provided by Anaconda or Miniconda."""
    if "continuum" in sys.version.lower() or "anaconda" in sys.version.lower:
        return True
    return False


def check_python_path_set():
    """Check if User had $PYTHONPATH environment variable set."""
    try:
        pypath = os.environ['PYTHONPATH']
    except KeyError:
        return None
    return pypath
