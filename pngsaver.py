import numpy
import png
import matrixfix
import math
    
def toHeat(matrix):
    """
    creates a heat map from an array of normalized values (range 0 to 1) 
    """
    cosinevector = numpy.vectorize(getcosine)
    # jiggle the values a bit so that the range will be from .25 to 1
    modifiedMatrix = (matrix * .75) + .25
    # values near 1 will be red
    red = cosinevector(modifiedMatrix)
    # values near .7 will be green
    green = cosinevector(modifiedMatrix + .3)
    # values near .5 will be blue
    blue = cosinevector(modifiedMatrix + .5)
    # values near .25 will be black
    
    return mergeColors(red, green, blue)
    
def getcosine(x):
    """
    Gets the cosine of a value between 0 and 1
    returns cos(2piX)
    """
    rad = (x * 2 * math.pi)
    result = math.cos(rad)
    return result
    
def toGradient(matrix, fromColor, toColor):
    """
    """
    import plasma
    
    rgbOffset = [fromColor[0]/float(255), fromColor[1]/float(255), fromColor[2]/float(255)]
    rgbSlope = [toColor[0]/float(255) - rgbOffset[0], 
                 toColor[1]/float(255) - rgbOffset[1], 
                 toColor[2]/float(255) - rgbOffset[2]]
    
    # print "rgbSlope =", rgbSlope, "rgbOffset = ", rgbOffset
   
    red = matrix * rgbSlope[0] + rgbOffset[0]
    green = matrix * rgbSlope[1] + rgbOffset[1]
    blue = matrix * rgbSlope[2] + rgbOffset[2]

    colorMatrix = mergeColors(red, green, blue)

 
    # print "result mean =", colorMatrix.mean(), "result std = ", colorMatrix.std()
    return colorMatrix

def mergeColors(redValues, greenValues, blueValues, alphaValues = None):
    """
    merges arrays representing red, blue, and green and (optionally) alpha
    into an array ready to export to a png file
    """
    red = (redValues * 255).astype(int)
    green = (greenValues * 255).astype(int)
    blue = (blueValues * 255).astype(int)

    rows = red.shape[0]

    colors = 3
    if (alphaValues != None):
        alpha = (alphaValues * 255).astype(int)
        colors = 4
    colorMatrix = numpy.zeros((rows, red.shape[1] * colors))
    
    for i in range(0, red.shape[0]):
        redcol = i * colors
        colorMatrix[:, redcol] = red[:,i]
        colorMatrix[:, redcol+1]= green[:,i]
        colorMatrix[:, redcol+2] = blue[:,i]
    
        if (alphaValues != None):
            colorMatrix[:,redcol + 3] = alpha[:,i]
            
    colorMatrix = matrixfix.flatten(colorMatrix, 0, 255)
    return colorMatrix.astype(int)
     
def savePng(filename, matrix, hasAlpha = False):
    """
    saves an array to a png file.
    """
    pngfile = open(filename, 'wb')
    height = matrix.shape[0]
    width = matrix.shape[1] / 3
    if (hasAlpha):
        width  = matrix.shape[1] / 4
    
    writer = png.Writer(height, width, alpha = hasAlpha)
    writer.write(pngfile, matrix)
    pngfile.close()
   
def saveGradient(filename, matrix, fromColor, toColor):
    """ 
    saves a matrix of values between 0 and 1 to a 
    png with a given gradient.
    """
    color = toGradient(matrix, fromColor, toColor)
    savePng(filename, color)

    
def saveHeat(filename, matrix):
    """
    saves a matrix of values between 0 and 1 to a 
    png as a heat map
    """
    heat = toHeat(matrixfix.normalize(matrix))
    savePng(filename, heat)
    
def saveColors(filename, redMatrix, greenMatrix, blueMatrix, alphaMatrix = None):
    """
    merges a red, green, blue and (optional) alpha matrix and saves
    them as a png file.
    """
    if (alphaMatrix == None):
        merged = mergeColors(redMatrix, greenMatrix, blueMatrix)
    else:
        merged = mergeColors(redMatrix, greenMatrix, blueMatrix, alphaMatrix)
        
    savePng(filename, merged, alphaMatrix != None)

def saveGradient3D(fileName, matrix, fromColor = [0,0,255], toColor =[255,255,255], ask = True):
    """ 
    saves a 3d matrix of values between 0 and 1 to a 
    series of png files with a given gradient.
    The png files can be merged into a movie file using 
    Sequimago or other movie making tools.
    """
    
    numberImages = matrix.shape[2]
    
    print "This method will create",  numberImages, "image files."
    if (ask):
        answer = raw_input("Is that okay?")
        if answer == "N" or answer == "n" or answer=="No" or answer=="no":
            return
    fileNumber = 0
    for f in range(numberImages):

        file = "{0}{1}.png".format(fileName, fileNumber)
        if (fileNumber < 10):
            file = "{0}00{1}.png".format(fileName,fileNumber)
        elif (fileNumber< 100):
            file = "{0}0{1}.png".format(fileName,fileNumber)
        fileNumber += 1

        slice = matrix[:,:,f]
        print "saving", file
        saveGradient(file, slice, [0,0,255], [255,255,255])

def saveHeat3D(fileName, matrix, ask = True, normalize = True):
    """ 
    saves a 3d matrix of values between 0 and 1 to a 
    series of png files as a heat map.
    The png files can be merged into a movie file using 
    Sequimago or other movie making tools.
    """
    numberImages = matrix.shape[2]
    
    print "This method will create",  numberImages, "image files."
    if (ask):
        answer = raw_input("Is that okay?")
        if answer == "N" or answer == "n" or answer=="No" or answer=="no":
            return
    fileNumber = 0

    
    # get values for normalizing the individual slices
    maxValue = numpy.amax(matrix)
    minValue = numpy.amin(matrix)
    
    if maxValue == minValue:
        print "Sorry, the matrix is blank."
        return
    
    for f in range(numberImages):

        file = "{0}{1}.png".format(fileName, fileNumber)
        if (fileNumber < 10):
            file = "{0}00{1}.png".format(fileName,fileNumber)
        elif (fileNumber< 100):
            file = "{0}0{1}.png".format(fileName,fileNumber)
        fileNumber += 1
        print "saving", file
        
        slice = matrix[:,:,f]
        if (normalize):
            slice = (slice - minValue) / (maxValue - minValue)
        else:
            slice = matrixfix.flatten(slice, 0, 1)

        heat = toHeat(slice)
        savePng(file, heat)
