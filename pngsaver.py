from numpy import *
import png
import matrixfix

def toHeatOld(matrix, levels = [.9, .8, 1]):
    newMatrix = zeros((matrix.shape[0], matrix.shape[1] * 3))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]): 
            red = green = blue = 0
            a = matrix[i, j] * 20
            if a < 5:
                red = 0
                green = 0
                blue = a
            elif a < 10:
                red = 0
                green = a - 5
                blue = 5
            elif a < 15:
                red = a-10
                green = 5
                blue = 15 - a
            else:
                red = 5
                green = 20-a
                blue = 0
                
            if red<0 or green <0 or blue<0:
                print "********", i, j, matrix[i, j], red, green, blue
            k = j*3
            newMatrix[i, k] = red * 51 * levels[0]
            newMatrix[i, k+1] = green * 51 * levels[1]
            newMatrix[i, k+2] = blue * 51 * levels[2]
    
    return newMatrix.astype(int)    
    
def toHeat(matrix):
    cosinevector = vectorize(getcosine)
    expandedMatrix = (matrix * .75) + .25
    red = cosinevector(expandedMatrix)
    green = cosinevector(expandedMatrix + .3)
    blue = cosinevector(expandedMatrix + .5)
    
    return mergeColors(red, green, blue)
    
def getcosine(x):
    rad = (x * 2 * math.pi)
    result = cos(rad)
    return result
    
def toGradient(matrix, fromColor, toColor):
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
    
    red = (redValues * 255).astype(int)
    green = (greenValues * 255).astype(int)
    blue = (blueValues * 255).astype(int)

    rows = red.shape[0]

    colors = 3
    if (alphaValues != None):
        alpha = (alphaValues * 255).astype(int)
        colors = 4
    colorMatrix = zeros((rows, red.shape[1] * colors))
    
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

    pngfile = open(filename, 'wb')
    height = matrix.shape[0]
    width = matrix.shape[1] / 3
    if (hasAlpha):
        width  = matrix.shape[1] / 4
    
    writer = png.Writer(height, width, alpha = hasAlpha)
    writer.write(pngfile, matrix)
    pngfile.close()
   
def saveGradient(filename, matrix, fromColor, toColor):

    color = toGradient(matrix, fromColor, toColor)
    savePng(filename, color)

    
def saveHeat(filename, matrix):

    heat = toHeat(matrixfix.normalize(matrix))
    savePng(filename, heat)
    
def saveColors(filename, redMatrix, greenMatrix, blueMatrix, alphaMatrix = None):

    if (alphaMatrix == None):
        merged = mergeColors(redMatrix, greenMatrix, blueMatrix)
    else:
        merged = mergeColors(redMatrix, greenMatrix, blueMatrix, alphaMatrix)
        
    savePng(filename, merged, alphaMatrix != None)

