import numpy
import matrixfix
import math
import random
import time

didCancel = False

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

    # The algorithm requires calculating the midpoints and edges of 
    # all of the n-size squares before any n/2-size squares are calculated.
    # (This is because the midpoints of neighboring squares are used when
    # calculating the edges.)
    # A queue will be used to manage the squares waiting to be calculated.
    from collections import deque
    queue = deque()

    # add the whole matrix.
    queue.append([0, fractalsize-1, 0 ,fractalsize-1])

    while len(queue) > 0:
        # pop a square
        [row, maxRow, col, maxCol] = queue.popleft()

        # populate the midpoint and edges of the square
        [midRow, midCol] = diamondSquarePopulate(matrix, row, maxRow, col, maxCol,\
             roughness, perturbance, midError, edgeError, hasBorder)

        # add divided squares

        # to do: if the fractal size > size, not all of the smaller squares on the
        # bottom right would need to be calculated..  Determine which could be 
        # left out.

        if maxRow - row >= 4:
            #add top left square to the queue
            queue.append([row, midRow, col, midCol])
            #print "adding top left", row, midRow, col, midCol

            #add top right square to the queue
            queue.append([row, midRow, midCol, maxCol])
            #print "adding top right", row, midRow, midCol, maxCol

            #add bottom left square to the queue
            queue.append([midRow, maxRow, col, midCol])
            #print "adding bottom left", midRow, maxRow, col, midCol

            #add bottom right square to the queue
            queue.append([midRow, maxRow, midCol, maxCol])
            #print "adding bottom right", midRow, maxRow, midCol, maxCol


    #print "result mean =", matrix.mean(), "result std = ", matrix.std()

    print "elapsed seconds =", time.time() - start	
    # return the requested size
    return matrix[0:size, 0:size]

def diamondSquarePopulate(matrix, row, maxRow, col, maxCol, roughness, perturbance,\
                          midError, edgeError, hasBorder):
    """
    Internal method
    Populate a square using the diamond square algorithm.

    This function is internal to diamondSquareFractal().

    1. Find a noise level for this size square which includes the overall roughness
    input and a perturbance factor that is based on perturbance input and the 
    size of the square.
    2. The center value is found by averaging the four corners (plus an error)
    3. The edge values are found by averaging the averaging the neighboring corners
    and the neighboring center values. (plus an error).  
    Of course, if the edge is on the outer edge of the whole matrix, there won't
    be any neighboring center values to calculate.

    To make the process a bit more efficient, the bottom and right edges are 
    calculated only when the square is at the bottom or right of the whole matrix.

    The error can be turned off for the edges, mid-points, or the matrix border
    """    

    rowRange = maxRow - row + 1
    colRange = maxCol - col + 1

    #print "*** diamondSquarePopulate:", row, maxRow, rowRange, col, maxCol, colRange

    pf = perturbanceFactor(matrix.shape[0], rowRange, perturbance)
    noiseLevel = roughness * pf

    midNoise = 0
    edgeNoise = 0

    if (midError == True): midNoise = noiseLevel
    if (edgeError == True): edgeNoise = noiseLevel

    shape = matrix.shape

    midRow = row + int(rowRange / 2)
    midCol = col + int(colRange / 2)

    # do square step (center)
    centerValue = getValue(midNoise, [matrix[row, col], matrix[row, maxCol], \
                                    matrix[maxRow, col], matrix[maxRow, maxCol]])

    matrix[midRow, midCol] = centerValue
    #print "setting center ", midRow, midCol

    # do diamond step (edges)
    leftNeighborCenter = col - int(rowRange/2)
    topNeighborCenter = row -  int(rowRange/2)    

    # always do the left side
    if hasBorder and 0 == col:
        matrix[midRow, col] = (matrix[row, col] + matrix[maxRow, col]) / 2.0
    else:
        values = [matrix[row, col], matrix[maxRow, col], centerValue]
        if leftNeighborCenter >= 0:
            values.append(matrix[midRow, leftNeighborCenter])
        matrix[midRow, col] = getValue(edgeNoise, values)
    #print "setting left", midRow, col

    # only do the right side if we are on the right edge
    if maxCol == shape[0] - 1:
        if (hasBorder):
            matrix[midRow, maxCol] = (matrix[row, maxCol] +
                                      matrix[maxRow, maxCol]) / 2.0
        else:
            matrix[midRow, maxCol] =  getValue(edgeNoise,\
                                           [matrix[row, maxCol],\
                                            matrix[maxRow, maxCol], \
                                            centerValue])
        #print "setting right", midRow, maxCol


    # always do the top
    if hasBorder and 0 == row:
        matrix[row, midCol] = (matrix[row, col] + matrix[row, maxCol]) /2.0
    else:
        values = [matrix[row, col], matrix[row, maxCol], centerValue]
        if topNeighborCenter >= 0:
            values.append(matrix[topNeighborCenter, midCol])
        matrix[row, midCol] = getValue(edgeNoise, values)
    #print "setting top", row, midCol

    # only do the bottom side if we are on the bottom edge
    if maxRow == shape[1] - 1:
        if (hasBorder):
             matrix[maxRow, midCol] = (matrix[maxRow, col] +
                                       matrix[maxRow, maxCol]) / 2.0
        else:
            matrix[maxRow, midCol] = getValue(edgeNoise, \
                                        [matrix[maxRow, col],\
                                        matrix[maxRow, maxCol], \
                                        centerValue])
        #print "setting bottom", maxRow, midCol

    #printAllowCancel(matrix)
    return [midRow, midCol]

def double(matrix, roughness, perturbance):
    """
    Internal method
    Double is used by the zoom module to expand a fractal.
     
    Doubles the size of a fractal by expanding it to a larger matrix,
    and using the populate method to fill in the missing cells
    """ 
    size = matrix.shape[0]

    result = matrixfix.expand(matrix)

    for i in range(size):
        for j in range(size):
            row = i * 2
            col = j * 2
            diamondSquarePopulate(result, row, row+2, col, col+2, roughness, perturbance,\
            True, True, False) 
    return result

def midpointDisplacementFractal(size, roughness = .5, perturbance = .5,\
                         cornerValues = None, edgeError = True, midError = True, 
                         hasBorder = False):
    """
    Create a plasma function using the midpoiont displacement algorithm.

    This returns a square matrix of values between 0 and 1.
    This algorithm produces a lower quality fractal than the 
    diamond square algorithm.

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

    fractalsize = int(math.pow(2, math.ceil(math.log(size-1, 2)))) + 1 
    
    matrix = numpy.zeros((fractalsize, fractalsize))
    
    if None == cornerValues:
        corners = []
    elif isinstance(cornerValues, list):
        corners = cornerValues
    else:
        corners = [cornerValues]

    applyCornerValues(matrix, corners, roughness)

    midpointDisplacementPopulate(matrix, 0, fractalsize-1, 0, fractalsize-1, roughness, 
        perturbance, edgeError, midError, hasBorder)

    return matrix[0:size, 0:size]

def midpointDisplacementPopulate(matrix, row, maxRow, col, maxCol, 
                                 roughness, perturbance,\
                                 edgeError, midError, hasBorder):
    """ 
    Internal method
    Populate a square using the midpoint displacement algorithm.

    This is an iterative function and internal to midpointDisplacementFractal().

    1. Find a noise level for this size square which includes the overall roughness
    input and a perturbance factor that is based on perturbance input and the 
    size of the square.
    2. The edge values are found by averaging the neighboring corners (plus an error)
    3. The center value is found by averaging the four corners (plus an error)
    4. The square is divided into 4 smaller squares, and this function is called
    for each.  (until the squares are less than 3x3)

    To make the process a bit more efficient, the top and left edges are 
    calculated only when the square is at the top or left of the whole matrix.

    The error can be turned off for the edges, mid-points, or the matrix border
    """

    rowRange = maxRow - row + 1
    colRange = maxCol - col + 1

    if (rowRange != colRange):
        print("Sorry, matrix is not square")
    if rowRange <= 2: return

    shape = matrix.shape

    pf = perturbanceFactor(shape[0], rowRange, perturbance)
    noiseLevel = roughness * pf

    midNoise = 0
    edgeNoise = 0

    if (midError == True): midNoise = noiseLevel
    if (edgeError == True): edgeNoise = noiseLevel

    midRow = row + int(rowRange / 2)
    midCol = col + int(colRange / 2)

    # only do the left side if we are on the left edge
    if col == 0 :
        if hasBorder:
            matrix[midRow, col] =\
                (matrix[row, col] + matrix[maxRow, col]) / 2.0 
        else:   
            matrix[midRow, col] =\
                getValue(edgeNoise, [matrix[row, col], matrix[maxRow, col]])
        #print "setting left", midRow, col
    
    # always do the right side
    if hasBorder and maxCol == shape[1]-1:
        matrix[midRow, maxCol] = (matrix[row, maxCol] + matrix[maxRow, maxCol]) / 2.0
    else:
        matrix[midRow, maxCol] =\
            getValue(edgeNoise, [matrix[row, maxCol], matrix[maxRow, maxCol]])
    #print "setting right", midRow, maxCol
    
    # only do the top if we are at the top edge
    if row == 0 :
        if hasBorder:
            matrix[row, midCol] =\
                (matrix[row, col] + matrix[row, maxCol]) / 2.0
        else:
            matrix[row, midCol] =\
                getValue(edgeNoise, [matrix[row, col], matrix[row, maxCol]])
        #print "setting top", row, midCol
    
    # always do the bottom
    if hasBorder and maxRow == shape[0]-1:
        matrix[maxRow, midCol] = (matrix[maxRow, col] + matrix[maxRow, maxCol]) / 2.0
    else:
        matrix[maxRow, midCol] =\
            getValue(edgeNoise, [matrix[maxRow, col], matrix[maxRow, maxCol]])
    
    
    # do center
    values = [matrix[row, col], matrix[row, maxCol], \
              matrix[maxRow, col], matrix[maxRow, maxCol]]
    matrix[midRow, midCol] = getValue(midNoise, values)
            
    #printAllowCancel(matrix)
    
    midpointDisplacementPopulate(matrix, row, midRow, col, midCol, \
                                 roughness, perturbance, 
                                 edgeError, midError, hasBorder)
    midpointDisplacementPopulate(matrix, row, midRow, midCol, maxCol, \
                                 roughness, perturbance, 
                                 edgeError, midError, hasBorder)
    midpointDisplacementPopulate(matrix, midRow, maxRow, col, midCol, \
                                 roughness, perturbance,
                                 edgeError, midError, hasBorder)
    midpointDisplacementPopulate(matrix, midRow, maxRow, midCol, maxCol, \
                                 roughness, perturbance,
                                 edgeError, midError, hasBorder)
    
def applyCornerValues(matrix, cornerValues, roughness):
    """ 
    Internal method
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
    Internal method
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
    Internal method
    Calculate a single cell in the fractal.
    
    Finds an average value with an error.
    
    Keyword arguments:
    values: list of values to be averaged
    noise level: the proportion of the result that should be 
    randomized. 
    """
    
    randomValue = random.random()
    
    averageValue = sum(values)/len(values)
    
    result = (noiseLevel * randomValue) + ((1 - noiseLevel) * averageValue)
    
    return result

# for debugging
def printAllowCancel(matrix):
    
    newMatrix = around(matrix, 2)
    print newMatrix
        
    response = raw_input('ctl_c to stop >')

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
    
    matrix = zeros((size, size))
    
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

