import numpy

def shrink(oldList, newSize):
    oldIndex = 0
    newIndex = 0

    oldSize = len(oldList)
    sizeAdjust = newSize/float(oldSize)
    
    # x is a float indicating the current position in the oldList
    # for example 2.5 means that oldList[0] through oldList[2] and half of oldList[3] 
    # has been copied to the result
    x = 0
    result = []

    for newIndex in range(newSize):
        # limit is the highest position that can be copied 
        # into the result
        limit = (newIndex + 1) * oldSize / float(newSize)
        result.append(0)
        
        # while the current position is less than the limit
        while x < limit:
            if oldIndex >= oldSize:
                print "stopped because x =", x, "and oldIndex =", oldIndex
                break
            # portion is the portion of oldList[oldIndex] that will be included
            # in result[newIndex]
            # limit - x: keeps portion from pushing x over the limit 
            # oldIndex + 1 - x: keeps the portion from pushing x into the next cell.
            portion = min(1, min(oldIndex + 1 - x, limit - x))
            x +=  portion
            result[newIndex] += round(oldList[oldIndex] * portion * sizeAdjust, 6)
            if x >= oldIndex + 1:
                oldIndex += 1
    return result


def shrinkMatrix(oldMatrix, newSize):
    oldSize = oldMatrix.shape[0]
    rowMatrix = numpy.zeros((oldSize, newSize))
    for i in range(oldSize):
        mat = shrink(oldMatrix[i,:], newSize)
        rowMatrix[i,:] = mat

    newMatrix = numpy.zeros((newSize, newSize))
    for i in range(newSize):
        mat = shrink(rowMatrix[:,i], newSize)
        newMatrix[:,i] = mat

    #import matrixfix
    #newMatrix = matrixfix.normalize(newMatrix)
    return newMatrix
    
