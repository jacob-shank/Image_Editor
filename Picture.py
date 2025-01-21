from PIL import Image
from Pixel import Pixel
import os
import math

class Picture:
    def __init__(self, file_name: str):
        self.image = Image.open(file_name + ".jpg")
        self.width: int = self.image.size[0]
        self.height: int = self.image.size[1]
        self.pixels: list[Pixel] = list()
        self.black_point: int = 0
        self.white_point: int = 255

        self.name: str = file_name

        #loop through self.imageData and fill a new list with pixel objects     #(x,y,r,g,b)
        for y in range(self.height):
            for x in range(self.width):
                currentPixel = self.image.getpixel((x,y))
                self.pixels.append(Pixel(x,y,currentPixel[0],currentPixel[1],currentPixel[2]))

    def saveAs(self, file_extension: str) -> None:
        #creates a new, empty image.
        newImage = Image.new("RGB",(self.width,self.height))

        #puts the modified pixels values from newImageData into the new image and saves it
        for pixel in self.pixels:
            newImage.putpixel((pixel.v[0],pixel.v[1]),(pixel.v[2],pixel.v[3],pixel.v[4]))

        #While loop that adds "(n)" until the name is not a duplicate
        named = True
        tagNum = 1
        while named == True:
            tag = f"({tagNum})"
            if os.path.exists("" + self.name + tag + file_extension):
                tagNum += 1
            else:
                newImage.save("" + self.name + tag + file_extension)
                named = False

        del newImage

    def gradient(self) -> None:
        for pixel in self.pixels:
            value = lambda offset : 255 - abs(int((255 * (pixel.x() - offset))/(self.width/2)))
            pixel.setColor(max(0,value(0)), max(0,value(self.width/2)), max(0,value(self.width)))

            #now normalize the brightness/saturation
            '''saturation: int = int(pixel.r()) + int(pixel.g()) + int(pixel.b())
            if(saturation != 0):
                #find how much of the color is made up by a given color
                percent_r = pixel.r()/saturation
                percent_g = pixel.g()/saturation
                percent_b = pixel.b()/saturation

                #now distribute the difference among them accordingly
                difference = 255 - saturation
                
                pixel.changeColor(int(percent_r*difference), int(percent_g*difference), int(percent_b*difference))'''
            
            #vary brightness on the vetical axis
            pixel.changeBrightness(int(((255 * (pixel.y() - (self.height/2)))/(self.height/2))))

    def changeBrightness(self, delta: int) -> None:
        for pixel in self.pixels:
            pixel.changeBrightness(delta)

    def changeContrast(self, delta: int) -> None:
        for pixel in self.pixels:
            pixel.changeContrast(delta)

    def changeSaturation(self, percentChange: int) -> None:
        for pixel in self.pixels:
            pixel.changeSaturation(percentChange)
    
    def setBlackPoint(self, threshhold: int, smoothing: float) -> None:
        self.black_point = threshhold
        if(self.black_point < 0):
            self.black_point = 0
        elif(self.black_point > 255):
            self.black_point = 255

        #execute the transformation
        for pixel in self.pixels:
            if(int(pixel.brightness()) <= self.black_point):
                pixel.setGray(0)
            elif(smoothing > 0 and pixel.brightness() > 0):
                pixel.changeBrightness(-(smoothing/(pixel.brightness()-self.black_point)))

    def setWhitePoint(self, threshhold: int, smoothing: float) -> None:
        self.white_point = threshhold
        if(self.white_point < 0):
            self.white_point = 0
        elif(self.white_point > 255):
            self.white_point = 255

        #execute the transformation
        for pixel in self.pixels:
            if(int(pixel.brightness()) >= self.white_point):
                pixel.setGray(255)
            elif(smoothing > 0 and pixel.brightness() > 0):
                pixel.changeBrightness((smoothing/(self.white_point-pixel.brightness())))
    
    def changeWhitePoint(self, delta: int, smoothing: float) -> None:
        self.setWhitePoint(self.white_point + delta, smoothing)

    def changeBlackPoint(self, delta: int, smoothing: float) -> None:
        self.setBlackPoint(self.black_point + delta, smoothing)

    def changeVignette(self, percent_cover: int, gradient_coeffiecient: float, color: tuple[int, int, int] = (0,0,0)) -> None:
        center: tuple[int, int] = (self.width/2,self.height/2)
        for pixel in self.pixels:
            pixel.changeVignette(percent_cover, gradient_coeffiecient, center, int(max(self.width/2,self.height/2)), self.width/self.height, color)

    def boxBlur(self, distance: int) -> None:
        '''Replaces a pixels value with the average value of all pixels in a box with side length distance*2 + 1'''

        '''blur both axes seperately with a distance of distance in both directions'''
        temp: list[Pixel] = self.pixels #blur cannot be done in place because a particular pixels value depends on its neighbors value

        avg_r = 0
        avg_g = 0
        avg_b = 0

        #(x,y) -> index in temp: index = (y*width) + x

        #blur vertically
        for pixel in temp:
            #go up
            for i in range(distance):
                #only go up if there is pixels above
                if(pixel.y() - i >= 0):
                    #x stays the same -> same column
                    #y decreases -> go up rows
                    current_pixel: Pixel = temp[((pixel.y() - i)*self.width) + pixel.x()]

                    avg_r += current_pixel.r()
                    avg_g += current_pixel.g()
                    avg_b += current_pixel.b()
            
            #go down
            for i in range(distance):
                #only go down if there are pixels below
                if(pixel.y() + i < self.height):
                    #x stays the same -> same columns
                    #y increases -> go down rows
                    current_pixel: Pixel = temp[((pixel.y() + i)*self.width) + pixel.x()]

                    avg_r += current_pixel.r()
                    avg_g += current_pixel.g()
                    avg_b += current_pixel.b()
            
            #now calc averages
            num_pixels: int = (distance*2 + 1)
            if(pixel.y() - distance < 0):
                num_pixels += pixel.y() - distance #Do not count the pixels that were above the screen
            if(pixel.y() + distance >= self.height):
                num_pixels -= pixel.y() + distance - self.height # Do not coun pixels that were below the screen

            avg_r /= num_pixels
            avg_g /= num_pixels
            avg_b /= num_pixels

            #now write it into self.pixels
            self.pixels[(pixel.y()*self.width) + pixel.x()].setColor(int(avg_r),int(avg_g),int(avg_b))

        #blur horizontally
        for pixel in temp:
            #go left
            for i in range(distance):
                #only go left if there are pixels leftward
                if(pixel.x() - i >= 0):
                    #x decreases -> go left column
                    #y stays same -> stay in row
                    current_pixel: Pixel = temp[(pixel.y()*self.width) + pixel.x() - i]

                    avg_r += current_pixel.r()
                    avg_g += current_pixel.g()
                    avg_b += current_pixel.b()

            #go right
            for i in range(distance):
                #only go right if there are pixels rightward
                if(pixel.x() + i < self.width):
                    #x increases -> go right columns
                    #y stays same -> stay in row
                    current_pixel: Pixel = temp[(pixel.y()*self.width) + pixel.x() + i]

                    avg_r += current_pixel.r()
                    avg_g += current_pixel.g()
                    avg_b += current_pixel.b()
            
            #now calc averages
            num_pixels: int = distance*2 + 1
            if(pixel.x() - distance < 0):
                num_pixels += pixel.x() - distance # Do not count pixels to the left of the screen
            if(pixel.x() + distance >= self.width):
                num_pixels -= pixel.x() + distance - self.width # Do not count pixels to the right of the screen

            avg_r /= num_pixels
            avg_g /= num_pixels
            avg_b /= num_pixels

            #now write it into self.pixels
            self.pixels[(pixel.y()*self.width) + pixel.x()].setColor(int(avg_r),int(avg_g),int(avg_b))