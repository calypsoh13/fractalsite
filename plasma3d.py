import numpy
import math
import random
import matrixfix

def diamondSquareFractal3D(size, roughness = .5, perturbance = .5):
    """
    Create a plasma fractal using the diamond square algorithm.

    This returns a cube matrix of values between 0 and 1.

    Keyword arguments:
    size: the length and width of the square matrix. 
    For best results, the size should be = 2^n+1 where n is and integer.
    (9, 17, 33, 65, etc).  
    If a size is entered that doesn't meet this criteria, a fractal will 
    be calculated for the next largest size and the function will return
    a slice of the result.
    roughness (from 0 to 1): the overall noise level 
    perturbance (from 0 to 1): the size-proportional noise level
    numpy.savetxt("matrix.txt", matrix) can be used to save the result as a text file
    pngsaver has routines for converting the fractal to an image. 
    """
    
    #calculate the fractal based on the next highest 2^n + 1
    n = math.log(size-1, 2)
    if n != float(int(n)):
        print "The size is not valid, choose a side that is a power of 2 + 1."
        print "65, 129, 257, 513, 1025, etc."
        return
   
    matrix = numpy.zeros((size, size, size)) * -100
    
    applyCornerValues(matrix, roughness)
    
    matrixsize = size
    csize = maxindex = matrixsize-1
    
    while csize > 1:
    
        midsize = csize/2
        pf = perturbanceFactor(size, csize, perturbance)
        noiseLevel = roughness * pf
        
        #centers
        matrix[midsize::csize, midsize::csize, midsize::csize] =\
            getValue(noiseLevel,\
            [matrix[0:maxindex:csize,0:maxindex:csize, 0:maxindex:csize],\
            matrix[0:maxindex:csize, 0:maxindex:csize, csize::csize],\
            matrix[0:maxindex:csize, csize::csize, 0:maxindex:csize],\
            matrix[0:maxindex:csize, csize::csize, csize::csize],\
            matrix[csize::csize, 0:maxindex:csize, 0:maxindex:csize],
            matrix[csize::csize, 0:maxindex:csize, csize::csize],
            matrix[csize::csize, csize::csize, 0:maxindex:csize],
            matrix[csize::csize, csize::csize, csize::csize]])
            
        #topmost face
        matrix[0, midsize::csize, midsize::csize] =\
            getValue(noiseLevel,\
            [matrix[0, 0:maxindex:csize, 0:maxindex:csize],\
            matrix[0, 0:maxindex:csize, csize::csize],\
            matrix[0, csize::csize, 0:maxindex:csize],\
            matrix[0, csize::csize, csize::csize],\
            matrix[midsize, midsize::csize, midsize::csize]])
            
        #leftmost face
        matrix[midsize::csize, 0, midsize::csize] =\
            getValue(noiseLevel,\
            [matrix[0:maxindex:csize, 0, 0:maxindex:csize],\
            matrix[0:maxindex:csize, 0, csize::csize],\
            matrix[csize::csize, 0, 0:maxindex:csize],\
            matrix[csize::csize, 0, csize::csize],\
            matrix[midsize::csize, midsize, midsize::csize]])
            
        #frontmost face
        matrix[midsize::csize, midsize::csize, 0] =\
            getValue(noiseLevel,\
            [matrix[0:maxindex:csize, 0:maxindex:csize, 0],\
            matrix[0:maxindex:csize, csize::csize, 0],\
            matrix[csize::csize, 0:maxindex:csize, 0],\
            matrix[csize::csize, csize::csize, 0],\
            matrix[midsize::csize, midsize::csize, midsize]])
            
        #bottommost face
        matrix[maxindex, midsize::csize, midsize::csize] =\
            getValue(noiseLevel,\
            [matrix[maxindex, 0:maxindex:csize, 0:maxindex:csize],\
            matrix[maxindex, 0:maxindex:csize, csize::csize],\
            matrix[maxindex, csize::csize, 0:maxindex:csize],\
            matrix[maxindex, csize::csize, csize::csize],\
            matrix[maxindex - midsize, midsize::csize, midsize::csize]])
        
        #rightmost face
        matrix[midsize::csize, maxindex, midsize::csize] =\
            getValue(noiseLevel,\
            [matrix[0:maxindex:csize, maxindex, 0:maxindex:csize],\
            matrix[0:maxindex:csize, maxindex, csize::csize],\
            matrix[csize::csize, maxindex, 0:maxindex:csize],\
            matrix[csize::csize, maxindex, csize::csize],\
            matrix[midsize::csize, maxindex-midsize, midsize::csize]])
            
        #back-most face
        matrix[midsize::csize, midsize::csize, 0] =\
            getValue(noiseLevel,\
            [matrix[0:maxindex:csize, 0:maxindex:csize, maxindex],\
            matrix[0:maxindex:csize, csize::csize, maxindex],\
            matrix[csize::csize, 0:maxindex:csize, maxindex],\
            matrix[csize::csize, csize::csize, maxindex],\
            matrix[midsize::csize, midsize::csize, maxindex-midsize]])
        
        #printAllowCancel(matrix)
        
        if (csize < maxindex):
            
            limit = maxindex - midsize
            
            # top faces
            matrix[csize:limit:csize, midsize::csize, midsize::csize] =\
                getValue(noiseLevel,\
                [matrix[csize:limit:csize, 0:maxindex:csize, 0:maxindex:csize],\
                matrix[csize:limit:csize, 0:maxindex:csize, csize::csize],\
                matrix[csize:limit:csize, csize::csize, 0:maxindex:csize],\
                matrix[csize:limit:csize, csize::csize, csize::csize],\
                matrix[midsize + csize::csize, midsize::csize, midsize::csize],\
                matrix[csize - midsize:limit:csize, midsize::csize, midsize::csize]])
            
            # left faces
            matrix[midsize::csize, csize:limit:csize, midsize::csize] =\
                getValue(noiseLevel,\
                [matrix[0:maxindex:csize, csize:limit:csize, 0:maxindex:csize],\
                matrix[0:maxindex:csize, csize:limit:csize, csize::csize],\
                matrix[csize::csize, csize:limit:csize, 0:maxindex:csize],\
                matrix[csize::csize, csize:limit:csize, csize::csize],\
                matrix[midsize::csize, midsize + csize::csize, midsize::csize],\
                matrix[midsize::csize, csize - midsize:limit:csize, midsize::csize]])
            
            # front faces
            matrix[midsize::csize, midsize::csize, csize:limit:csize] =\
                getValue(noiseLevel,\
                [matrix[0:maxindex:csize, 0:maxindex:csize, csize:limit:csize],\
                matrix[0:maxindex:csize, csize::csize, csize:limit:csize],\
                matrix[csize::csize, 0:maxindex:csize, csize:limit:csize],\
                matrix[csize::csize, csize::csize, csize:limit:csize],\
                matrix[midsize::csize, midsize::csize, midsize + csize::csize],\
                matrix[midsize::csize, midsize::csize, csize-midsize:limit:csize]])
            
            # edges
            
            
            printAllowCancel(matrix)
            
            matrix[csize:limit:csize, csize:limit:csize, midsize+csize::csize] =\
                getValue(noiseLevel,\
    111            [matrix[csize:limit:csize, csize:limit:csize, csize:limit:csize],
    113            matrix[csize:limit:csize, csize:limit:csize, csize+csize::csize],
    102            matrix[csize:limit:csize, midsize:limit:csize, csize+midsize::csize],
    122            matrix[csize:limit:csize, csize+midsize::csize, csize+midsize::csize],
    012            matrix[midsize:limit:csize, csize:limit:csize, csize+midsize::csize],
    212            matrix[csize + midsize::csize, csize:limit:csize, csize+midsize::csize]])
            
            matrix[csize:limit:csize, csize+midsize::csize, midsize:limit:csize] =\
                getValue(noiseLevel,\
    111            [matrix[csize:limit:csize, csize:limit:csize, csize:limit:csize],
    122            matrix[csize:limit:csize, csize+midsize::csize, csize+midsize::csize],
    120            matrix[csize:limit:csize, csize+midsize::csize, midsize:limit:csize],
    131            matrix[csize:limit:csize, csize+csize::csize, csize:limit:csize],
    021            matrix[midsize:limit:csize, csize+midsize::csize, csize:limit:csize],
    221            matrix[csize+midsize::csize, csize+midsize::csize, csize:limit:csize]])
            
            matrix[csize+midsize::csize, csize:limit:csize, midsize:limit:csize] =\
                getValue(noiseLevel,\
    111            [matrix[csize:limit:csize, csize:limit:csize, csize:limit:csize],
    122            matrix[csize:limit:csize, csize+midsize::csize, csize+midsize::csize],
    120            matrix[csize:limit:csize, csize+midsize::csize, midsize:limit:csize],
    131            matrix[csize:limit:csize, csize+csize::csize, csize:limit:csize],
    021            matrix[midsize:limit:csize, csize+midsize::csize, csize:limit:csize],
    221            matrix[csize+midsize::csize, csize+midsize::csize, csize:limit:csize]])

        #decrement 
        csize = csize/2
    
    return matrix

""" 
these arrays include the information needed to determine the center, face and edge 
values for each cube.  See indexRef and setValue for more information.
"""
center = [[2,2,2], [1,1,1], [1,1,3], [1,3,3], [3,1,1], [3,1,3], [3,3,1], [3,3,3]]

faces = [[[1,2,2], [1,1,1], [1,3,1], [1,1,3], [1,3,3], [2,2,2], [0,2,2]],
        [[2,1,2], [1,1,1], [3,1,1], [1,1,3], [3,1,3], [2,2,2], [2,0,2]],
        [[2,2,1], [1,1,1], [3,1,1], [1,3,1], [3,3,1], [2,2,2], [2,2,0]],
        [[2,2,3], [1,1,3], [3,1,3], [1,3,3], [3,3,3], [2,2,2]],
        [[2,3,2], [1,3,1], [3,3,1], [1,3,3], [3,3,3], [2,2,2]],
        [[3,2,2], [3,1,1], [3,3,1], [3,1,3], [3,3,3], [2,2,2]]]
           
edges = [[[1,1,2], [1,1,1], [1,1,3], [1,0,2], [1,2,2], [0,1,2], [2,1,2]],
         [[1,2,1], [1,2,0], [1,2,2], [1,1,1], [1,3,1], [0,2,1], [2,2,1]],
         [[2,1,1], [2,1,0], [2,1,2], [2,0,1], [2,2,1], [1,1,1], [3,1,1]],
         [[1,2,3], [1,2,2], [1,1,3], [1,3,3], [0,2,3], [2,2,3]],
         [[1,3,2], [1,3,1], [1,3,3], [1,2,2], [0,3,2], [2,3,2]],
         [[2,1,3], [2,1,2], [2,0,3], [2,2,3], [1,1,3], [3,1,3]],
         [[2,3,1], [2,3,0], [2,3,2], [2,2,1], [1,3,1], [3,3,1]],
         [[3,1,2], [3,1,1], [3,1,3], [3,0,2], [3,2,2], [2,1,2]], 
         [[3,2,1], [3,2,0], [3,2,2], [3,1,1], [3,3,1], [2,2,1]],
         [[2,3,3], [2,3,2], [2,2,3], [1,3,3], [3,3,3]],
         [[3,2,3], [3,2,2], [3,1,3], [3,3,3], [2,2,3]],
         [[3,3,2], [3,3,1], [3,3,3], [3,2,2], [2,3,2]]]


def olddiamondSquareFractal3D(size, roughness = .5, perturbance = .5):
    """"
    Create a 3D plasma fractal using the diamond square algorithm.
    
    This returns a square 3D matrix of values between 0 and 1.

    Keyword arguments:
    size: a single value representing the length and width and height 
    of the square matrix. 
    The size must be = 2^n+1 where n is and integer (9, 17, 33, 65, etc).  

    roughness (from 0 to 1): the overall noise level 
    perturbance (from 0 to 1): the size-proportional noise level

    numpy.savetxt("matrix.txt", matrix) can be used to save the result as a text file
    pngsaver has routines for converting the fractal to an series of images. 
    """
    count = 0;
    
    #calculate the fractal based on the next highest 2^n + 1
    n = math.log(size-1, 2)
    if n != float(int(n)):
        print "The size is not valid, choose a side that is a power of 2 + 1."
        print "65, 129, 257, 513, 1025, etc."
        return
   
    matrix = numpy.zeros((size, size, size)) - 100
    total = matrix.size
    
    applyCornerValues(matrix, roughness)
    
    """
    The algorithm requires calculating the centers, faces and edges 
    in a particular order so that neighboring values will be 
    available to average:
    
    1. Calc centers of all size n cubes.
    2. for each size n cube:
        a. calc faces
        b. calc edges
        c. divide the cube into 8 cubes of size n-1.
        d. repeat from step 1 until n < 3.
    
    Subdivided cubes are populated in the following order so that a
    cube will not be populated until its top, left, and front neighbors
    are done.  Values from neighboring cubes are used to calculate 
    top, left and front faces and edges
        top. left, front
        top, left, back
        top, right, front
        bottom, left, front
        top, right, back
        bottom, left, back
        bottom, right, front
        bottom, right, back
    
    A queue will be used to manage the cubes waiting to be calculated.
    """
    
    from collections import deque
    queue = deque()
    
    # add the whole matrix.
    queue.append([0, 0 ,0 , size-1])

    # calc the center for the whole matrix
    pf = perturbanceFactor(size, size, perturbance)
    noiseLevel = roughness * pf
    indexRef = getIndexRef(0, 0, 0, size/2, size)
    setValue(matrix, center, indexRef, noiseLevel)

    while len(queue) > 0:
        # pop a square
        whatisit = queue.popleft()
        [row, col, frame, range] = whatisit

        midRange = range/2
        # populate the faces and edges of the cube
        [midRow, midCol, midFrame] = populate3D(matrix, 
            row, col, frame, midRange, roughness, perturbance)

        if midRange >= 2:
            #calc the centers for the next layer
            populateCenters(matrix, row, col, frame, midRange, roughness, perturbance)
            
            #add top left front cube to the queue 
            queue.append([row, col, frame, midRange])
            
            #add top left back cube to the queue
            queue.append([row, col, midFrame, midRange])

            #add top right front cubes to the queue
            queue.append([row, midCol, frame, midRange])

            #add bottom left front cubes to the queue
            queue.append([midRow, col, frame, midRange])
            
            #add top right back cubes to the queue 
            queue.append([row, midCol, midFrame, midRange])

            #add bottom left back cubes to the queue
            queue.append([midRow, col, midFrame, midRange])

            #add bottom right front cubes to the queue
            queue.append([midRow, midCol, frame, midRange])
            
            #add bottom right back cubes to the queue
            queue.append([midRow, midCol, midFrame, midRange])

    #print "result mean =", matrix.mean(), "result std = ", matrix.std()

    # return the requested size
    return matrix[0:size, 0:size]

def populateCenters(matrix, row, col, frame, midRange, roughness, perturbance):
    """
    Internal method
    Given a cube defined by the row, col, frame and size
    (midRange = (size-1)/2)  this method populates the centers of all
    the subdivided cubes of size = midRange-1
    """
    maxIndex = matrix.shape[0]-1
    quarterRange = midRange/2

    pf = perturbanceFactor(matrix.shape[0], midRange, perturbance)
    noiseLevel = roughness * pf

    """
    For each subdivided cube, getIndexRef is used to get the indicies, and center is used
    to determine the points that should be averaged and the point to be set.  
    setValue does the calculations.
    """
    indexRef = getIndexRef(row, col, frame, quarterRange, maxIndex)
    setValue(matrix, center, indexRef, noiseLevel)
    
    indexRef = getIndexRef(row, col, frame + midRange, quarterRange, maxIndex)
    setValue(matrix, center, indexRef, noiseLevel)
    
    indexRef = getIndexRef(row, col + midRange, frame, quarterRange, maxIndex)
    setValue(matrix, center, indexRef, noiseLevel)
    
    indexRef = getIndexRef(row + midRange, col, frame, quarterRange, maxIndex)
    setValue(matrix, center, indexRef, noiseLevel)
    
    indexRef = getIndexRef(row + midRange, col + midRange, frame, quarterRange, maxIndex)
    setValue(matrix, center, indexRef, noiseLevel)
    
    indexRef = getIndexRef(row + midRange, col, frame + midRange, quarterRange, maxIndex)
    setValue(matrix, center, indexRef, noiseLevel)
    
    indexRef = getIndexRef(row, col + midRange, frame + midRange, quarterRange, maxIndex)
    setValue(matrix, center, indexRef, noiseLevel)
    
    indexRef = getIndexRef(row + midRange, col + midRange, frame + midRange, quarterRange, maxIndex)
    setValue(matrix, center, indexRef, noiseLevel)
    

    #printAllowCancel(matrix)
    
    
def populate3D(matrix, row, col, frame, midRange, roughness, perturbance):
    """
    Internal method
    Given a cube defined by the row, col, frame and size
    (midRange = (size-1)/2)  this method populates the centers of the
    faces and edges.
    """
    maxIndex = matrix.shape[0]-1
    
    #put the actual indices appropriate for this cube into the indexRef array
    indexRef = getIndexRef(row, col, frame, midRange, maxIndex)

    pf = perturbanceFactor(matrix.shape[0], midRange * 2, perturbance)
    noiseLevel = roughness * pf
    
    populateFaces(matrix, indexRef, noiseLevel)

    populateEdges(matrix, indexRef, noiseLevel)
    
    #printAllowCancel(matrix)
    
    return [row + midRange, col + midRange, frame + midRange]

def populateFaces(matrix, indexRef, noiseLevel):
    """
    Internal method
    Populate each face in a cube defined by indexRef
    """
    for face in faces:
        setValue(matrix, face, indexRef, noiseLevel)
        
def populateEdges(matrix, indexRef, noiseLevel):
    """
    Internal method
    Populate each edge in a cube defined by indexRef
    """
    for edge in edges:
        setValue(matrix, edge, indexRef, noiseLevel)

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
    averageValue = numpy.zeros(values[0].shape)
    
    for value in values:
        averageValue = averageValue + value
        if numpy.amin(value) <= 0:
            print "zero value in ", value
            response = raw_input('ctl_c to stop >')
    averageValue = averageValue / float(len(values))
    
    randomValue = numpy.random.random(values[0].size).reshape(values[0].shape)
    
    result = (noiseLevel * randomValue) + ((1 - noiseLevel) * averageValue)
    
    return result
    
def setValue(matrix, line, indexRef, noiseLevel):
    """
    Internal method
    Calculates the value of a cell in the matrix 
    indexRef represents a cube within the matrix. 
    line[0] represents the target point within that cube. 
    line[1]...line[len(line)-1] represent the points to 
    be averaged together to get the target value.
    
    Bottom faces and edges are only populated if on the right edge of the whole matrix.
    Likewise for the right and back faces and edges.
    """
    #print "getValue for ", value, noiseLevel
    maxIndex = matrix.shape[0] - 1
    sum = 0
    summedItems = 0
    
    if line[0][0] == 3 and indexRef[3,0] < maxIndex:
        return
    if line[0][1] == 3 and indexRef[3,1] < maxIndex:
        return
    if line[0][2] == 3 and indexRef[3,2] < maxIndex:
        return
        
    for i in range(1, len(line)):
        point = line[i]
        r = indexRef[point[0],0]
        c = indexRef[point[1],1]
        f = indexRef[point[2],2]
        if r >= 0 and c >= 0 and f >= 0 and matrix[r,c,f] >= 0:
            sum += matrix[r,c,f]
            summedItems += 1
    value = 0
    average = 0
    if (summedItems > 0):
        average = sum / float(summedItems)
        
    # determine the target index
    r = indexRef[line[0][0],0]
    c = indexRef[line[0][1],1]
    f = indexRef[line[0][2],2]
    # set the target cell 
    matrix[r,c,f] = (noiseLevel * random.random()) + ((1-noiseLevel) * average)
    
    #print "setting", r, c, f, "to ", matrix[r, c, f]


def getIndexRef(row, col, frame, midRange, maxIndex):
    """
    Internal method
    Given a cube defined by the row, col, frame and size
    (midRange = (size-1)/2)  this method constructs a 3x4 array
    with the indices of the following values:
        [[row - midRange, row, row + midRange, row + 2*midRange],
         [col - midRange, col, col + midRange, col + 2*midRange],
         [frame - midRange, frame, frame + midRange, frame + 2*midRange]]
    Indices outside the range of 0 to maxIndex are set to -1.
    This can be used to find the center of a given cube, the midpoint 
    of any face and the midpoint of any edge.  
    It can also be used to find midpoints of neighboring cubes 
    to the top, left and front.
    """ 
    indexRef = numpy.zeros(12).reshape(4,3)
    indexRef[:,0] = numpy.arange(-1, 3) * midRange + row
    indexRef[:,1] = numpy.arange(-1, 3) * midRange + col
    indexRef[:,2] = numpy.arange(-1, 3) * midRange + frame
    
    for i in range(4):
        for j in range(3):
            if indexRef[i,j] < 0 or indexRef[i,j] > maxIndex:
                indexRef[i,j] = -1
    return indexRef
    
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

def applyCornerValues(matrix, roughness):
    """
    Internal method
    use random values to populate the corners of the matrix
    """
    maxIndex = matrix.shape[0] -1 
    #print "maxIndex = ", maxIndex
    
    matrix[0, 0, 0] = random.random() * roughness
    matrix[0, maxIndex, 0 ] = random.random() * roughness
    matrix[maxIndex, 0, 0] = random.random() * roughness
    matrix[maxIndex, maxIndex, 0] = random.random() * roughness
    
    matrix[0, 0, maxIndex] = random.random() * roughness
    matrix[0, maxIndex, maxIndex] = random.random() * roughness
    matrix[maxIndex, 0, maxIndex] = random.random() * roughness
    matrix[maxIndex, maxIndex, maxIndex] = random.random() * roughness
    # for debugging
    
def gaussianFilter3D(size, points): 
    """
    Create a 3D gaussian filter that can be applied to a matrix.
    
    Applying this filter will give a roundish frame to your fractal,
    or can be used to animate a moving plasma ball.
    
    Keyword arguments:
    size: size of the matrix
    points: list of points, each of which should be a tuple 
    including x, y, z, sigmaX, sigmaY, and sigmaZ
    sigmas are used to make the frame larger
    in the x and y or z dimension
    use numpy.multiply to apply the filter to a matrix.
    """
    
    matrix = numpy.zeros((size, size, size))
    
    for point in points:
        x0 = point[0]
        y0 = point[1]
        z0 = point[2]
        x2SigmaSquared = pow(point[3] * size/4, 2) * 2
        y2SigmaSquared = pow(point[4] * size/4, 2) * 2
        z2SigmaSquared = pow(point[5] * size/4, 2) * 2
        tempMatrix = numpy.zeros((size, size, size))
        for x in range(0, size):
            for y in range(0, size):
                for z in range(0, size):
                    tempMatrix[y, x, z] = math.exp(-1 * \
                        (math.pow(x-x0, 2)/x2SigmaSquared +\
                        math.pow(y-y0, 2)/y2SigmaSquared +\
                        math.pow(z-z0, 2)/z2SigmaSquared))
                      
        matrix = numpy.add(matrix, tempMatrix)
              
    matrix = matrixfix.flatten(matrix, 0, 1)
    
    return matrix
    
def printAllowCancel(matrix):
    # debugging method
    print (matrix * 100).astype(int)
        
    response = raw_input('ctl_c to stop >')