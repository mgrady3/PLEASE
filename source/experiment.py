"""
PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: March, 2017

Generic LEEM / LEED experiment object
Used for serializing experiment data
This makes it easier to load data from a previously analyzed experiment
"""
import yaml
import pprint

pp = pprint.PrettyPrinter(indent=4)


class Experiment(object):
    """Container object to hold Experiment Parameters.

    These parameters are loaded from User created YAML config files.
    """

    def __init__(self):
        """Initialize empty container object."""
        self._Test = False
        self.exists = True
        self.exp_type = ''
        self.name = ''
        self.path = ''
        self.data_type = ''
        self.ext = ''
        self.bit = ''
        self.byte_order = ''
        self.mine = ''
        self.maxe = ''
        self.stepe = ''
        self.num_files = ''
        self.imw = ''
        self.imh = ''

        self.loaded_settings = None

    def toFile(self):
        """Write experiment settings to a YAML config file.

        To Be Implemented later.
        :return: None
        """
        pass

    def fromFile(self, fl):
        """
        Read in parameters from a YMAL file.

        :param fl: string path to YAML file
        :return:
        """
        with open(fl, 'r') as f:
            self.loaded_settings = yaml.load(f)
        try:
            # Parse Settings into sub groups
            exp_settings = self.loaded_settings['Experiment']
            eng_settings = exp_settings['Energy Parameters']
            img_settings = exp_settings['Image Parameters']

            # Fill Experiment object attributes from loaded settings
            self.exp_type = exp_settings['Type']
            self.name = exp_settings['Name']
            self.path = exp_settings['Data Path']
            self.data_type = exp_settings['Data Type']
            self.ext = exp_settings['File Format']
            self.bit = exp_settings['Bit Size']
            if self.data_type == 'Raw':
                self.byte_order = exp_settings['Byte Order']
            self.mine = eng_settings['Min']
            self.maxe = eng_settings['Max']
            self.stepe = eng_settings['Step']
            self.imw = img_settings['Width']
            self.imh = img_settings['Height']

            # self.loaded_settings = None
            # pp.pprint(vars(self))

        except KeyError as e:
            # TODO: Rewrite this section; Add additional Error handling
            print("Error in Experiment YAML - Check for usage of Valid Keys Only")
            print("Invalid key is {0}".format(e.args[0]))
            print("Valid Experiment Parameters are: name, path, type, ext, bits, byteo, mine, maxe, stepe, and numf")
            print("Please refer to experiment.py docstrings for explanation of valid YAML parameter files.")

    def test_load(self):
        """Test Loading a pre-made file with hard coded path.

        :return: None
        """
        test_file = '/Users/Maxwell/Desktop/141020_03_LEEM-IV_50FOV.yaml'
        with open(test_file, 'r') as f:
            self.loaded_settings = yaml.load(f)
        self._Test = True

    def test_fill(self):
        """Test filling object attributes from YAML file.

        :return: None
        """
        if self.loaded_settings is not None and self._Test:
            try:
                exp_settings = self.loaded_settings['Experiment']
                eng_settings = exp_settings['Energy Parameters']
                img_settings = exp_settings['Image Parameters']
                self.exp_type = exp_settings['Type']
                self.name = exp_settings['Name']
                self.path = exp_settings['Data Path']
                self.data_type = exp_settings['Data Type']
                self.ext = exp_settings['File Format']
                self.bit = exp_settings['Bit Size']
                self.byte_order = exp_settings['Byte Order']
                self.mine = eng_settings['Min']
                self.maxe = eng_settings['Max']
                self.stepe = eng_settings['Step']
                self.imw = img_settings['Width']
                self.imh = img_settings['Height']

            except KeyError:
                print("Error in Experiment YAML - Check for usage of Valid Keys Only")
        self.loaded_settings = None
        self._Test = False
