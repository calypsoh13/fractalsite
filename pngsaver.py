import numpy
import png
import matrixfix
import math
import time
    
def toHeat(matrix):
    """
    creates a heat map from an array of normalized values (range 0 to 1) 
    """
    
    gradient = CosGradient([0,0,0])
    gradient.addStop([0,0,255], .3)
    gradient.addStop([0,255,0], .6)
    gradient.addStop([255,0,0], .9)
    
    return gradient.apply((matrix * 255).astype(int))
    
def toGradient(matrix, fromColor, toColor):
    """
    apples a gradient to a matrix of values between 0 and 1
    """
    import plasma
    
    rgbOffset = [fromColor[0]/float(255), fromColor[1]/float(255), fromColor[2]/float(255)]
    rgbSlope = [toColor[0]/float(255) - rgbOffset[0], 
                 toColor[1]/float(255) - rgbOffset[1], 
                 toColor[2]/float(255) - rgbOffset[2]]
    
    alphaOffset = 1
    alphaSlope = 0
    hasAlpha = False
    
    if len(fromColor) > 3:
        alphaOffset = fromColor[3]/float(255)
        alphaSlope = 1 - alphaOffset
        hasAlpha = True
        
    if len(toColor) > 3: 
        alphaSlope = toColor[3]/float(255) - alphaOffset
        hasAlpha = True
    
    red = matrix * rgbSlope[0] + rgbOffset[0]
    green = matrix * rgbSlope[1] + rgbOffset[1]
    blue = matrix * rgbSlope[2] + rgbOffset[2]
    
    if hasAlpha:
        alpha = matrix * alphaSlope + alphaOffset
        colorMatrix = mergeColors(red, green, blue, alpha)
    
    else:
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

    colors = 3
    if (alphaValues != None):
        alpha = (alphaValues * 255).astype(int)
        colors = 4
    colorMatrix = numpy.zeros((red.shape[0], red.shape[1] * colors))
    
    colorMatrix[:, 0::colors] = red
    colorMatrix[:, 1::colors] = green
    colorMatrix[:, 2::colors] = blue
    
    if (alphaValues != None):
        colorMatrix[:, 3::4] = alpha
    
    colorMatrix = numpy.clip(colorMatrix, 0, 255)
    colorMatrix =  colorMatrix.astype(int)
    return colorMatrix
    
def savePng(filename, matrix, hasAlpha = False):
    """
    saves an array to a png file.
    """
    
    pngfile = open(filename, 'wb')
    height = matrix.shape[0]
    width = matrix.shape[1] / 3
    if (hasAlpha):
        width  = matrix.shape[1] / 4
    writer = png.Writer(width, height, alpha = hasAlpha)
    writer.write(pngfile, matrix)
    pngfile.close()
   
def saveCosGradient(filename, matrix, cosGradient):
    """
    saves a matrix of values between 0 and 1 to a 
    png with a colors defined by the CosGradient object.
    """
    intMatrix = (matrix * 255).astype(int)
    
    color = cosGradient.apply(intMatrix)
    
    savePng(filename, color, cosGradient.colors > 3)
    

def saveGradient(filename, matrix, fromColor, toColor):
    """ 
    saves a matrix of values between 0 and 1 to a 
    png with a given gradient.
    """
    color = toGradient(matrix, fromColor, toColor)
    
    hasAlpha = False
    if len(fromColor) > 3 or len(toColor) > 3:
        hasAlpha = True
        
    savePng(filename, color, hasAlpha)

    
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
            slice = numpy.clip(slice, 0, 1)

        heat = toHeat(slice)
        savePng(file, heat)

class CosGradient:

    def __init__(self, fromColor = None, toColor = None):
        self.stops = dict()
        self.gradient = numpy.zeros((255, 4)) - 1
        self.colors = 3
        self.isCosine = True
        
        if None != fromColor:
            if len(fromColor) > 3:
                color = [fromColor[0], fromColor[1], fromColor[2], fromColor[3]]
                self.colors = 4
            else:
                color = [fromColor[0], fromColor[1], fromColor[2], 255]
            self.stops[0] = color
            
        if None != toColor:
            if len(toColor) > 3:
                color = [toColor[0], toColor[1], toColor[2], toColor[3]]
                self.colors = 4
            else:
                color = [toColor[0], toColor[1], toColor[2], 255]
            self.stops[255] = color
    
    def addStop(self, color, location):
        key = int(255 * location)
        if len(color) > 3:
            c = [color[0], color[1], color[2], color[3]]
            self.colors = 4
        else:
            c = [color[0], color[1], color[2], 255]
        self.stops[key] = c
        self.prep()
        
    def setCosine(self, isCosine):
        self.isCosine = isCosine
        self.prep()
            
    def prep(self):
        self.gradient = numpy.zeros((256, 4)) +.5
        if len(self.stops) == 0:
            return
        lastloc = -1;
        for key in sorted(self.stops.iterkeys()):
            self.gradient[key] = self.stops[key]
            if lastloc < 0:
                for i in range(key):
                    self.gradient[i] = self.stops[key]
            else:
                for i in range(lastloc + 1, key):
                    if self.isCosine:
                        self.gradient[i] = self.getCosInterpColor(lastloc, key, i)
                    else:
                        self.gradient[i] = self.getAverageColor(lastloc, key, i)
            lastloc = key
        
        if lastloc < 255:
            for i in range(lastloc + 1, 256):
                self.gradient[i] = self.stops[lastloc]
                
        self.gradient = self.gradient.astype(int)
    
    def getAverageColor(self, index1, index2, i):
        color1 = self.gradient[index1]
        color2 = self.gradient[index2]
        weight1 = (i - index1)/float(index2 - index1)
        weight2 = (index2 - i)/float(index2 - index1)
        result = (color1 * weight2 + color2 * weight1).astype(int)
        return result;
    
    def getCosInterpColor(self, index1, index2, i):
        color1 = self.gradient[index1]
        color2 = self.gradient[index2]
        mu = (i - index1)/float(index2 - index1)
        mu2 = (1 - math.cos(mu * math.pi))/float(2)
        result = (color1 * (1-mu2)) + (color2 * mu2)
        return result;
    
    def apply(self, matrix):
        """ 
        the matrix should be in the range of 0 to 255 prior
        """
        colorMatrix = self.gradient[matrix[:], 0:self.colors]
        return colorMatrix.reshape((matrix.shape[0], matrix.shape[1]*self.colors))

    def makeSample(self, width):
        
        valrange = numpy.arange(256).reshape((1, 256)).astype(int)
        row = self.apply(valrange)[0,:]
        result = numpy.zeros(width * 256 * self.colors).reshape((width, 256 * self.colors))
        for i in range(width):
            result[i,:] = row
        return result