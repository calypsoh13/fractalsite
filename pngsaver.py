from numpy import *
import png

def toHeat(matrix, levels = [.9, .8, 1]):
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

def toGradient(matrix, fromColor, toColor):
    
    rgbOffset = [fromColor[0]/float(255), fromColor[1]/float(255), fromColor[2]/float(255)]
    rgbSlope = [toColor[0]/float(255) - rgbOffset[0], 
                 toColor[1]/float(255) - rgbOffset[1], 
                 toColor[2]/float(255) - rgbOffset[2]]
    
    
    print "rgbSlope =", rgbSlope, "rgbOffset = ", rgbOffset
    
    shape = matrix.shape
    
    colorMatrix = zeros((shape[0], shape[1] * 3))
    
    for i in range(shape[0]):
        for j in range(shape[1]): 
            k = j * 3       
            colorMatrix[i,k] = matrix[i,j] * rgbSlope[0] + rgbOffset[0]
            colorMatrix[i, k+1] = matrix[i,j] * rgbSlope[1] + rgbOffset[1]
            colorMatrix[i, k+2] = matrix[i,j] * rgbSlope[2] + rgbOffset[2]           
                  
    colorMatrix = flatten(colorMatrix, 0, 1)

    colorMatrix = (colorMatrix * 255).astype(int)
 
    print "result mean =", colorMatrix.mean(), "result std = ", colorMatrix.std()
    return colorMatrix    

def savePng(filename, matrix):

    pngfile = open(filename, 'wb')
    writer = png.Writer(matrix.shape[0], matrix.shape[1]/3)
    writer.write(pngfile, matrix)
    pngfile.close()
   
def saveGradient(filename, matrix, fromColor, toColor):

    color = toGradient(matrix, fromColor, toColor)
    savePng(filename, color)

    
def saveHeat(filename, matrix, levels = None):

    heat = []
    if None == levels:
        heat = toHeat(matrix)
    else:
        heat = toHeat(matrix, levels)
        
    savePng(filename, heat)