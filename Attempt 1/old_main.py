from PIL import Image
import os


#runs processes that prepare the image for manipulation
#opens an image based on input from the user
def start(originalFileName):
    originalImage = Image.open(originalFileName + ".jpg")

    #ensure that the image is 144p
    #if (originalImage.size[0] != 256) and (originalImage.size[1] != 144):
    #print("Not valid image size. Please use 256x144")
    #ends the program if not 144p
    #exit
  
    loop(originalImage, originalFileName)


#


#loops through all the pixels
#the manipultion functions are called within this one
def loop(original, name):
    #gets data on the color of pixels
    #originalImageData is a list
    originalImageData = original.getdata()
    originalImageData = list(originalImageData)

    #creates an empty list that will hold the manipulated color values
    newImageData = []

    #this is where the user chooses which filter to use
    filter = int(
        input(
            "1. Color Shift 2. Blur 3. Saturation 4. Brightness 5. Grayscale 6. Done\n"
        ))
    if (filter != 1) and (filter != 2) and (filter != 3) and (
            filter != 4) and (filter != 5) and (filter != 6):
        print("not valid answer")

        #these if statements collect an needed information to make the filter work
    if filter == 1:
        addR = int(input("Add red: "))
        addG = int(input("Add green: "))
        addB = int(input("Add blue: "))
    elif filter == 2:
        blurRadius = int(input("Blur Radius: "))
        originalImageMap = TwoDList(originalImageData, name)
        print(originalImageMap)
    elif filter == 3:
        addSat = int(input("Percent Saturation: "))
    elif filter == 4:
        addBright = int(input("Add brightness: "))
    elif filter == 5:
        pass
    #ends the program
    else:
        quit()

        #these two lines place the new color values into a list for later converstion into an image

    #runs once for each pixel
    #The manipulation fucntions will be called in this for loop
    for location in range(len(originalImageData)):
        #the element in the location index of originalImageData is a tuple, which will be temporarily converted to a list
        #the first element of the tuple is the red value, the second is green, and the third is blue

        #originalImageData[location] is breifly converted to a list to support item assignment
        pixelData = list(originalImageData[location])

        #This is where the function would be called that manipulates the color values
        if filter == 1:
            #pixelData is a list
            pixelData = colorShift(pixelData, addR, addG, addB)
        elif filter == 2:
            pixelData = blur(blurRadius, originalImageMap, location,
                             original.size)
            #blur(pixelData, originalImageData)
        elif filter == 3:
            pixelData = saturation(pixelData, addSat)
        elif filter == 4:
            pixelData = colorShift(pixelData, addBright, addBright, addBright)
        elif filter == 5:
            pixelData = grayscale(pixelData)

        #at this point, pixelData has been manipulated by a function
        pixelData = tuple(pixelData)
        newImageData.append(pixelData)

    #creates a new, empty image.
    newImage = Image.new("RGB", original.size)

    #puts the modified pixels values from newImageData into the new image and saves it
    newImage.putdata(newImageData)

    #While loop that adds "I" until the name is not a duplicate
    naming = True
    tag = "I"
    while naming == True:
        if os.path.exists(name + tag + ".jpg"):
            tag += "I"
        else:
            newImage.save(name + tag + ".jpg")
            naming = False


#allows the user to add or subtract a set value to each color channel individually
#is used for manual color shift and brightness
def colorShift(pixColors, deltaR, deltaG, deltaB):

    #pixColors is a list. [0] is red, [1] is green [2] is blue. It is changed to a list so that it supports item assignment

    #adds the specified value to red, keep contraints of 0-255
    pixColors[0] += deltaR
    if pixColors[0] > 255:
        pixColors[0] = 255
    if pixColors[0] < 0:
        pixColors[0] = 0

    #adds the specified value to green, keep contraints of 0-255
    pixColors[1] += deltaG
    if pixColors[1] > 255:
        pixColors[1] = 255
    if pixColors[1] < 0:
        pixColors[1] = 0

    #adds the specified value to blue, keep contraints of 0-255
    pixColors[2] += deltaB
    if pixColors[2] > 255:
        pixColors[2] = 255
    if pixColors[2] < 0:
        pixColors[2] = 0

    return pixColors


def saturation(pixColors, deltaSat):
    #adds deltaSat to the greatest number in the pixel, and subtracts it from the least

    #changes deltaSat to a %       25% --> .25
    deltaSat /= 100

    #finds indicies of the max, min, and the other
    maxIndex = pixColors.index(max(pixColors))
    minIndex = pixColors.index(min(pixColors))
    if maxIndex + minIndex == 3:
        otherIndex = 0
    elif maxIndex + minIndex == 2:
        otherIndex = 1
    else:
        otherIndex = 2

    #finds deltaSat% of the way to 255 from the max number
    maxAdd = int(255 - pixColors[maxIndex])
    maxAdd *= deltaSat
    maxAdd = round(maxAdd)

    #finds deltaSat% of the way to min from other
    otherSubtract = pixColors[otherIndex] - pixColors[minIndex]
    otherSubtract *= deltaSat
    otherSubtract = round(otherSubtract)

    #finds deltaSat% of the way to 0 from min
    minSubtract = round(pixColors[minIndex] * deltaSat)

    #adjusts the colors by a certain percent
    pixColors[maxIndex] += maxAdd
    pixColors[minIndex] -= minSubtract
    pixColors[otherIndex] -= otherSubtract

    return pixColors


def grayscale(pixColors):
    #averages the colors in each pixel
    avg = int((pixColors[0] + pixColors[1] + pixColors[2]) / 3)
    pixColors[0] = avg
    pixColors[1] = avg
    pixColors[2] = avg

    return (pixColors)


#averages the pixels within a radius blurR
def blur(blurR, Image2Dlist, blurLocation, imageSize):
    #the pixel's x position, or column index is the remainder of the original index divided by the length of the rows:  int(blurLocation % imageSize[0])
    #the pixel's y position, or row index is the original index divided by the length of the rows, and truncated at the tenths place: int(blurLocation / imageSize[0])

    pixColorsRowIndex = int(blurLocation // imageSize[0])
    pixColorsColumnIndex = int(blurLocation % imageSize[0])

    #finds pixColors based on the coordinate system
    pixColors = Image2Dlist[pixColorsRowIndex][pixColorsColumnIndex]

    #makes a sum of a pixels within a suare radius of the original pixel for red
    sumR = 0
    rowMove = 0
    columnMove = 0
    for i in range(((blurR * 2) + 1)**2):
        if ((pixColorsRowIndex + blurR - rowMove) < 0) or (
            (pixColorsColumnIndex - blurR + columnMove) < 0):
            pass
        else:
            try:
                sumR += Image2Dlist[pixColorsRowIndex + blurR - rowMove][pixColorsColumnIndex - blurR + columnMove][0]
            except:
                pass
        columnMove += 1

        if i % ((blurR * 2) + 1):
            rowMove += 1
            columnMove = 0

    sumR /= ((blurR * 2) + 1)**2

    #makes a sum of a pixels within a suare radius of the original pixel for green
    sumG = 0
    rowMove = 0
    columnMove = 0
    for i in range(((blurR * 2) + 1)**2):
        if ((pixColorsRowIndex + blurR - rowMove) < 0) or (
            (pixColorsColumnIndex - blurR + columnMove) < 0):
            pass
        else:
            try:
                sumG += Image2Dlist[pixColorsRowIndex + blurR - rowMove][pixColorsColumnIndex - blurR + columnMove][1]
            except:
                pass
        columnMove += 1

        if i % ((blurR * 2) + 1):
            rowMove += 1
            columnMove = 0

    sumG /= ((blurR * 2) + 1)**2

    #makes a sum of a pixels within a suare radius of the original pixel for blue
    sumB = 0
    rowMove = 0
    columnMove = 0
    for i in range(((blurR * 2) + 1)**2):
        if ((pixColorsRowIndex + blurR - rowMove) < 0) or (
            (pixColorsColumnIndex - blurR + columnMove) < 0):
            pass
        else:
            try:
                sumB += Image2Dlist[pixColorsRowIndex + blurR - rowMove][pixColorsColumnIndex - blurR + columnMove][2]
            except:
                pass
        columnMove += 1

        if (i % ((blurR * 2) + 1)) == 0:
            rowMove += 1
            columnMove = 0

    sumB /= ((blurR * 2) + 1)**2

    sumR = int(sumR)
    sumG = int(sumG)
    sumB = int(sumB)

    pixColors = (sumR, sumG, sumB)
    return pixColors


def TwoDList(pixelDataList, imageListName):
    #creates a list of all the pixel values in the image
    imageList = Image.open(imageListName + ".jpg")

    #assigns the length and width to the varible numRows and numColumns
    numRows = imageList.size[1]
    numColumns = imageList.size[0]
    pixelDataMap = []
    imageList = list(imageList.getdata())
    #loops through each row and appends it in order to a sindle element in pixelDataMap
    #Each element of pixelDataMap is a row of the image, and the index within the row is the column that the pixel is in
    for rowIndex in range(numRows):
        pixelDataMap.append(imageList[rowIndex * numColumns:(rowIndex + 1) *
                                      numColumns])

    return pixelDataMap


run = True
while run == True:
    start(str(input("\nFile name (exclude .jpg): ")))