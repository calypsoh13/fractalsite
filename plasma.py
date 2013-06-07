from numpy import *
import png

didCancel = False

# plasma function
# returns a square matrix of values between 0 and 1
# for the given size, roughness (from 0 to 1), and a list of initial values.
# Note: The algoritm only works for sizes = 2^n+1 (9, 17, 33, 65, etc.)
# other sizes will give results with unwanted vertical and horizontal features. 
def diamondSquareFractal(size, roughness, cornerValues = None):
    
    #print "size = ", size, "roughness =", roughness, "corner values =", cornerValues

    matrix = zeros((size, size))
    
    if None == cornerValues:
        pass
        matrix[0, 0] = random.random()
        matrix[0, size-1] = random.random()
        matrix[size-1, 0] = random.random()
        matrix[size-1, size-1] = random.random()
    else:
        try:
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
        except TypeError:
            matrix[0, 0] = cornerValues
            matrix[0, size-1] = cornerValues
            matrix[size-1, 0] = cornerValues
            matrix[size-1, size-1] = cornerValues

    #print matrix[0, 0], matrix[0, size-1], matrix[size-1, 0],

    from collections import deque
    queue = deque()
    queue.append([0, size-1, 0 ,size-1])

    while len(queue) > 0:

        [row, maxRow, col, maxCol] = queue.popleft()

        
        [midRow, midCol] = populate(matrix, row, maxRow, col, maxCol, roughness)

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

# populate square 
def populate(matrix, row, maxRow, col, maxCol, roughness):
    
    rowRange = maxRow - row + 1
    colRange = maxCol - col + 1
    
    #print "*** populate:", row, maxRow, rowRange, col, maxCol, colRange
    
    sizeFactor = math.log(rowRange, 2)/ math.log(matrix.shape[0],2)
    noiseLevel = roughness * sizeFactor
    
    shape = matrix.shape
    
    midRow = row + int(rowRange / 2)
    midCol = col + int(colRange / 2)
    
    # do diamond step
    
    diamondValue = getValue(noiseLevel, [matrix[row, col], matrix[row, maxCol], \
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
        matrix[midRow, col] = getValue(noiseLevel, values)
        #print "setting left", midRow, col
        
        # only do the right side if we are on the right edge
        if maxCol == shape[0] - 1:
            matrix[midRow, maxCol] =  getValue(noiseLevel,\
                                               [matrix[row, maxCol], matrix[maxRow, maxCol], \
                                                diamondValue])
            #print "setting right", midRow, maxCol
    
    # check whether there's an empty column
    if midCol > col and midCol < maxCol:
        # always do the top
        values = [matrix[row, col], matrix[row, maxCol], diamondValue]
        if topMost >= 0:
            values.append(matrix[topMost, midCol])
        matrix[row, midCol] = getValue(noiseLevel, values)
        #print "setting top", row, midCol
        
        # only do the bottom side if we are on the bottom edge
        if maxRow == shape[1] - 1:
            matrix[maxRow, midCol] = getValue(noiseLevel, \
                                              [matrix[maxRow, col], matrix[maxRow, maxCol], \
                                               diamondValue])
            #print "setting bottom", maxRow, midCol
            
        #printAllowCancel(matrix)
    return [midRow, midCol]

def getValue(noiseLevel, values):
    
    randomValue = random.random()
    
    averageValue = sum(values)/len(values)
    
    result = (noiseLevel * randomValue) + ((1 - noiseLevel) * averageValue)
    
    return result

def printAllowCancel(matrix):
    
    newMatrix = around(matrix, 2)
    print newMatrix
        
    response = raw_input('ctl_c to stop >')

#use numpy.savetxt("matrix.txt", matrix) to save
    

