import numpy
import math
import random
import time

def diamondSquareFractal(size, roughness = .5, perturbance = .5,\
                         cornerValues = None, edgeError = True, midError = True, 
                         hasBorder = False):
    """
    Create a plasma fractal using the diamond square algorithm.

    This returns a square matrix of values between 0 and 1.

    Keyword arguments:
    size: the length and width of the square matrix. 
    For best results, the size should be = 2^n+1 where n is and integer.
    (9, 17, 33, 65, etc).  
    If a size is entered that doesn't meet this criteria, a fractal will 
    be calculated for the next largest size and the function will return
    a slice of the result.
    roughness (from 0 to 1): the overall noise level 
    perturbance (from 0 to 1): the size-proportional noise level
    cornerValues: a list of initial values.  If the list contains 1 value, it's used
    for all four corners.  If it contains 2 values, the first is used for tl and br and 
    second is used for the other corners.  If it contains 4 values, they are placed at
    tl, tr, bl and br.
    edgeError: whether to apply the noise level to the edges of the fractal squares.
    midError: whether to apply the noise level to the midpoint of the fractal squares.
    (Either edgeError or midError should be true to produce some variability.)
    hasBorder: whether to ignore the noise level to the perimeter of the fractal.
    numpy.savetxt("matrix.txt", matrix) can be used to save the result as a text file
    pngsaver has routines for converting the fractal to an image. 
    """
    
    start = time.time()

    #calculate the fractal based on the next highest 2^n + 1
    fractalsize = int(math.pow(2, math.ceil(math.log(size-1, 2)))) + 1 
   
    matrix = numpy.zeros((fractalsize, fractalsize))

    if None == cornerValues :
        corners = []
    elif isinstance(cornerValues, list) :
        corners = cornerValues
    else:
        corners = [cornerValues]

    applyCornerValues(matrix, corners, roughness)

    
    matrixsize = fractalsize
    currentsize = maxindex = matrixsize-1
    
    while currentsize > 1:
    
        midsize = currentsize/2
        pf = perturbanceFactor(fractalsize, currentsize, perturbance)
        noiseLevel = roughness * pf
        borderNoise = midNoise = edgeNoise = 0
        if not hasBorder: borderNoise = noiseLevel
        if edgeError: edgeNoise = noiseLevel
        if midError: midNoise = noiseLevel
        
        #centers
        matrix[midsize::currentsize, midsize::currentsize] =\
            getValue(midNoise,\
            [matrix[0:maxindex:currentsize,0:maxindex:currentsize],\
            matrix[0:maxindex:currentsize, currentsize::currentsize],\
            matrix[currentsize::currentsize,currentsize::currentsize],\
            matrix[currentsize::currentsize, 0:maxindex:currentsize]])
            
        #left edge
        matrix[midsize::currentsize, 0] =\
            getValue(borderNoise,\
            [matrix[0:maxindex:currentsize, 0],\
            matrix[midsize::currentsize, midsize],\
            matrix[currentsize::currentsize, 0]])
            
        #right edge
        matrix[midsize::currentsize,maxindex] =\
            getValue(borderNoise,\
            [matrix[0:maxindex:currentsize, maxindex],\
            matrix[midsize::currentsize, maxindex-midsize],\
            matrix[currentsize::currentsize, maxindex]])
        
        #top edge
        matrix[0, midsize::currentsize] =\
            getValue(borderNoise,\
            [matrix[0, 0:maxindex:currentsize],\
            matrix[midsize, midsize::currentsize],\
            matrix[0, currentsize::currentsize]])
        
        #bottom edge
        matrix[maxindex, midsize::currentsize] =\
            getValue(borderNoise,\
            [matrix[maxindex, 0:maxindex:currentsize],\
            matrix[maxindex-midsize, midsize::currentsize],\
            matrix[maxindex, currentsize::currentsize]])
        
        if (currentsize < maxindex):
            
            limit = maxindex - midsize
            
            matrix[midsize::currentsize, currentsize:limit:currentsize] =\
                getValue(edgeNoise,
                [matrix[0:maxindex:currentsize, currentsize:limit:currentsize],\
                matrix[currentsize::currentsize,currentsize:limit:currentsize],\
                matrix[midsize::currentsize,midsize:limit:currentsize],\
                matrix[midsize::currentsize,currentsize+midsize::currentsize]])
            
            matrix[currentsize:limit:currentsize, midsize::currentsize] =\
                getValue(edgeNoise,
                [matrix[currentsize:limit:currentsize, 0:maxindex:currentsize],\
                matrix[currentsize:limit:currentsize, currentsize::currentsize],\
                matrix[midsize:limit:currentsize, midsize::currentsize],\
                matrix[currentsize+midsize::currentsize, midsize::currentsize]])
        
        #decrement 
        currentsize = currentsize/2
    print "elapsed seconds =", time.time() - start
    return matrix
    
def applyCornerValues(matrix, cornerValues, roughness):
    """ 
    Determine number of corner values available and place them in the matrix.
    
    1 value: all four corners
    2 values: value 0 is placed in the top left and bottom right.
    4 values: top left, top right, bottom left, bottom right.
    0 values: the corners are given a random value adjusted for roughness
    """
    
    size = matrix.shape[0]
    
    #allow the user to pass in 4, 2, or 1 value for the corners
    if len(cornerValues) > 3:
        matrix[0, 0] = cornerValues[0]
        matrix[0, size-1] = cornerValues[1]
        matrix[size-1, 0] = cornerValues[2]
        matrix[size-1, size-1] = cornerValues[3]
    elif len(cornerValues) > 1:
        matrix[0, 0] = cornerValues[0]
        matrix[0, size-1] = cornerValues[1]
        matrix[size-1, 0] = cornerValues[1]
        matrix[size-1, size-1] = cornerValues[0]
    elif len(cornerValues) == 1:
        matrix[0, 0] = cornerValues[0]
        matrix[0, size-1] = cornerValues[0]
        matrix[size-1, 0] = cornerValues[0]
        matrix[size-1, size-1] = cornerValues[0]
    else:
        matrix[0, 0] = random.random() * roughness
        matrix[0, size-1] = random.random() * roughness
        matrix[size-1, 0] = random.random() * roughness
        matrix[size-1, size-1] = random.random() * roughness
    
    
def perturbanceFactor(lenWhole, lenPart, perturbance):
    """ 
    Return a perturbance factor based on matrix properties.
    
    We want the error for small squares to be smaller than the error
    for large squares.  This function calculates a perturbance
    factor based on the size of the whole matrix, the size of the
    current square, and a peturbance user input.
    """
    k = 1 - perturbance
    return lenPart ** k / lenWhole ** k
    
def getValue(noiseLevel, values):
    """ 
    Calculate a single cell in the fractal.
    
    Finds an average value with an error.
    
    Keyword arguments:
    values: list of values to be averaged
    noise level: the proportion of the result that should be 
    randomized. 
    """
    averageValue = numpy.zeros(values[0].shape)
    
    for value in values:
        averageValue = averageValue + value
    averageValue = averageValue / float(len(values))
    
    randomValue = numpy.random.random(values[0].size).reshape(values[0].shape)
    
    result = (noiseLevel * randomValue) + ((1 - noiseLevel) * averageValue)
    
    return result

def gaussianFilter(size, points): 
    """
    Create a gaussian filter that can be applied to a matrix.
    
    Applying this filter will give a roundish frame to your fractal.
    
    Keyword arguments:
    size: size of the matrix
    points: list of points, each of which should be a tuple 
    including x, y, sigmaX and sigmaY
    sigmas are used to make the frame larger
    in the x and y dimension
    use numpy.multiply to apply the filter to a matrix.
    """
    
    matrix = numpy.zeros((size, size))
    
    for point in points:
        x0 = point[0]
        y0 = point[1]
        x2SigmaSquared = pow(point[2] * size/4, 2) * 2
        y2SigmaSquared = pow(point[3] * size/4, 2) * 2
        tempMatrix = numpy.zeros((size, size))
        for x in range(0, size):
            for y in range(0, size):
                tempMatrix[y, x] = math.exp(-1 * \
                    (math.pow(x-x0, 2)/x2SigmaSquared + math.pow(y-y0, 2)/y2SigmaSquared))
                      
        matrix = numpy.add(matrix, tempMatrix)
              
    matrix = matrixfix.flatten(matrix, 0, 1)
    
    return matrix

# for debugging
def printAllowCancel(matrix):
    
    #print matrix.astype(int)
        
    #response = raw_input('ctl_c to stop >')
    return
