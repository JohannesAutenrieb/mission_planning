"""
frame_module.py contains functions to convert between local battlefield
co-coordinates and GPS co-coordinates
"""
import os
import time
import numpy as np
from pyproj import Proj


class FrameConvertor:
    def __init__(self):
        # Read battlefield waypoints from file
        f = open(self.getRelativeFilePath("Battlefield.txt"))
        lines = f.readlines()
        f.close()

        x0y0_GPS = np.array([float(i) for i in lines[0].split(',')])
        x100y0_GPS = np.array([float(i) for i in lines[1].split(',')])
        #x0y100_GPS = np.array([float(i) for i in lines[2].split(',')])
        #x100y100_GPS = np.array([float(i) for i in lines[3].split(',')])

        self.world = Proj(proj='tmerc', lon_0=x0y0_GPS[1], lat_0=x0y0_GPS[0], ellps='airy')
        #self.x_off,self.y_off = self.world(0,0,inverse=True)

        #x0y0_lcl = self.world(x0y0_GPS[1],x0y0_GPS[0])
        x100y0_lcl = list(self.world(x100y0_GPS[1],x100y0_GPS[0]))
        #x0y100_lcl = self.world(x0y100_GPS[1],x0y100_GPS[0])
        #x100y100_lcl = self.world(x100y100_GPS[1],x100y100_GPS[0])

        self.tilt = np.arctan2(x100y0_lcl[1],x100y0_lcl[0])


    def localToWorldFrame(self,pos):
        ''' To convert from the local battlefield coordinates to GPS'''
        lon, lat = self.world(pos[0],pos[1],inverse=True)   # For AIRY ellipse

        worldPos = [lat, lon, pos[2]]

        return worldPos


    def worldToLocalFrame(self,gps,orient):
        ''' To convert from GPS to the local battlefield coordinates'''
        x,y = self.world(gps[1], gps[0])    # For AIRY ellipse

        localPos = [x, y, gps[2]]
        localHead = orient - self.tilt

        return localPos,localHead


    def getRelativeFilePath(self, relativePath):
        scriptDir = os.path.dirname(__file__)
        absFilePath = os.path.join(scriptDir, relativePath)
        return absFilePath

if __name__ == "__main__":

    convertor = FrameConvertor()
    inputFilenames = ["takeoff_local.txt", "round1_landing_local.txt", "round2_landing_local.txt","round3_landing_local.txt"]
    outputFilenames = ["takeoff_global.txt", "round1_landing_global.txt", "round2_landing_global.txt",
                      "round3_landing_global.txt"]

    for i in range(0,len(inputFilenames)):
        f = open(convertor.getRelativeFilePath(inputFilenames[i]))
        lines = f.readlines()
        f.close()
        f = open(convertor.getRelativeFilePath(outputFilenames[i]), 'a')

        for i in range(0, len(lines)):
            line = lines[i].split(" ")
            del line[-1]  # delete last element with new line command
            id = line[0]
            localwaypoint[0] = line[1]
            localwaypoint[0] = line[2]
            localwaypoint = [float(x) for x in localwaypoint]
            globalwaypoint = convertor.localToWorldFrame(localwaypoint)
            f.write("%s %6.4f %6.4f" % (id, globalwaypoint[0], globalwaypoint[1]))
        f.close()


