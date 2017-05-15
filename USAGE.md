# PLEASE
PLEASE: The Python Low-energy Electron Analysis SuitE - Enabling rapid analysis and visualization of LEEM and LEED Data.

### Author: Maxwell Grady
### Affiliation: University of New Hampshire Department of Physics
### Current Version: 1.0.0

# Usage:

The PLEASE software package is primarily used for visualization of LEEM/LEED-I(V) data sets and extraction/plotting of I(V) curves. In order to load data for visualization, the experimental configuration settings must be read in from a .yaml file.

## Test Data:
There are two types of test data provided with the source repository: one set of actual experimental LEEM and LEED I(V) data, and one set of computer generated LEEM and LEED I(V) data. The computer generated data can be used to ensure PLEASE is functioning correctly. To load the test data sets, you will need to edit the Path setting in the .yaml file provided with each test data. Enter the absolute path to the data files on your computer.

For example: Assuming you want to load the computer generate LEED-I(V) test data set
and you have cloned the PLEASE git repository to your Desktop, then path you need to enter will be similar to this -

    "/Users/yourusername/Desktop/PLEASE/TestData/TestDataSets/LEEDTestData/dat2/"

## Experiment YAML files:
The minimal set of required parameters to load a data set for visualization in PLEASE is as follows:

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

This data must be saved as a .yaml file following the format provided in the ExperimentYAML section of the source repository. There is an instruction file that details how to create/edit a .yaml file in the correct format for PLEASE.

For convenience, PLEASE provides a GUI method for creating experiment configuration files. Select "Generate Experiment Config File" from the File menu to display a window where you can input the above settings. This will then allow you to save the file in the correct format.

## Loading Data:

To Load data for visualization, select the Load Experiment button from the left hand side of the PLEASE GUI. This will prompt you to select a .yaml file that contains the configuration settings for the experiment you want to load. After selecting the .yaml file, PLEASE will automatically select either the LEEM or LEED tab based on the settings provided in the .yaml file. During the data loading process some messages will be displayed in the bottom console outlining the loading procedure. When the loading has finished you should see one of the images from your data set displayed on the left.

## I(V) Analysis:

Visualization and extraction of I(V) data happens in two separate ways for LEEM and LEED Data sets. When viewing LEEM I(V) data, data images are displayed on the left and the right hand side displays a plot area for I(V) plots. To display different images from the data set, the right/left arrow keys can be used to navigate through the available images.

  * LEEM-I(V):
      *  When viewing LEEM data, I(V) curves are extracted from a single pixel extended through the data set and plotted against the incident electron energy. PLEASE automatically tracks the mouse movement when the mouse is in the image region and plots the I(V) in real time to the right hand side plot area.
      * For clarity, a yellow crosshair is overlaid atop the image area designating the point where the I(V) data is being extracted from.
      * The thickness of the crosshair can be adjusted in the CONFIG tab.
      * Clicking the main image area will overlay a circular patch on the image in the location of the click and open a new window with a static I(V) plot from that location. Multiple static curves can be plotted in this fashion.
      * To output LEEM-I(V) data to text, select a number of locations by clicking the image. Finally click the Output LEEM IV button on the left hand side. This will open a prompt to select first the directory you wish to save the files in and finally a second prompt to enter a name for the files.
      * When multiple curves are output at once, each consecutive file takes the basename entered by the USER and appends a number to the end: file0.txt, file2.txt ...
      * I(V) curves are output to test files as tab delimited data with two labeled columns E (eV) and I (arbitrary units).
  * LEED-I(V)
      * The extraction of I(V) curves from LEED-I(V) data sets is somewhat different from LEEM analysis. This is due to the fact that the intensity of an entire electron beam spot must be summed and averaged. Thus, rather than extracting the I(V) curve from a single pixel, a square window with adjustable size is used.
      * Rather than tracking mouse movement and plotting the I(V) curves in real time, for LEED data sets the User selects electron beam spots by clicking the left hand side image.
      * Clicking the left hand side image will create a square box centered on the mouse position. The box size can be adjusted in the CONFIG tab.
      * To extract the I(V) curves from the selected boxes, select "Extract-I(V)" from the LEED Menu. This will plot the I(V) curve(s) on the right hand side color coded to match the selection box(es).
      * To output LEED-I(V) curves to text, select a number of location in the image area then press the "Output LEED IV" button on the left hand side. This will open a prompt to select first the directory you wish to save the files in and finally a second prompt to enter a name for the files.
      * When multiple curves are output at once, each consecutive file takes the basename entered by the USER and appends a number to the end: file0.txt, file2.txt ...

## Data Smoothing
More often than not, the raw output from the CCD on the LEEM instrument will be a noisy signal. This may be due to sample quality as well as inherent instrumentation noise. To help reduce the level of noise in the I(V) curves, PLEASE provides a built in method for smoothing the data via convolution with a known window function. The CONFIG tab provides settings for smoothing LEEM and LEED data. The available window functions are: Flat (boxcar average/sliding average), Bartlett, Blackman, Hanning, and Hamming. In general, a decent degree of smoothing can be obtained by simply choosing to perform a sliding average (Flat window) and choosing an appropriate window length based on the input data. I(V) data sets with a smaller energy (0.1 or 0.5eV) step can use a larger smoothing window (8-10) whereas data sets with a larger energy step (1 eV) should use a smaller smoothing window (4-6).

When outputting I(V) curves to text, if data smoothing is enabled then the smoothed data will be output to text. To output the raw data to text simply disable the data smoothing in the CONFIG tab before outputting the data to text.

## Background Analysis
Analysis of LEEM-I(V) data sets generally does not require a treatment of the electron background.

A common procedure for analysis of LEED-I(V) data is to attempt to remove the intensity of the background inelastic electrons from the extracted I(V) curves. While PLEASE does not provide an inherent background subtraction method, there are a number of ways to collect background data from the experimental data.

When selecting an electron beam spot for I(V) analysis, the User can also select boxes of the same size or smaller size in close proximity to the selected beam spot. By extracting the I(V) curves from all boxes, then the intensity of the local background can be compared to that of the electron beam spot.

To aid this procedure, a feature is included in the LEED menu - Auto Background Selection. When this method is triggered form the menu, all current electron beam selections will be surrounded by six smaller selection windows. Upon extracting the I(V) curves, the electron beam spot curves will be plotted and color coded to the selection box. The background curves will be displayed in white, matching the color of the background boxes surrounding the electron beam spots.

When outputting the I(V) curves to text, each user selected electron beam I(V) curve will be output followed by the six curves automatically generated background curves. The background files will have 'bkgnd' appended to their names to clarify that they represent text files for the background curves.

With both the electron beam spot I(V) curve and the background curves output to text, the background curves can be averaged together and subtracted from the main I(V) curve as needed via any number of post processing methods.


In the future, additional features may be included to provide alternate methods of reducing the noise in the data. For example, a feature currently being tested, which applies only to LEED data, is to remove some of the inelastic electron background from the diffraction images using a gaussian filter subtraction.
