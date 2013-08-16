import numpy
import math
import pngsaver
import matrixfix

def demoAnimation(fileName, inputMatrix, fromColor = [0,0,255], toColor =[255,255,255], ask = True):
    """ 
    zeros out the values in a plasma in the reverse order as they 
    were added and saves each step as an image. 
    The png files can be merged into a movie file using 
    Sequimago or other movie making tools.
    """
    msize = inputMatrix.shape[0]
    numberImages = inputMatrix.size * 2 + 1
    
    print "This method will create",  numberImages, "image files."
    if (ask):
        answer = raw_input("Is that okay?")
        if answer == "N" or answer == "n" or answer=="No" or answer=="no":
            return
    
    norm = matrixfix.normalize(inputMatrix, 0.01, 0.98)
    
    gradient = pngsaver.CosGradient([0,0,0])
    gradient.addStop(fromColor, 0.01)
    gradient.addStop(toColor, 0.98)
    gradient.addStop([255, 255, 0], 0.99)
    gradient.addStop([255, 0, 0], 1.0)
    
    matrix = numpy.zeros((msize * 3) * (msize * 3)).reshape((msize*3, msize*3))
    
    for i in range(msize):
        for j in range(msize):
            for k in range(3):
                for l in range(3):
                    matrix[i*3+k, j*3+l] = inputMatrix[i,j]
    
    fileNumber = numberImages + 100
    file = getFileName(fileName, fileNumber)
    fileNumber -= 1
    
    print "saving original", file
    pngsaver.saveCosGradient(file, matrix, gradient)
    
    size = 2
    
    while size < msize:
        
        offset2 = msize - 1 - size/2
        
        # diamond steps
        steps = (msize/size)
        print " "
        print "****diamond steps size:", size
        print " "
        for i in range(steps):
            r = (offset2 - (i * size)) * 3 + 1
            for j in range (steps):
                c = (offset2 - (j * size)) * 3 + 1
                
                #right edge 
                right = c + (3 * size/2)
                highlightPixel(r, right, 1, matrix)
                
                highlightDiamond(r, right, size, matrix)
                
                file = getFileName(fileName, fileNumber)
                fileNumber -= 1
                 
                print "saving right", file
                pngsaver.saveCosGradient(file, matrix, gradient)
                
                clearPixel(r, right, matrix)
                highlightDiamond(r, right, size, matrix, True)
                
                file = getFileName(fileName, fileNumber)
                fileNumber -= 1
                 
                print "saving cleared", file
                pngsaver.saveCosGradient(file, matrix, gradient)
                
                #bottom edge
                bottom = r + (3 * size/2)
                highlightPixel(bottom, c, 1, matrix)
                
                highlightDiamond(bottom, c, size, matrix)
                
                file = getFileName(fileName, fileNumber)
                fileNumber -= 1
                
                print "saving bottom", file
                pngsaver.saveCosGradient(file, matrix, gradient)
                
                clearPixel(bottom, c, matrix)
                highlightDiamond(bottom, c, size, matrix, True)
                 
                file = getFileName(fileName, fileNumber)
                fileNumber -= 1
                 
                print "saving cleared", file
                pngsaver.saveCosGradient(file, matrix, gradient)
                
                if i == (steps-1):
                    #top edge
                    highlightPixel(1, c, 1, matrix)
                    
                    highlightDiamond(1, c, size, matrix)
                    
                    file = getFileName(fileName, fileNumber)
                    fileNumber -= 1
                    
                    print "saving top", file
                    pngsaver.saveCosGradient(file, matrix, gradient)
                    
                    clearPixel(1, c, matrix)
                    highlightDiamond(1, c, size, matrix, True)
                    
                    file = getFileName(fileName, fileNumber)
                    fileNumber -= 1
                    
                    print "saving cleared", file
                    pngsaver.saveCosGradient(file, matrix, gradient)

            #left edge
            highlightPixel(r, 1, 1, matrix)
            
            highlightDiamond(r, 1, size, matrix)
            
            file = getFileName(fileName, fileNumber)
            fileNumber -= 1
            
            print "saving left", file
            pngsaver.saveCosGradient(file, matrix, gradient)
            
            clearPixel(r, 1, matrix)
            highlightDiamond(r, 1, size, matrix, True)
            
            file = getFileName(fileName, fileNumber)
            fileNumber -= 1
             
            print "saving cleared", file
            pngsaver.saveCosGradient(file, matrix, gradient)

        #square steps 
        print " "
        print "****square steps size:", size
        print " "
        for i in range(steps):
            for j in range (steps):
                r = (offset2 - (i * size)) * 3 + 1
                c = (offset2 - (j * size)) * 3 + 1
                
                highlightPixel(r, c, 1, matrix)
                
                highlightSquare(r, c, size, matrix)
                
                file = getFileName(fileName, fileNumber)
                fileNumber -= 1
                
                print "saving square", file
                pngsaver.saveCosGradient(file, matrix, gradient)
                
                clearPixel(r, c, matrix)
                highlightSquare(r, c, size, matrix, True)
                
                file = getFileName(fileName, fileNumber)
                fileNumber -= 1
                
                print "saving cleared", file
                pngsaver.saveCosGradient(file, matrix, gradient)
                
        size = size * 2
        
    file = getFileName(fileName, fileNumber)
    fileNumber -= 1

def highlightDiamond(r, c, size, matrix, undo = False):
    maxIndex = matrix.shape[0] - 1
    
    [top, bottom, left, right] = getBoundingSquare(r, c, size, maxIndex)
    
    if (undo):
        unhighlightPixel(top, c, matrix)
        unhighlightPixel(bottom, c, matrix)
        unhighlightPixel(r, left, matrix)
        unhighlightPixel(r, right, matrix) 
    else:
        highlightPixel(top, c, .99, matrix)
        highlightPixel(bottom, c, .99, matrix)
        highlightPixel(r, left, .99, matrix)
        highlightPixel(r, right, .99, matrix) 

def highlightSquare(r, c, size, matrix, undo = False):
    maxIndex = matrix.shape[0] - 1
    
    [top, bottom, left, right] = getBoundingSquare(r, c, size, maxIndex)
    
    if (undo):
        unhighlightPixel(top, left, matrix)
        unhighlightPixel(top, right, matrix)
        unhighlightPixel(bottom, left, matrix)
        unhighlightPixel(bottom, right, matrix) 
    else:
        highlightPixel(top, left, .99, matrix)
        highlightPixel(top, right, .99, matrix)
        highlightPixel(bottom, left, .99, matrix)
        highlightPixel(bottom, right, .99, matrix) 

def getBoundingSquare(r, c, size, maxIndex):
    incr = (size/2) * 3
    top = r - incr
    if top < 0:
        top = maxIndex + top - 2
        
    bottom = r + incr
    if bottom > maxIndex:
        bottom = bottom - maxIndex + 2
        
    left = c - incr
    if left < 0:
        left = maxIndex + left - 2
        
    right = c + incr
    if right > maxIndex:
        right = right - maxIndex + 2
        
    return [top, bottom, left, right]

def highlightPixel(r, c, color, matrix):
    matrix[r-1, c-1] = color
    matrix[r-1, c+1] = color
    matrix[r+1, c-1] = color
    matrix[r+1, c+1] = color

def clearPixel(r, c, matrix):
    for i in range(3):
        for j in range(3):
            matrix[r + i -1, c + j - 1] = 0

def unhighlightPixel(r, c, matrix):
    color = matrix[r,c]
    highlightPixel(r, c, color, matrix)

def getFileName(fileName, fileNumber):
    file = "{0}{1}.png".format(fileName, fileNumber)
    if (fileNumber < 10):
        file = "{0}000{1}.png".format(fileName,fileNumber)
    elif (fileNumber< 100):
        file = "{0}00{1}.png".format(fileName,fileNumber)
    elif (fileNumber< 1000):
        file = "{0}0{1}.png".format(fileName,fileNumber)
    return file
