import numpy
import math
import random
import matrixfix
import time
import sys

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
    
    start = time.time()
    
    #calculate the fractal based on the next highest 2^n + 1
    n = math.log(size-1, 2)
    if size >  513 or n != float(int(n)):
        print "The size is not valid."
        print "Valid sizes are 5, 9, 17, 33, 65, 129, 257 and 513."
        return
    
    print "Initializing..."
    
    matrix = numpy.zeros((size, size, size))
    
    applyCornerValues(matrix, roughness)
    
    # csize is the current cube size
    # It starts at the maximum index value.  The centers, faces and edges of the csize cubes
    # are filled in, then csize is halved.  The process is repeated until all the cells
    # are filled in.
    csize = maxindex = size-1
    
    numberCubes = 1
    
    while csize > 1:
        startcube = time.time()
        if 1 == numberCubes:
            print "Populating 1 size", csize, "cube",
        else:
            print "Populating", numberCubes, "size", csize, "cubes",
        numberCubes = numberCubes * 2
        sys.stdout.flush()
        
        # variables indicating where to start slicing the matrix
        # startb is half the current cube size. 
        startb = csize/2             #1
        # startc is the current cube size.
        startc = csize               #2
        # startd is 1.5 times the current cube size 
        startd = csize + csize/2     #3
        # startz starts at the last index
        startz = maxindex            #4
        #start y starts at the max index minus half the current cube size
        starty = maxindex - csize/2  #3
        
        #variables indicating where to stop slicing the matrix
        #(The stop index is not included in the slice.)
        #enda is the max index - the current cube size
        enda = maxindex-csize        #2
        #endb is the max index minus half the current cube size
        endb = maxindex-csize/2      #3
        #endc is the max index
        endc = maxindex              #4
        
        pf = perturbanceFactor(size, csize, perturbance)
        noiseLevel = roughness * pf
        
        print ".",
        sys.stdout.flush()
        
        #centers
        matrix[startb::csize, startb::csize, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[0:endc:csize,0:endc:csize, 0:endc:csize],\
            matrix[0:endc:csize, 0:endc:csize, startc::csize],\
            matrix[0:endc:csize, startc::csize, 0:endc:csize],\
            matrix[0:endc:csize, startc::csize, startc::csize],\
            matrix[startc::csize, 0:endc:csize, 0:endc:csize],
            matrix[startc::csize, 0:endc:csize, startc::csize],
            matrix[startc::csize, startc::csize, 0:endc:csize],
            matrix[startc::csize, startc::csize, startc::csize]])
            
        print ".",
        sys.stdout.flush()
            
        #topmost face
        matrix[0, startb::csize, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[0, 0:endc:csize, 0:endc:csize],\
            matrix[0, 0:endc:csize, startc::csize],\
            matrix[0, startc::csize, 0:endc:csize],\
            matrix[0, startc::csize, startc::csize],\
            matrix[startb, startb::csize, startb::csize]])
            
        #leftmost face
        matrix[startb::csize, 0, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[0:endc:csize, 0, 0:endc:csize],\
            matrix[0:endc:csize, 0, startc::csize],\
            matrix[startc::csize, 0, 0:endc:csize],\
            matrix[startc::csize, 0, startc::csize],\
            matrix[startb::csize, startb, startb::csize]])
            
        #frontmost face
        matrix[startb::csize, startb::csize, 0] =\
            getValue(noiseLevel,\
            [matrix[0:endc:csize, 0:endc:csize, 0],\
            matrix[0:endc:csize, startc::csize, 0],\
            matrix[startc::csize, 0:endc:csize, 0],\
            matrix[startc::csize, startc::csize, 0],\
            matrix[startb::csize, startb::csize, startb]])
            
        #bottommost face
        matrix[startz, startb::csize, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[startz, 0:endc:csize, 0:endc:csize],\
            matrix[startz, 0:endc:csize, startc::csize],\
            matrix[startz, startc::csize, 0:endc:csize],\
            matrix[startz, startc::csize, startc::csize],\
            matrix[starty, startb::csize, startb::csize]])
        
        #rightmost face
        matrix[startb::csize, startz, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[0:endc:csize, startz, 0:endc:csize],\
            matrix[0:endc:csize, startz, startc::csize],\
            matrix[startc::csize, startz, 0:endc:csize],\
            matrix[startc::csize, startz, startc::csize],\
            matrix[startb::csize, starty, startb::csize]])
            
        #backmost face
        matrix[startb::csize, startb::csize, startz] =\
            getValue(noiseLevel,\
            [matrix[0:endc:csize, 0:endc:csize, startz],\
            matrix[0:endc:csize, startc::csize, startz],\
            matrix[startc::csize, 0:endc:csize, startz],\
            matrix[startc::csize, startc::csize, startz],\
            matrix[startb::csize, startb::csize, starty]])
            
        print ".",
        sys.stdout.flush()
        
        # top left edge
        matrix[0, 0, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[0, 0, 0:endb:csize],\
            matrix[0, 0, startc::csize],\
            matrix[0, startb, startb::csize],\
            matrix[startb, 0, startb::csize]])
        
        # top front edge
        matrix[0, startb::csize, 0] =\
            getValue(noiseLevel,\
            [matrix[0, 0:endb:csize, 0],\
            matrix[0, startc::csize, 0],\
            matrix[0, startb::csize, startb],\
            matrix[startb, startb::csize, 0]])
                
        # top right edge
        matrix[0, startz, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[0, startz, 0:endb:csize],\
            matrix[0, startz, startc::csize],\
            matrix[0, starty, startb::csize],\
            matrix[startb, 0, startb::csize]])
        
        # top back edge
        matrix[0, startb::csize, startz] =\
            getValue(noiseLevel,\
            [matrix[0, 0:endb:csize, startz],\
            matrix[0, startc::csize, startz],\
            matrix[0, startb::csize, starty],\
            matrix[startb, startb::csize, startz]])
            
        # left front edge
        matrix[startb::csize, 0, 0] =\
            getValue(noiseLevel,\
            [matrix[0:endb:csize, 0, 0],\
            matrix[startc::csize, 0, 0],\
            matrix[startb::csize, 0, startb],\
            matrix[startb::csize, startb, 0]])
            
        # left back edge
        matrix[startb::csize, 0, startz] =\
            getValue(noiseLevel,\
            [matrix[0:endb:csize, 0, startz],\
            matrix[startc::csize, 0, startz],\
            matrix[startb::csize, 0, starty],\
            matrix[startb::csize, startb, startz]])
            
        # right front edge
        matrix[startb::csize, startz, 0] =\
            getValue(noiseLevel,\
            [matrix[0:endb:csize, startz, 0],\
            matrix[startc::csize, startz, 0],\
            matrix[startb::csize, startz, startb],\
            matrix[startb::csize, starty, 0]])
            
        # right back edge
        matrix[startb::csize, startz, startz] =\
            getValue(noiseLevel,\
            [matrix[0:endb:csize, startz, startz],\
            matrix[startc::csize, startz, startz],\
            matrix[startb::csize, startz, starty],\
            matrix[startb::csize, starty, startz]])
            
        # bottom left edge
        matrix[startz, 0, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[startz, 0, 0:endb:csize],\
            matrix[startz, 0, startc::csize],\
            matrix[startz, startb, startb::csize],\
            matrix[starty, 0, startb::csize]])
        
        # bottom front edge
        matrix[startz, startb::csize, 0] =\
            getValue(noiseLevel,\
            [matrix[startz, 0:endb:csize, 0],\
            matrix[startz, startc::csize, 0],\
            matrix[startz, startb::csize, startb],\
            matrix[starty, startb::csize, 0]])
                
        # bottom right edge 
        matrix[startz, startz, startb::csize] =\
            getValue(noiseLevel,\
            [matrix[startz, startz, 0:endb:csize],\
            matrix[startz, startz, startc::csize],\
            matrix[startz, starty, startb::csize],\
            matrix[starty, startz, startb::csize]])
        
        # bottom back edge 
        matrix[startz, startb::csize, startz] =\
            getValue(noiseLevel,\
            [matrix[startz, 0:endb:csize, startz],\
            matrix[startz, startc::csize, startz],\
            matrix[startz, startb::csize, starty],\
            matrix[starty, startb::csize, startz]])
        
        if (csize < maxindex):
            print ".",
            sys.stdout.flush()
            
            # top/bottom faces
            matrix[startc:endb:csize, startb::csize, startb::csize] =\
                getValue(noiseLevel,\
                [matrix[startc:endb:csize, 0:endc:csize, 0:endc:csize],\
                matrix[startc:endb:csize, 0:endc:csize, startc::csize],\
                matrix[startc:endb:csize, startc::csize, 0:endc:csize],\
                matrix[startc:endb:csize, startc::csize, startc::csize],\
                matrix[startd::csize, startb::csize, startb::csize],\
                matrix[startb:endb:csize, startb::csize, startb::csize]])
            
            # left/right faces
            matrix[startb::csize, startc:endb:csize, startb::csize] =\
                getValue(noiseLevel,\
                [matrix[0:endc:csize, startc:endb:csize, 0:endc:csize],\
                matrix[0:endc:csize, startc:endb:csize, startc::csize],\
                matrix[startc::csize, startc:endb:csize, 0:endc:csize],\
                matrix[startc::csize, startc:endb:csize, startc::csize],\
                matrix[startb::csize, startd::csize, startb::csize],\
                matrix[startb::csize, startb:endb:csize, startb::csize]])
            
            # front/back faces
            matrix[startb::csize, startb::csize, startc:endb:csize] =\
                getValue(noiseLevel,\
                [matrix[0:endc:csize, 0:endc:csize, startc:endb:csize],\
                matrix[0:endc:csize, startc::csize, startc:endb:csize],\
                matrix[startc::csize, 0:endc:csize, startc:endb:csize],\
                matrix[startc::csize, startc::csize, startc:endb:csize],\
                matrix[startb::csize, startb::csize, startd::csize],\
                matrix[startb::csize, startb::csize, startb:endb:csize]])
                        
            print ".",
            sys.stdout.flush()
            
            # surface edges
            # top edge 1
            matrix[0, startc:endb:csize, startb::csize] =\
                getValue(noiseLevel,\
                [matrix[0, startb:endb:csize, startb::csize],\
                matrix[0, startd::csize, startb::csize],\
                matrix[0, startc:endc:csize, 0:endb:csize],\
                matrix[0, startc:endc:csize, startc::csize],\
                matrix[startb, startc:endc:csize, startb::csize]])
                        
            # top edge 2
            matrix[0, startb::csize, startc:endb:csize] =\
                getValue(noiseLevel,\
                [matrix[0, 0:endb:csize, startc:endb:csize],\
                matrix[0, startc::csize, startc:endb:csize],\
                matrix[0, startb::csize, startb:endb:csize],\
                matrix[0, startb::csize, startd::csize],\
                matrix[startb, startb::csize, startc:endb:csize]])
            
            # bottom edges 1
            matrix[startz, startc:endb:csize, startb::csize] =\
                getValue(noiseLevel,\
                [matrix[startz, startb:endb:csize, startb::csize],
                matrix[startz, startd::csize, startb::csize],
                matrix[startz, startc:endc:csize, 0:endb:csize],
                matrix[startz, startc:endc:csize, startc::csize],
                matrix[starty, startc:endc:csize, startb::csize]])
                        
            # bottom edges 2 
            matrix[startz, startb::csize, startc:endb:csize] =\
                getValue(noiseLevel,\
                [matrix[startz, 0:endb:csize, startc:endb:csize],\
                matrix[startz, startc::csize, startc:endb:csize],\
                matrix[startz, startb::csize, startb:endb:csize],\
                matrix[startz, startb::csize, startd::csize],\
                matrix[starty, startb::csize, startc:endb:csize]])
            
            # left edges 1
            matrix[startc:endb:csize, 0, startb::csize] =\
                getValue(noiseLevel,\
                [matrix[startb:endb:csize, 0, startb::csize],\
                matrix[startd::csize, 0, startb::csize],\
                matrix[startc:endc:csize, 0, 0:endb:csize],\
                matrix[startc:endc:csize, 0, startc::csize],\
                matrix[startc:endc:csize, startb, startb::csize]])
            
            # left edges 2
            matrix[startb::csize, 0, startc:endc:csize] =\
                getValue(noiseLevel,\
                [matrix[0:endb:csize, 0, startc:endc:csize],\
                matrix[startc::csize, 0, startc:endc:csize],\
                matrix[startb::csize, 0, startb:endb:csize],\
                matrix[startb::csize, 0, startd::csize],\
                matrix[startb::csize, startb, startc:endc:csize]])
            
            # right edges 1
            matrix[startc:endc:csize, startz, startb::csize] =\
                getValue(noiseLevel,\
                [matrix[startb:endb:csize, startz, startb::csize],\
                matrix[startd::csize, startz, startb::csize],\
                matrix[startc:endc:csize, startz, 0:endb:csize],\
                matrix[startc:endc:csize, startz, startc::csize],\
                matrix[startc:endc:csize, starty, startb::csize]])
            
            # right edges 2
            matrix[startb::csize, startz, startc:endc:csize] =\
                getValue(noiseLevel,\
                [matrix[0:endb:csize, startz, startc:endc:csize],\
                matrix[startc::csize, startz, startc:endc:csize],\
                matrix[startb::csize, startz, startb:endb:csize],\
                matrix[startb::csize, startz, startd::csize],\
                matrix[startb::csize, starty, startc:endc:csize]])
            
            # front edges 1
            matrix[startb::csize, startc:endb:csize, 0] =\
                getValue(noiseLevel,\
                [matrix[startb::csize, startb:endb:csize, 0],\
                matrix[startb::csize, startd::csize, 0],\
                matrix[0:endb:csize, startc:endc:csize, 0],\
                matrix[startc::csize, startc:endc:csize, 0],\
                matrix[startb::csize, startc:endc:csize, startb]])
            
            # front edges 2
            matrix[startc:endc:csize, startb::csize, 0] =\
                getValue(noiseLevel,\
                [matrix[startc:endc:csize, 0:endb:csize, 0],\
                matrix[startc:endc:csize, startc::csize, 0],\
                matrix[startb:endb:csize, startb::csize, 0],\
                matrix[startd::csize, startb::csize, 0],\
                matrix[startc:endc:csize, startb::csize, startb]])
            
            # back edges 1
            matrix[startb::csize, startc:endc:csize, startz] =\
                getValue(noiseLevel,\
                [matrix[startb::csize, startb:endb:csize, startz],\
                matrix[startb::csize, startd::csize, startz],\
                matrix[0:endb:csize, startc:endc:csize, startz],\
                matrix[startc::csize, startc:endc:csize, startz],\
                matrix[startb::csize, startc:endc:csize, starty]])
            
            # back edges 2
            matrix[startc:endc:csize, startb::csize, startz] =\
                getValue(noiseLevel,\
               [matrix[startc:endc:csize, 0:endb:csize, startz],\
                matrix[startc:endc:csize, startc::csize, startz],\
                matrix[startb:endb:csize, startb::csize, startz],\
                matrix[startd::csize, startb::csize, startz],\
                matrix[startc:endc:csize, startb::csize, starty]])
            
            print ".",
            sys.stdout.flush()
            # internal edge 1
            matrix[startb:endc:csize, startc:endb:csize, startc:endb:csize] =\
                getValue(noiseLevel,\
                [matrix[0:endb:csize, startc:endb:csize, startc:endb:csize],\
                matrix[startc::csize, startc:endb:csize, startc:endb:csize],\
                matrix[startb:endc:csize, startb:enda:csize, startc:endb:csize],\
                matrix[startb:endc:csize, startd:endc:csize, startc:endb:csize],\
                matrix[startb:endc:csize, startc:endb:csize, startb:enda:csize],\
                matrix[startb:endc:csize, startc:endb:csize, startd:endc:csize]])
            
            # internal edge 2
            matrix[startc:endb:csize, startb:endc:csize, startc:endb:csize] =\
                getValue(noiseLevel,\
               [matrix[startc:endb:csize, 0:endb:csize, startc:endb:csize],\
                matrix[startc:endb:csize, startc::csize, startc:endb:csize],\
                matrix[startb:enda:csize, startb:endc:csize, startc:endb:csize],\
                matrix[startd:endc:csize, startb:endc:csize, startc:endb:csize],\
                matrix[startc:endb:csize, startb:endc:csize, startb:enda:csize],\
                matrix[startc:endb:csize, startb:endc:csize, startd:endc:csize]])
            
            # internal edge 3
            matrix[startc:endb:csize, startc:endb:csize, startb:endc:csize] =\
                getValue(noiseLevel,\
               [matrix[startc:endb:csize, startc:endb:csize, 0:endb:csize],\
                matrix[startc:endb:csize, startc:endb:csize, startc::csize],\
                matrix[startb:enda:csize, startc:endb:csize, startb:endc:csize],\
                matrix[startd:endc:csize, startc:endb:csize, startb:endc:csize],\
                matrix[startc:endb:csize, startb:enda:csize, startb:endc:csize],\
                matrix[startc:endb:csize, startd:endc:csize, startb:endc:csize]])
        
        print str(time.time() - startcube), "seconds."
        sys.stdout.flush()
        
        #decrement the current cube size
        csize = csize/2
    print "average =", numpy.sum(matrix)/matrix.size
    print "elapsed seconds =", str(time.time() - start)
    return matrix


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
        if numpy.amin(value) < 0:
            print "getValue received a value < 0."
            print "This indicates that an unpopulate cell is being used in an average."
            print value
            response = raw_input('ctl_c to stop >')
    averageValue = averageValue / float(len(values))
    
    randomValue = numpy.random.random(values[0].size).reshape(values[0].shape)
    
    result = (noiseLevel * randomValue) + ((1 - noiseLevel) * averageValue)
    
    return result
    

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
    #print (matrix * 100).astype(int)
        
    #response = raw_input('ctl_c to stop >')
    return