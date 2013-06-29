import shrink
import plasma
import pngsaver
import matrixfix
import numpy
import math


def zoom(fileName, size, numberofzooms, roughness, perturbance, \
        fromColor = [0,0,255], toColor = [255,255,255], ask = True):
    """ 
    Saves a series of png files that, when animated, show the viewer zooming
    into a plasma fractal.
    filename: the starting name for the png file series.  A series index will
    be appended to each file.  Ex: filename = "plasma" with 16 files would produce
    plasma000.png through plasma015.png.
    numberOfZooms: The number of times the image width is halved.  
    (After the image width is halved, a new fractal is created based on the previous values.)
    The number of images will be 16 x numberOfZooms.
    roughness (from 0 to 1): the overall noise level 
    perturbance (from 0 to 1): the size-proportional noise level
    fromColor: the starting point for the image gradient as [r,g,b] (default is blue)
    toColor: the ending point for the image gradient as [r,g,b] (default is white)
    ask: set to False to avoid a user prompt.
    """
    
    # check whether the size is valid
    n = math.log(size-1, 2)
    if n != float(int(n)):
        print "The size is not valid, choose a side that is a power of 2 + 1."
        print "65, 129, 257, 513, 1025, etc."
        return
    largerSize = math.pow(2, n) + 1 
    print "This method will create",  numberofzooms * 16, "image files."
    if (ask):
        answer = raw_input("Is that okay?")
        if answer == "N" or answer == "n" or answer=="No" or answer=="no":
            return
    fractalsd = 0
    maxCrop =  (size-1)/4
    cropIncrement =  max((size-1)/64, 1)
    fractal = None
    fileNumber = 0
    for f in range(numberofzooms):
        if (None == fractal):
            fractal = plasma.diamondSquareFractal(largerSize, roughness, perturbance)
            #fractalsd = numpy.std(fractal)
        else:
            fractal = plasma.double(\
                fractal[maxCrop:largerSize-maxCrop, maxCrop:largerSize-maxCrop],\
                roughness, perturbance)
        fractalsd = numpy.std(fractal)
        for i in range(16):
            file = "{0}{1}.png".format(fileName, fileNumber)
            if (fileNumber < 10):
                file = "{0}00{1}.png".format(fileName,fileNumber)
            elif (fileNumber< 100):
                file = "{0}0{1}.png".format(fileName,fileNumber)
            fileNumber += 1
            currentCrop = i*cropIncrement
            slice = fractal[currentCrop:largerSize-currentCrop,\
                         currentCrop:largerSize-currentCrop]
            #slice = matrixfix.setStd(slice, fractalsd)
            slice = matrixfix.normalize(slice)
            mat = shrink.shrinkMatrix(slice, size)
            print "saving", file
            pngsaver.saveGradient(file, mat, [0,0,255], [255,255,255])
            
