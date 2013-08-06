import numpy

def normalize(matrix, min = 0, max = 1):
    """
    Adjusts the values in a matrix to a given range
    """
    maxValue = numpy.amax(matrix)
    minValue = numpy.amin(matrix)
    
    if maxValue == minValue: return numpy.copy(matrix)
    
    newMatrix = (matrix - minValue) / (maxValue - minValue) 
    newMatrix = (newMatrix * (max - min)) + min;

    return newMatrix
    
def setStd(matrix, desiredSd):
    """ 
    Adjusts a matrix so that it has a given standard deviation, 
    without changing the mean.
    """  
    givenMean = numpy.sum(matrix)/float(matrix.size)
    givenSd = numpy.std(matrix)
    sdDif = desiredSd/float(givenSd);
    newMatrix = matrix * sdDif
    adjMean = numpy.sum(newMatrix)/matrix.size
    newMatrix = newMatrix + (givenMean - adjMean)
    return newMatrix