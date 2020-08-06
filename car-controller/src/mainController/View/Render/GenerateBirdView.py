# @PascalPuchtler

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import CubicHermiteSpline as Spline
from CrossCutting.TimeMeasurement.TimeMeasurement import TimeMeasurement

import json
import cv2

class GenerateBirdView:
    def __init__(self):
        self.timeMeasurement = TimeMeasurement("GenerateBirdView", 100)

        self.figure = self.createFigure()

        self.plot = self.createPlot(self.figure)
        self.completeRedraw()
        self.elements = self.initElements(self.plot)
        self.count = 0


    def createFigure(self):
        imH =  480
        imW = 700
        figure = plt.figure(figsize= (imW/100, imH/100))
        return figure

    def createPlot(self, figure):
        plot = figure.add_subplot ( 111 )
        plt.axis("equal")
        plt.axis([-4,4, -1,5])
        plt.grid(True)
        return plot

    def completeRedraw(self):
        self.figure.canvas.draw()
        self.canvasBackup = self.figure.canvas.copy_from_bbox(self.plot.bbox)

    def initElements(self, plot):
        elements = {}
        elements['StartPoint'], = plot.plot(0,0, color='red', marker='s', markersize=10)
        elements['CarPoint'], = plot.plot(1,1, color='black', marker='s', markersize=10)
        elements['CarArrow'] = plot.quiver(0,0,0)
        elements['CarHistory'], = plot.plot(0,0)
        elements['PylonsPosition_b'], = plot.plot(0,0, color='b', marker='.', markersize=20, linestyle = '')
        elements['PylonsPosition_gold'], = plot.plot(0,0, color='gold', marker='.', markersize=20, linestyle = '')
        elements['PylonsPosition_orange'], = plot.plot(0,0, color='orange', marker='.', markersize=20, linestyle = '')
        elements['PylonsIsVisible'], = plot.plot(0,0, color='green', marker='*', markersize=8, linestyle = '')
        elements['PylonsShouldVisible'], = plot.plot(0,0, color='red', marker='*', markersize=8, linestyle = '')
        elements['CameraLeft'], = plot.plot(0,0, color='red', marker='', linewidth = 0.4)
        elements['CameraRight'], = plot.plot(0,0, color='red', marker='', linewidth = 0.4)
        elements['TrajectoryPlanning'], = plot.plot(0,0, color='c', marker='.', markersize=0)
        elements['SupportPointChain'], = plot.plot(0, 0, color = 'gray', marker = '.', markersize = 5, linestyle = ':')
        return elements

    def getFrame(self, imH, imW, areaMap, trajectoryPlanning, angleWidthCamera):
        self.timeMeasurement('add elements')
        plot = self.plot
        self.addCameraView(plot, areaMap.robotPosition, angleWidthCamera)
        self.addPylons(plot, areaMap.left, 'b')
        self.addPylons(plot, areaMap.right, 'gold')
        self.addPylons(plot, areaMap.others, 'orange')
        self.addStartPoint(plot)
        self.addCarHistory(plot, areaMap.robotPositionsHistory, areaMap.robotPosition )
        self.addTrajectoryPlanning(plot, trajectoryPlanning.callculatedNextMove, areaMap.robotPosition )
        self.addCar(plot, areaMap.robotPosition)
        self.printSupportPointChain(plot, trajectoryPlanning.newestSupportChain)

        self.updateElements()
        image = self.renderImage()
        self.timeMeasurement('wait')
        print(self.timeMeasurement, end='')
        return image


    def addCameraView(self,plot, robotPosition, angleWidthCamera):
        distance = 2
        def plotPoint(angle, plotName):
            targetPoint = robotPosition.getAbsolutPointFromRelativeOffset(distance * np.sin(angle), distance * np.cos(angle))
            self.elements[plotName].set_data([robotPosition.x, targetPoint[0]],[robotPosition.y, targetPoint[1]])

        plotPoint(angleWidthCamera/2, 'CameraLeft')
        plotPoint(-angleWidthCamera/2, 'CameraRight')


    def addStartPoint(self,plot,x=0,y=0):
        self.elements['StartPoint'].set_data(x,y)

    def addCar(self,plot, point):
        self.elements['CarArrow'].set_offsets([point.x,point.y])
        self.elements['CarArrow'].set_UVC(np.sin(point.orientation),np.cos(point.orientation))
        self.elements['CarPoint'].set_data(point.x, point.y)

    def addPylons(self, plot, pylons, color):
        self.addPylonsPosition(plot, pylons, color)
        # self.addPylonsCount(plot, pylons)
        self.addPylonsIsVisible(plot, pylons)
        self.addPylonsShouldVisible(plot, pylons)
        
    def addCarHistory(self, plot, robotPositionsHistory, robotPosition):
        xCoordinates=[robotPosition.x for robotPosition in robotPositionsHistory]
        yCoordinates=[robotPosition.y for robotPosition in robotPositionsHistory]
        xCoordinates.append(robotPosition.x)
        yCoordinates.append(robotPosition.y)
        self.elements['CarHistory'].set_data(xCoordinates,yCoordinates)

    def addTrajectoryPlanning(self, plot, curveCommand, robotPosition):
        if curveCommand is not None and curveCommand['x']>0:
            self.spline = Spline([0,curveCommand['x']], [0,curveCommand['y']], [0,curveCommand['m']])
            self.maxPosition = curveCommand['x']

            supportPoints = np.linspace(0, curveCommand['x'], 20)
            targetPoints = self.spline(supportPoints)
            points = [robotPosition.getAbsolutPointFromRelativeOffset(-y,x) for (x,y) in zip(supportPoints,targetPoints)]
            xCoordinates,yCoordinates = zip(*points)
            self.elements['TrajectoryPlanning'].set_data(xCoordinates,yCoordinates)

    def printSupportPointChain(self, plot, supportPointChain):
        if not len(supportPointChain) == 0:
            x = supportPointChain[:,0]
            y = supportPointChain[:,1]
            self.elements['SupportPointChain'].set_data(x,y)

    def addPylonsPosition(self, plot, pylons, color):
        xCoordinates=[pylon['x'] for pylon in pylons]
        yCoordinates=[pylon['y'] for pylon in pylons]
        self.elements['PylonsPosition_' + color].set_data(xCoordinates,yCoordinates)
    
    def addPylonsCount(self, plot, pylons):
        xCoordinates=[pylon['x'] for pylon in pylons]
        yCoordinates=[pylon['y'] for pylon in pylons] 
        count = [json.dumps(pylon['label']) for pylon in pylons]
        
        for i, txt in enumerate(count):
            plot.annotate(txt, (xCoordinates[i], yCoordinates[i]))

    def addPylonsIsVisible(self,plot, pylons):
        xCoordinates = [pylon['x'] for pylon in pylons if pylon['isVisible']]
        yCoordinates=[pylon['y'] for pylon in pylons if pylon['isVisible']]
        self.elements['PylonsIsVisible'].set_data(xCoordinates,yCoordinates)

    def addPylonsShouldVisible(self,plot, pylons):
        xCoordinates = [pylon['x'] for pylon in pylons if pylon['shouldVisible'] and not pylon['isVisible']]
        yCoordinates=[pylon['y'] for pylon in pylons if pylon['shouldVisible'] and not pylon['isVisible']]
        self.elements['PylonsShouldVisible'].set_data(xCoordinates,yCoordinates)


    def updateElements (self):
        self.timeMeasurement('render element update')
        
        self.figure.canvas.restore_region(self.canvasBackup)
        for key, value in self.elements.items():
            self.plot.draw_artist(value)
        
        self.timeMeasurement('full render')
        # self.count +=1
        # if self.count%25 == 0:
        #     self.plot.autoscale_view()
        #     self.plot.relim()
        #     self.completeRedraw()

        self.figure.canvas.blit(self.plot.bbox)


    def renderImage(self):
        self.timeMeasurement('format output')
        # Get the RGBA buffer from the figure
        w,h = self.figure.canvas.get_width_height()
        image = np.fromstring ( self.figure.canvas.tostring_rgb(), dtype=np.uint8 ).reshape(h, w,3)
        image   = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.figure.canvas.flush_events()
        return image
