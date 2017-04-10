The Experimental parameters that define each LEEM and LEED experiment are required by PLEASE to load each data set. For each data set you would like to analyze with PLEASE, you need to create a .yaml file with the corresponding parameters in the following format:


Experiment:
# Required Parameters
    Type:  # Choose either "LEEM" or "LEED" [string]
    Name:  # This can be anything you liker [string]
    Data Type:  # Choose either "Image" or "Raw" [string]
    File Format:  # File Extension including the . [string]
    Image Parameters:
        Height:  # Height of your image data[int]
        Width:  # Width of your image data[int]
    Energy Parameters:
        Min:  # Starting energy in eV [float]
        Max:  # Final energy in eV [float]
        Step:  # Energy step between each image in eV [float]
    Data Path:  # Absolute path to your data files [string]

# Additional Required parameters if "Raw" is your data type
    Bit Size:  # Number of bits per pixel in your data (Must be 8 or 16) [int]
    Byte Order:  # 'Endian-ness' Choose either "L" or "B" [string]

 An example of an experiment configuration file can be seen in this same directory in the file "Experiment.yaml"
