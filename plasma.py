from numpy import *
import png

didCancel = False

# plasma function using the diamond square algorithm
# returns a square matrix of values between 0 and 1
# size: the length and width of the square matrix. 
# For best results, the size should be = 2^n+1 where n is and integer.
# (9, 17, 33, 65, etc).  Other sizes will give results with unwanted 
# vertical and horizontal features. 
# roughness (from 0 to 1): the overall noise level 
# perturbance (from 0 to 1): the size-proportional noise level
# cornerValues: a list of initial values.  If the list contains 1 value, it's used
# for all four corners.  If it contains 2 values, the first is used for tl and br and 
# second is used for the other corners.  If it contains 4 values, they are placed at
# tl, tr, bl and br.
# edgeError: whether to apply the noise level to the edges of the fractal squares.
# midError: whether to apply the noise level to the midpoint of the fractal squares. 
# (Either edgeError or midError should be true to produce some variability.)

#use numpy.savetxt("matrix.txt", matrix) to save

def diamondSquareFractal(size, roughness = .5, perturbance = .5,\
                         cornerValues = None, edgeError = True, midError = True):

    matrix = zeros((size, size))
    
    if None == cornerValues :
        corners = []
    elif isinstance(cornerValues, list) :
        corners = cornerValues
    else:
        corners = [cornerValues]
    
    applyCornerValues(matrix, corners, roughness)
    
    from collections import deque
    queue = deque()
    queue.append([0, size-1, 0 ,size-1])

    while len(queue) > 0:

        [row, maxRow, col, maxCol] = queue.popleft()

        
        [midRow, midCol] = diamondSquarePopulate(matrix, row, maxRow, col, maxCol,\
             roughness, perturbance, midError, edgeError)

        if midRow - row >= 2 or midCol - col >= 2:
                #add top left square
                queue.append([row, midRow, col, midCol])
                #print "adding top left", row, midRow, col, midCol
        if midRow - row >= 2 or maxCol - midCol >=2:
                #add top right square
                queue.append([row, midRow, midCol, maxCol])
                #print "adding top right", row, midRow, midCol, maxCol
        if maxRow - midRow >=2 or midCol - col >= 2:
                #add bottom left square
                queue.append([midRow, maxRow, col, midCol])
                #print "adding bottom left", midRow, maxRow, col, midCol
        if maxRow - midRow >=2 or maxCol - midCol >=2:
                #add bottom right square
                queue.append([midRow, maxRow, midCol, maxCol])
                #print "adding bottom right", midRow, maxRow, midCol, maxCol


    print "result mean =", matrix.mean(), "result std = ", matrix.std()

    return matrix

# diamondSquarePopulate inner method to populate a square 
def diamondSquarePopulate(matrix, row, maxRow, col, maxCol, roughness, perturbance,\
                          midError, edgeError):
    
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
    
    # do diamond step
    
    diamondValue = getValue(midNoise, [matrix[row, col], matrix[row, maxCol], \
                                    matrix[maxRow, col], matrix[maxRow, maxCol]])
    
    if (midRow > row and midRow < maxRow) and (midCol > col and midCol < maxCol):
        matrix[midRow, midCol] = diamondValue
        #print "setting center ", midRow, midCol
    
    # do square step
    
    leftMost = col - (midCol - col)
    topMost = row - (midRow - row)
    
    # check whether there's an empty row
    if midRow > row and midRow < maxRow:
        # always do the left side
        values = [matrix[row, col], matrix[maxRow, col], diamondValue]
        if leftMost >= 0:
            values.append(matrix[midRow, leftMost])
        matrix[midRow, col] = getValue(edgeNoise, values)
        #print "setting left", midRow, col
        
        # only do the right side if we are on the right edge
        if maxCol == shape[0] - 1:
            matrix[midRow, maxCol] =  getValue(edgeNoise,\
                                               [matrix[row, maxCol],\
                                                matrix[maxRow, maxCol], \
                                                diamondValue])
            #print "setting right", midRow, maxCol
    
    # check whether there's an empty column
    if midCol > col and midCol < maxCol:
        # always do the top
        values = [matrix[row, col], matrix[row, maxCol], diamondValue]
        if topMost >= 0:
            values.append(matrix[topMost, midCol])
        matrix[row, midCol] = getValue(edgeNoise, values)
        #print "setting top", row, midCol
        
        # only do the bottom side if we are on the bottom edge
        if maxRow == shape[1] - 1:
            matrix[maxRow, midCol] = getValue(edgeNoise, \
                                    [matrix[maxRow, col],\
                                    matrix[maxRow, maxCol], \
                                    diamondValue])
            #print "setting bottom", maxRow, midCol
            
        #printAllowCancel(matrix)
    return [midRow, midCol]

# plasma function using the midpoint displacement algorithm
def midpointDisplacementFractal(size, roughness = .5, perturbance = .5,\
                         cornerValues = None, edgeError = True, midError = True):
                         
   #print "size = ", size, "roughness =", roughness, "corner values =", cornerValues

    matrix = zeros((size, size))
    
    if None == cornerValues:
        corners = []
    elif isinstance(cornerValues, list):
        corners = cornerValues
    else:
        corners = [cornerValues]
    
    applyCornerValues(matrix, corners, roughness)
    
    midpointDisplacementPopulate(matrix, 0, size-1, 0, size-1, roughness, perturbance, 
                                 edgeError, midError)
    
    return matrix
    
def midpointDisplacementPopulate(matrix, row, maxRow, col, maxCol, 
                                 roughness, perturbance,\
                                 edgeError, midError):
    
    rowRange = maxRow - row + 1
    colRange = maxCol - col + 1

    if rowRange <= 2 and colRange <= 2: return
           
    shape = matrix.shape
    
    pf = perturbanceFactor(shape[0], rowRange, perturbance)
    noiseLevel = roughness * pf
    
    midNoise = 0
    edgeNoise = 0
    
    if (midError == True): midNoise = noiseLevel
    if (edgeError == True): edgeNoise = noiseLevel
    
    midRow = row + int(rowRange / 2)
    midCol = col + int(colRange / 2)
    
    # check whether there's an empty row
    if midRow > row and midRow < maxRow:
        # only do the left side if we are on the left edge
        if col == 0 :
            matrix[midRow, col] =\
                getValue(edgeNoise, [matrix[row, col], matrix[maxRow, col]])
            #print "setting left", midRow, col
        
        # always do the right side
        matrix[midRow, maxCol] =\
            getValue(edgeNoise, [matrix[row, maxCol], matrix[maxRow, maxCol]])
        #print "setting right", midRow, maxCol
    
    # check whether there's an empty column
    if midCol > col and midCol < maxCol:
        # only do the top if we are at the top edge
        if row == 0 :
            matrix[row, midCol] =\
                getValue(edgeNoise, [matrix[row, col], matrix[row, maxCol]])
            #print "setting top", row, midCol
        
        # always do the bottom
        matrix[maxRow, midCol] =\
            getValue(edgeNoise, [matrix[maxRow, col], matrix[maxRow, maxCol]])

    
    if (midRow > row) and (midRow < maxRow) and (midCol > col) and (midCol < maxCol):
        values = [matrix[row, col], matrix[row, maxCol], \
                  matrix[maxRow, col], matrix[maxRow, maxCol]]
        matrix[midRow, midCol] = getValue(midNoise, values)
            
    #printAllowCancel(matrix)
    
    midpointDisplacementPopulate(matrix, row, midRow, col, midCol, \
                                 roughness, perturbance, 
                                 edgeError, midError)
    midpointDisplacementPopulate(matrix, row, midRow, midCol, maxCol, \
                                 roughness, perturbance, 
                                 edgeError, midError)
    midpointDisplacementPopulate(matrix, midRow, maxRow, col, midCol, \
                                 roughness, perturbance,
                                 edgeError, midError)
    midpointDisplacementPopulate(matrix, midRow, maxRow, midCol, maxCol, \
                                 roughness, perturbance,
                                 edgeError, midError)
             
def applyCornerValues(matrix, cornerValues, roughness):

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
    k = 1 - perturbance
    return lenPart ** k / lenWhole ** k
    

def getValue(noiseLevel, values):
        
    randomValue = random.random()
    
    averageValue = sum(values)/len(values)
    
    result = (noiseLevel * randomValue) + ((1 - noiseLevel) * averageValue)
    
    return result

def printAllowCancel(matrix):
    
    newMatrix = around(matrix, 2)
    print newMatrix
        
    response = raw_input('ctl_c to stop >')


    

