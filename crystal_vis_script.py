""" Script which takes in large 3D datasets of .CSV type and exports .png frames of them for further visualisation.

    This script, when run in a paraview shell, will take a collection of data points in a .CSV format and produce a formatted clipped
    set of visualised frames for each data point within the file. This script particularly is tailored at materials such as irradiated
    zirconium. An example of this, for said zirconium, would be running FrameCreation(/home/user/Desktop/Data/Max Data/CSVData/,/home/user/Desktop/Data/Max Data/CSVData/Frames, Temp)
    Which would produce a set of frames for all the data given in the directory for which their primary attribute shown is
    the scalar variable Temp. This would be seen as the crystal structure with major temperature spots seen within the crystal
    and coloured accordingly. (See README image)

    Lisence: MPL-2.0 

"""

from paraview.simple import *
from paraview.servermanager import *  # MAKE SURE TO INCLUDE THIS MODULE WHEN LOADING VTK FILES!!!!!!!!!!!!
from os import listdir
from os.path import isfile, join


# The directory you want to create stills from
# Sorts through your directory to create a list of all of the files
mypath = "/home/user/Desktop/Data/Max Data/ConvertedData/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.sort()


# The directory where you want your Stills/Frames to be saved
finalShotPath = (
    "/home/user/Desktop/Data/Max Data/ConvertedData/DataAndScreenshots/Screenshots/"
)

# This is the name of the scalar you would like to see in your .CSV file
ScalarName = "Strain Scaling Factor"

# The value you would like to do the scalar clip from. i.e Only values above this value will be shown.
ScalarVal = 0.15

# Number of frames you would like. This default does all of them in the directory, in order
NoOfFrames = len(onlyfiles)
### Creating empty lists ###
filepaths = []
datapoints = []
finalDataPath = []
finalStatePath = []
finalFilePath = []
imagesList = []

### Defines the standard clip used to show "extreme" or interesting parts of the data###


def MaxClip(
    MyData,
    ScaVal,
    ScalarName,
    ColourRange,
    opacity=0.05,
):

    """Sets the data to the correct view, with opacity and viewing only the scalar value wanted

    Sets the dataset imported to having the correct opacity as well as clipping the data to only show the specified scarlar variable
    and only from the Scalar value specified and up. This also sets an average colour array on to it to colour it specified based on the
    variable values given

    Args:
        MyData: The data which has been imported in, usually in paraview documentation under the name reader.
        ScaVal: The value for which you would like to clip from for your scalar
        ScarlarName: The name of the variable you would like clip with e.g "Temp"
        Range: The range over which the colour scale will be set. E.g ColourRange = (0,0.2)
        Opacity: The opacity wanted for the clipped data. Default value = 0.05

    Returns:
        The clipped view within paraview with set colours and set opacity


    """

    SetDisplayProperties(Opacity=opacity)
    clip = Clip(Input=MyData)

    clip.ClipType = "Scalar"
    clip.Scalars = ("POINTS", ScalarName)
    clip.Value = ScaVal
    clip.Invert = False

    display = Show(clip)

    ColourMap = GetColorTransferFunction(ScalarName)
    SetDisplayProperties(ColorArrayName=ScalarName)
    ColorBy(display, ("POINTS", ScalarName))
    ColourMap.RescaleTransferFunction(ColourRange)


### Turns the .CSV to actual points to be seen ###


def PointsView(reader):
    TableToPoints(
        Input=reader, XColumn="X Position", YColumn="Y Position", ZColumn="Z Position"
    )

    return print("Interpolated to points")


### Colours the points based on a set range ###
#                       ###


def MaxColour(points, ScalarName, Range=(0, 0.2)):
    SetDisplayProperties(ColorArrayName=ScalarName)
    display = Show(points)

    ColorBy(display, ("POINTS", ScalarName))

    ColourMap = GetColorTransferFunction(ScalarName)
    ColourMap.RescaleTransferFunction(Range)
    # You can change colour preset here ###
    ColourMap.ApplyPreset("Inferno (matplotlib)", True)
    return print("Coloured data")


### A function to saved the clipped data if you want to use it later on ###


def savedata(filepath):
    SaveData(filepath)

    return print("Saved Data")


### Saves the screenshot of the current view ###
def ScreenShot(filepath):
    myview = GetActiveView()
    myview.CameraPosition = [1000, 800, 800]
    myview.CameraViewUp = [0, 0, 1]

    SaveScreenshot(filepath + ".png", myview, ImageResolution=[1500, 1500])

    return print("Saved Screenshot")


### Connects all the other functions into one ###
def CrystalVis(reader, ShotPath, ScalarName, opacity=0.05):
    points = PointsView(reader)
    print()
    MaxColour(points, ScalarName)
    print()
    MaxClip(points, ScalarVal, ScalarName, opacity)

    ScreenShot(ShotPath)


### Adds all the files in the directory into a list and sorts it so it appears in numerical order ###


# A final function to create an amount of frames specified
def FrameCreation(
    File, FilePathForScreenshot, ScalarName, opacity=0.05, NoOfFrames=len(onlyfiles)
):
    """Converts 3D datasets to frames

    Obtains 3D datasets in .CSV format and converts them into frames by putting them
    into a paraview project and outputting frames of the data.

    Args:
        File: Your filepath for your data in .CSV format
        FilePathForScreenshot: Your directory you would like your screenshots to end up in
        ScalarName: The scalar you would like to act on to create your frames
        Opacity: Allows you to set an opacity for your data (default at 0.05)
        NoOfFrames: Allows you to specifiy how many frames of data you would like to create (Default: all of them)

    Returns:
        A collection of frames of the data inputted in .png format in the directory specified to save.

    """

    for i in range(NoOfFrames):  # This shows how many
        print(File[i])
        # This reads the file into the code
        reader = OpenDataFile(mypath + File[i])
        # This processes the data arrays within the vtk file, allowing them to be processed
        reader.GetPointDataInformation()
        # This is a compound function that takes all of the mini functions and processes it all here
        CrystalVis(reader, FilePathForScreenshot + File[i], ScalarName, opacity)

        ResetSession()
        ### 100 frames takes about 18 mins to process for the Max converted data set (85.3 Mbs each) ###


FrameCreation((NoOfFrames), (onlyfiles), finalShotPath, ScalarName)
