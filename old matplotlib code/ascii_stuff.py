from PIL import Image, ImageDraw
import time
import os
import numpy as np

## vars
"""


"""
console_size_full = (200, 32)
console_size = tuple(i - 1 for i in console_size_full) # BORDERS
font_width = 0.55 # compared to height (usually given percentage, here decimal)
calculate_resolution = 2 # factor to muitlply the image size by for calcs and PIL
max_time = 100 # seconds

impact_coeff = 0.85 # remaining percentage of v after impact

##
new_size = (
    int(console_size[0] * calculate_resolution),
    int(console_size[1] * calculate_resolution / font_width)
)

def setTime():
    global start_time
    start_time = time.time()

def refresh():
    os.system('cls')

class frame:
    def __init__(self) -> None:
        self.im = Image.new('P', new_size, color = 255)
        self.draw = ImageDraw.Draw(self.im)

    def convCoords(self, coords):
        # changes from normal cartesian (origin at lower left)
        # to PIl format
        return (
            coords[0],
            new_size[1] - 1 - coords[1]
        )

    def convBoundingBox(self, coords):
        return [
            coords[0],
            new_size[1] - 1 - coords[1],
            coords[2],
            new_size[1] - 1 - coords[3]
        ]

    def renderASCII(self):
        self.im = self.im.resize(console_size)

        frame = ""

        for y in range(console_size[1]):
            for x in range(console_size[0]):
            
                pixel = self.im.getpixel((x, y))
                if pixel < 128:
                    frame += "8"
                else:
                    frame += " "

                if x == console_size[0] - 1: # right border
                    frame += "0"

            frame += "\n"

        for i in range(console_size_full[0] - 1) : # lower border
            frame += "/"

        frame += "8"

        refresh()
        print(frame)


    def circle(self, center = (0,0), radius = 0, outline = 0, fill = 0, width = 1):    
        nc = self.convCoords(tuple(int(i) for i in center))
        x0 = max(nc[0] - radius, 0)
        y0 = max(nc[1] - radius, 0 )
        x1 = min(nc[0] + radius - 1, new_size[0])
        y1 = min(nc[1] + radius - 1, new_size[1])

        self.draw.ellipse(
            [x0, y0, x1, y1],
            fill = fill,
            outline = outline,
            width = width
        )

        del nc, x0, y0, x1, y1

    
    def circ_alt(self, xy = [0,0,0,0], outline = 0, fill = 0, width = 1):      
        # ellipses are broken lmao
        nc = self.convBoundingBox(list(int(i) for i in xy))
        x0 = max(nc[0], 0)
        y0 = max(nc[1], 0 )
        x1 = min(nc[2], new_size[0])
        y1 = min(nc[3], new_size[1])

        #print([x0, y0, x1, y1])

        self.draw.ellipse(
           [x0, y0, x1, y1],
            fill = fill,
            outline = outline,
            width = width
        )
        

        del nc, x0, y0, x1, y1
    
    def rect(self, xy = [0,0,0,0], outline = 0, fill = 0, width = 1):      
        self.draw.rectangle(
            xy = self.convBoundingBox(list(int(i) for i in xy)),
            fill = fill,
            outline = outline,
            width = width
        )

    def show(self):
        self.im.show()

    def smt(self):
        pass


### stuff for calculating drag.
def air_density(h): ##below 11km https://en.wikipedia.org/wiki/Barometric_formula
    return 1.2250 * ( 288.15 / (288.15 - 0.0065 * h )) ** -4.2557877405521705 ##(1 + (9.80665 * 0.0289644 / 8.3144598 / -0.0065))

m = 113100 # 1000 kg/cbm for a 6m diam sphere
As = 28.3 # sphere with diameter 6
Cd = 0.5 # sphere

def animate():
    frame_count = 0
    running = True
    crtime = time.time() - start_time
    prev_time = time.time() - start_time
    dt = 0.001 # temp, may change

    # UNIT CONVERSION - to do at some point.
    box_pos = [10, 10]
    #box_a = [0, -9.81]
    g = 9.81
    
    box_v = [450, 905]
    box_size = [6, 6]

    hit_times = 0
    prev_hit = False

    while running == True and crtime <= max_time and hit_times < 36:
        #unit conversions,
        
        
        prev_time = time.time() - start_time
        time.sleep(0.00001)
        frame_count += 1
        # can do a func, easier for the first round.
        # somehow quite difficult, and I'm tred
        

        ### simulation code
        #box_v = [ box_v[0] + box_a[0] * dt, box_v[1] + box_a[1] * dt ]

        #### DRAG CODE
        theta1 = np.arctan( box_v[1] / box_v[0] )
        v = np.sqrt( box_v[1] ** 2 + box_v[0] ** 2 )
        FD = 0.5 * air_density(box_pos[1]) * v ** 2 * As * Cd
        FDx = FD * np.cos(theta1)
        FDy = FD * np.sin(theta1)

        ax = FDx / m
        ay = FDy / m

        dsx = box_v[0] * dt - 1/2 * ax * dt ** 2
        dsy = box_v[1] * dt - 1/2 * ay * dt ** 2

        box_pos = [box_pos[0] + dsx, box_pos[1] + dsy]

        box_v[0] = box_v[0] - ax * dt
        box_v[1] = box_v[1] - ay * dt - g
        ####

        #box_pos = [box_pos[0] + box_v[0] * dt, box_pos[1] + box_v[1] * dt]

        ## code to test bouncing off the edge
        if box_pos[0] + box_size[0] > new_size[0] or box_pos[0] < 0:
            
            if not prev_hit:
                box_v[0] = -1 * box_v[0] * impact_coeff
                hit_times += 1
            prev_hit = True
            
            
        elif box_pos[1] + box_size[1] > new_size[1] or box_pos[1] < 0:
            
            if not prev_hit:
                box_v[1] = -1 * box_v[1] * impact_coeff
                hit_times += 1
            prev_hit = True


        else:
            prev_hit = False

        newframe = frame()
        newframe.rect(xy=[
            box_pos[0],
            box_pos[1],
            box_pos[0] + box_size[0],
            box_pos[1] + box_size[1]
        ])
        ###

        

        newframe.renderASCII()

        crtime = time.time() - start_time
        dt = crtime - prev_time
        #breakpoint()
        
        ## DATA output
        print("Time elapsed: {:.3f}s | Frame {} | Frametime: {:.2f}ms (avr: {:.2f}ms) | {:.2f}fps".format(
            crtime,
            frame_count,
            dt * 1000, 
            crtime / frame_count * 1000, 
            1/dt
        ))
        print("Horizontal Velocity: {:.2f}px/s | Acceleration: {:.2f}px/s^2".format(
            box_v[0],
            ax
        ))
        print("Vertical Velocity: {:.2f}px/s | Acceleration: {:.2f}px/s^2".format(
            box_v[1],
            ay
        ))
        print("Impact count: " +str(hit_times))
        ##


def animate2():
    frame_count = 0
    running = True
    crtime = time.time() - start_time
    prev_time = time.time() - start_time
    dt = 0.001 # temp, may change

    # UNIT CONVERSION - to do at some point.
    box_pos = [200, 50] # new equilbirum point
    equliibrium = 200
    # 1st number is the position to care about
    #box_a = [0, -9.81]
    g = 9.81
    
    box_v = [250, 0]
    box_size = [6, 6]
    angular_freq = 3
    a = 0

    hit_times = 0
    prev_hit = False

    while running == True and crtime <= max_time:
        #unit conversions,
        
        
        prev_time = time.time() - start_time
        time.sleep(0.00001)
        frame_count += 1
        # can do a func, easier for the first round.
        # somehow quite difficult, and I'm tred
        

        ### simulation code
        #box_v = [ box_v[0] + box_a[0] * dt, box_v[1] + box_a[1] * dt ]

        #### 
        a = - angular_freq**2 * (box_pos[0] - equliibrium)
        box_v[0] = box_v[0] + a * dt
        box_pos[0] = box_pos[0] + box_v[0] * dt
        

        if box_pos[0] + box_size[0] > new_size[0] or box_pos[0] < 0:
            
            if not prev_hit:
                box_v[0] = -1 * box_v[0] * impact_coeff
                hit_times += 1
            prev_hit = True
            
            
        elif box_pos[1] + box_size[1] > new_size[1] or box_pos[1] < 0:
            
            if not prev_hit:
                box_v[1] = -1 * box_v[1] * impact_coeff
                hit_times += 1
            prev_hit = True


        else:
            prev_hit = False

        newframe = frame()
        newframe.rect(xy=[
            box_pos[0],
            box_pos[1],
            box_pos[0] + box_size[0],
            box_pos[1] + box_size[1]
        ])
        ###
        newframe.renderASCII()

        crtime = time.time() - start_time
        dt = crtime - prev_time
        #breakpoint()
        
        ## DATA output
        print("Time elapsed: {:.3f}s | Frame {} | Frametime: {:.2f}ms (avr: {:.2f}ms) | {:.2f}fps".format(
            crtime,
            frame_count,
            dt * 1000, 
            crtime / frame_count * 1000, 
            1/dt
        ))
        print("Horizontal Velocity: {:.2f}px/s | Acceleration: {:.2f}px/s^2".format(
            box_v[0],
            a
        ))
        print("Impact count: " +str(hit_times))
        ##

if __name__ == "__main__":
    setTime()

    animate()

    input()
