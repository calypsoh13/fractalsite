import numpy
import math
import random

centers = [[[2,2,2], [1,1,1], [1,1,3], [1,3,3], [3,1,1], [3,1,3], [3,3,1], [3,3,3]],
           [[1,2,2], [1,1,1], [1,3,1], [1,1,3], [1,3,3]],
           [[2,1,2], [1,1,1], [3,1,1], [1,1,3], [3,1,3]],
           [[2,2,1], [1,1,1], [3,1,1], [1,3,1], [3,3,1]],
           [[2,2,3], [1,1,3], [3,1,3], [1,3,3], [3,3,3]],
           [[2,3,2], [1,3,1], [3,3,1], [1,3,3], [3,3,3]],
           [[3,2,2], [3,1,1], [3,3,1], [3,1,3], [3,3,3]]]
           
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

def diamondSquareFractal3D(size, roughness = .5, perturbance = .5):
    
    #calculate the fractal based on the next highest 2^n + 1
    n = math.log(size-1, 2)
    if n != float(int(n)):
        print "The size is not valid, choose a side that is a power of 2 + 1."
        print "65, 129, 257, 513, 1025, etc."
        return
   
    matrix = numpy.zeros((size, size, size))
    
    applyCornerValues(matrix, roughness)
    
    # The algorithm requires calculating the midpoints and edges of 
    # all of the n-size squares before any n/2-size squares are calculated.
    # (This is because the midpoints of neighboring squares are used when
    # calculating the edges.)
    # A queue will be used to manage the squares waiting to be calculated.
    from collections import deque
    queue = deque()
    
    # add the whole matrix.
    queue.append([0, size-1, 0 ,size-1, 0 , size-1])

    while len(queue) > 0:
        # pop a square
        [row, maxRow, col, maxCol, frame, maxFrame] = queue.popleft()

        range = maxRow - row
        # populate the midpoint and edges of the square
        [midRow, midCol, midFrame] = diamondSquarePopulate3D(matrix, 
            row, col, frame, range, roughness, perturbance)

        # add divided cubes
        if maxRow - row >= 4:
            #add top left front cube to the queue 
            queue.append([row, midRow, col, midCol, frame, midFrame])
            
            #add top left back cube to the queue
            queue.append([row, midRow, col, midCol, midFrame, maxFrame])

            #add top right front cubes to the queue
            queue.append([row, midRow, midCol, maxCol, frame, midFrame])

            #add bottom left front cubes to the queue
            queue.append([midRow, maxRow, col, midCol, frame, midFrame])
            
            #add top right back cubes to the queue 
            queue.append([row, midRow, midCol, maxCol, midFrame, maxFrame])

            #add bottom left back cubes to the queue
            queue.append([midRow, maxRow, col, midCol, midFrame, maxFrame])

            #add bottom right front cubes to the queue
            queue.append([midRow, maxRow, midCol, maxCol, frame, midFrame])
            
            #add bottom right back cubes to the queue
            queue.append([midRow, maxRow, midCol, maxCol, midFrame, maxFrame])

    #print "result mean =", matrix.mean(), "result std = ", matrix.std()

    # return the requested size
    return matrix[0:size, 0:size]

def makeTempMatrix(matrix, row, col, frame, midRange):
    temp = (numpy.zeros(64) - 1).reshape(4,4,4)
    for r in range(4):
        if r == 0 and row < midRange:
            #print "temp skipping row because ", row, "<", midRange
            continue
        else:
            for c in range(4):
                if c == 0 and col < midRange:
                    #print "temp skipping col because ", col, "<", midRange
                    continue
                else:
                    for f in range(4):
                        if f == 0 and frame < midRange:
                            #print "temp skipping frame because ", frame, "<", midRange
                            continue
                        else:
                            rr = (r - 1) * midRange + row
                            cc = (c - 1) * midRange + col
                            ff = (f - 1) * midRange + frame
                            temp[r,c,f] = matrix[rr,cc,ff]
    #print "makeTempMatrix row, col, frame, midRange", row, col, frame, midRange
    #print "makeTempMatrix temp=", temp
    #response = raw_input('ctl_c to stop >')
    return temp
    
def updateMatrix(matrix, temp, row, col, frame, midRange):
    #print "updateMatrix row, col, frame, midRange", row, col, frame, midRange
    #print "updateMatrix temp=", temp
    for r in range(1,4):
        for c in range (1,4):
            for f in range (1,4):
                rr = (r - 1) * midRange + row
                cc = (c - 1) * midRange + col
                ff = (f - 1) * midRange + frame
                #print "matrix", rr, cc, ff, "=", temp[r,c,f]
                matrix[rr,cc,ff] = temp[r,c,f]
    #response = raw_input('ctl_c to stop >')
    return matrix
    
def populateCenters(matrix, shift, noiseLevel):
    for center in centers:
        target = center[0]
        sum = 0
        summedItems = 0
        for i in range(1, len(center)):
            point = center[i]
            sum += matrix[shift[point[0],0],shift[point[1],1],shift[point[2],2]]
            summedItems += 1
        value = getValue(sum/float(summedItems), noiseLevel)
        matrix[shift[target[0],0],shift[target[1],1],shift[target[2],2]] = value
        
def populateEdges(matrix, shift, noiseLevel):
    for edge in edges:
        target = edge[0]
        sum = 0
        summedItems = 0
        for i in range(1, len(edge)):
            item = edge[i]
            sum += matrix[shift[item[0],0],shift[item[1],1],shift[item[2],2]]
            summedItems += 1
        value = getValue(sum / float(summedItems), noiseLevel)
        #print "edges target loc =", target[0], target[1], target[2], "value =", value
        matrix[shift[target[0],0],shift[target[1],1],shift[target[2],2]] = value

def getValue(value, noiseLevel):
    #print "getValue for ", value, noiseLevel
    return (noiseLevel * random.random()) + ((1-noiseLevel) * value)

def diamondSquarePopulate3D(matrix, row, col, frame, range, roughness, perturbance):
    
    midRange = range / 2
    maxIndex = matrix.shape[0]-1
    
    #put the actual indices appropriate for this cube into the shift array
    shift = numpy.zeros(12).reshape(4,3)
    shift[:,0] = numpy.arange(-1, 3) * midRange + row
    shift[:,1] = numpy.arange(-1, 3) * midRange + col
    shift[:,2] = numpy.arange(-1, 3) * midRange + frame
    
    pf = perturbanceFactor(matrix.shape[0], range, perturbance)
    noiseLevel = roughness * pf
    
    #temp = makeTempMatrix(matrix, row, col, frame, midRange)

    populateCenters(matrix, shift, noiseLevel)

    populateEdges(matrix, shift, noiseLevel)
    
    #updateMatrix(matrix, temp, row, col, frame, midRange)
    
    return [row + midRange, col + midRange, frame + midRange]

def perturbanceFactor(lenWhole, lenPart, perturbance):
    k = 1 - perturbance
    return lenPart ** k / lenWhole ** k

def applyCornerValues(matrix, roughness):

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