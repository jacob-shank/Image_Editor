import math

class Pixel:
    def __init__(self, x:int, y:int, r:int, g:int, b:int):
        self.v: list = [x,y,r,g,b] #used like a column vector

    def __str__(self):
        return f"({self.v[0]},{self.v[1]},{self.v[2]},{self.v[3]},{self.v[4]})"
    
    def __repr__(self):
        return self.__str__()

    #pixel level adjustment
    def changeBrightness(self, delta: int) -> None:
        self.changeColor(delta, delta, delta)

    def changeVignette(self, percent_cover: float, gradient_coeffiecient: float, center: tuple[int, int], dist_to_edge: int, aspect_ratio: float, color: tuple[int, int, int]) -> None:

        #get coordinates where center is origin (since we only care about distance, use abs)
        x: int = abs(self.v[0] - center[0])
        y: int = abs(self.v[1] - center[1])
        percent_cover /= 100

        #equation for an ellipse. Multiplying the images aspect ratio stretches the ellipse to match the ratio of the image
        dist_from_center: float = math.sqrt((x**2)+((y*aspect_ratio)**2))

        gradient_start_dist = (1-percent_cover)*(dist_to_edge)
        dist_from_gradient_start = dist_from_center - gradient_start_dist

        #use percent_cover as a percent of the distance from the edge to the center
        if(dist_from_gradient_start >= 0):
            #apply darkening function
            change = int(gradient_coeffiecient*(dist_from_gradient_start))
            self.changeBrightness(-change)

            '''# percent of the way from the grad start to the edge
            change = dist_from_gradient_start/(dist_to_edge-gradient_start_dist)
            change *= gradient_coeffiecient

            self.changeColor(int((color[0]-self.r())*change), int((color[1]-self.g())*change), int((color[2]-self.b())*change))'''
        
    def setColor(self, r: int, g: int, b: int) -> None:
        self.v[2] = r
        self.v[3] = g
        self.v[4] = b
    
    def setGray(self, value: int) -> None:
        self.setColor(value, value, value)

    def changeColor(self, delta_r: int, delta_g: int, delta_b: int) -> None:
        self.v[2] += delta_r
        self.v[3] += delta_g
        self.v[4] += delta_b

    #getters and setters
    def x(self) -> int:
        return self.v[0]
    
    def y(self) -> int:
        return self.v[1]
    
    def r(self) -> int:
        return self.v[2]
    
    def set_r(self, R: int) -> None:
        self.v[2] = R
    
    def g(self) -> int:
        return self.v[3]

    def set_g(self, G: int) -> None:
        self.v[3] = G

    def b(self) -> int:
        return self.v[4]
    
    def set_b(self, B: int) -> None:
        self.v[4] = B