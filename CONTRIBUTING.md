# How to Contribute to PLEASE: The Python Low-energy Electron Analysis SuitE
Contributions from Users and interested parties are welcomed and encouraged!
In order to make the PLEASE software package a more well rounded and full featured option for LEEM and LEED analysis input, feedback, and contributions from outside sources are essential. Here are a few guidelines for contributing to this project.

## Code Guidelines
I generally try to follow the PEP-8 python coding convention. However, I have not adhered to this with 100% strictness. Notable departures include a maximum allowed line length of 120 characters and sometimes unorthodox naming conventions. Many variables and methods in the source code require long names to be adequately descriptive. I favor descriptive naming at the expense of longer lines in the source code. Also, I choose to capitalize the acronyms LEEM and LEED which feature in numerous variable and method names. This sometimes leads to unorthodox naming compared to that suggested by PEP-8. When contributing to this source code, I simply ask that any and all variables, methods, and classes be labeled in a descriptive manner with LEEM/LEED capitalized. Outside of that, I do not ask that you must follow PEP-8 with 100% strictness.

## Discussion
The Issues section on the main repository: https://github.com/mgrady3/PLEASE/issues is a great place for discussion about the codebase, bugs that are present, features that could be added, etc.

## Bug Reports
When reporting bugs, please try to report as much information as possible about your runtime environment the bug itself. Please provide as much detail as possible concerning the minimal steps necessary to reproduce the bug.

To aid the process of reporting bugs in the software, a method is provided to write a text file containing information about the runtime environment being used as well as the general specifications of the hardware for the system running the software. Located in the Help menu, select "Generate User Config File". This will writes two files to the source directory in a folder called "config-info-output". The file contains information concerning your python version, versions of all installed libraries, etc. This information may be useful for tacking down the source of bugs. One file will be called "Environment.yaml" and is only written if you are using the Anaconda python distribution (or Miniconda). The second file will be called "configinfo" and has the current date appended. This contains more information about your runtime environment.

## Contributing Changes
Changes to the code should ideally happen in a separate branch from the master branch. The branch should be given a descriptive name to detail what change or feature is being worked on. I prefer that branches involving code changes, feature additions, and bugfixes be prefixed with 'dev_' to indicate that the branch is a development branch and thus may not be stable or up to date with the master.

### Code Changes, Bug fixes, and Feature Additions
To contribute a new feature, a refactoring of the code, or a bug fix, please first use the Issue tracker to open a discussion. Here we can choose the best course of action. Generally, if the bug/feature is not something I will work on myself I will ask that you place a pull request (PR). In your PR, you can then create a new branch based off the master with an appropriately named title. You may then make the required changes to any and all files. I will try to review pull requests in a timely manner and determine if the changes should be implemented and merged to the master branch.


### Documentation
I have tried to provide docstrings for all files, classes, and methods in the source code. Sometimes, if a class contains an init() which is fully self explanatory, I provided an empty docstring. The top of each file contains a small header with information about PLEASE and then a few sentences detailing what is contained in that file.

Contributions for documentation are welcome and encouraged. Documentation should try to be descriptive without being overly verbose.

### Testing
For all changes that are not simple and trivial, I prefer that the code be tested across all operating systems if possible. The three OS that I use for testing are OS X (version 9 or higher), Windows 10, and Ubuntu 16.04. If you do not have acces to these OS, please contact me for help in testing the new changes.

### Communication
The most important process of contributing to the PLEASE software package is maintaining communication. The github Issue tracker will be the primary method for discussion, however, I welcome communication via email as needed. Maintaining a constant channel of communication about current issues is important to the future development of this software.
