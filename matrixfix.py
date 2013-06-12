import numpy

#normalizes a matrix to a given min and max   
def normalize(matrix, min = 0, max = 1):
    maxValue = numpy.amax(matrix)
    minValue = numpy.amin(matrix)
    
    newMatrix = (matrix - minValue) / (maxValue - minValue) 
    newMatrix = (newMatrix * (max - min)) + min;

    return newMatrix
  
#flattens the values of a matrix to a given min and max      
def flatten(matrix, minVal, maxVal):

    newMatrix = numpy.zeros(matrix.shape)
    for x in range(0, matrix.shape[0]):
        for y in range(0, matrix.shape[1]):
            newMatrix[x, y] = max(minVal, min(maxVal, matrix[x,y]))
        
    return newMatrix 