# PLEASE
PLEASE: The Python Low-energy Electron Analysis SuitE - Enabling rapid analysis and visualization of LEEM and LEED Data.

### Author: Maxwell Grady
### Affiliation: University of New Hampshire Department of Physics
### Current Version: 1.0.0

# What is it?
The **PLEASE** software package provides an open source cross platform graphical user interface for rapid analysis and visualization of Low Energy Electrom Microscopy (LEEM) and selected area micro-spot size Low Energy Electron Diffraction (µLEED) data sets. PLEASE is written in python using the PyQt and pyqtgraph python bindings for the Qt graphics framework.

# Why is it?
LEEM and µLEED are powerful techniques for surface analysis of many types of novel materials and are especially useful for the study of two-deimsntional (2D) materials. Specific emphasis is placed on the analysis of Intensity-Voltage (IV) data sets. IV curves map the scattered or reflected electron intensity as a function of incident energy. The structure of these curves is inherently linked to the atomic surface structure of the target material. Given that the electronic properties of many 2D materials are linked to the surface structure, LEEM and µLEED provide unique avenues for the study of novel material properties in reduced dimensions and may help guide future application of these materials.

During my doctoral research I had the opportunity to be involved with a number of LEEM and µLEED experiments as well as the corresponding data analysis. At the time of this work, there were few if any open source solutions for analyzing LEEM and LEED data sets. Since the analysis routines for varying LEEM and µLEED experiments are essentially the same, I decided to write a piece of software to streamline the data anlaysis for my work and provide an easy to use interface for extraction of IV data from the experimental data. The project served a dual purpose to enhance my research group's capability to help with analysis for LEEM and µLEED experiments as well as to teach myself about scientific software development. 

# What can it do?
PLEASE provides an easy interface for visualization of LEEM and LEED data sets while also providing a convenient user-friendly point-and-click method for extracting IV curves. Alongside the data extraction fucntionality, basic data transformation tools are provided to smooth the IV curves, reducing instrument noise, and subtract background signal from the IV data.

Since LEEM and LEED data sets are collected with a wide range of experimental parameters, PLEASE provides an easy method for working with multiple data sets. Rather than having to input the experimental parameters each time data is loaded for analysis, the parameters are stored in a human readable structured text file using the YAML format. An example configuration file is provided with this source code. To setup a new data set for analysis, all that must be done is create a copy of the configuration template and fill in the required paramters. PLEASE can then load the experiment settings from the file and then load the data files accordingly.

#### The necessary infor for loading data is as follows:
* Image parameters:
  * Image Height [integer] 
  * Image Width [integer]
* Energy parameters (in eV):
  * Starting Energy [single decimal float i.e. 2.0]
  * Final Energy [single decimal float i.e. 2.0]
  * Step Energy [single decimal float i.e. 2.0]
* Data parameters:
  * Data Type [string] valid parameters are {"Image", "Raw"}
  * File format [string] {".tif", ".png", ".dat"}
  * Bit Depth (Required for loading raw data) [integer] valid parameters are {8, 16} for 8 and 16 bit data respectively
  * Byte Order (Required for loading raw data) [string] {"L" for little endian, "B" for big endian}
  * Data path [string pointing to folder containing data files]
        
        
