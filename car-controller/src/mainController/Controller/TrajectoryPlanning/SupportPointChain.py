# Copyright 2020 @PascalPuchtler

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

import networkx as nx

from scipy.spatial import distance_matrix
import numpy as np
from sklearn.neighbors import NearestNeighbors

from Controller.AreaMap.MapPoint import MapPoint


class SupportPointChain:
    def __init__ (self, minPointDistance = 0.3):
        self.minPointDistance = minPointDistance

    def getSupportPointChain(self,supportPoints, robotPosition):
        robotPositionArray = np.array( [robotPosition.x, robotPosition.y])
        supportPoints = np.array(list(supportPoints.values()))
        supportPoints = np.concatenate( [[robotPositionArray], supportPoints])

        optimalChain = self.getShortesPath(supportPoints, robotPosition)
        return optimalChain

    def getShortesPath(self,supportPoints, robotPosition):
        nearestNeighbourGraph = self.getNearesNeighboursGraph(supportPoints)
        shortestPaths = self.getShortestPathToEveryPoint(nearestNeighbourGraph,0)
        shortestPathsRightDirection = self.filterShortestPathsToRightDirection(robotPosition, shortestPaths, supportPoints)
        shortestPath = self.getLongestPath(shortestPathsRightDirection)
        realPath = supportPoints[shortestPath]
        realPath = self.dropoutToShortDistances(realPath,self.minPointDistance)
        return realPath

    def getShortestPathToEveryPoint(self, nearestNeighbourGraph, startIndex):
        shortestPaths = nx.single_source_dijkstra_path(nearestNeighbourGraph, startIndex)
        return shortestPaths

    def filterShortestPathsToRightDirection(self,robotPosition, shortestPaths,supportPoints):
        shortestPathsRightDirection = [path  for (target,path)in shortestPaths.items() if self.isPathInDriveDirection(robotPosition,supportPoints[path])]
        return shortestPathsRightDirection

    def getLongestPath(self, graphs):
        if len(graphs) == 0:
            return []
        elements = [len(g) for g in graphs]
        maxIndex = np.argmax(elements)
        return graphs[maxIndex]

    def dropoutToShortDistances(self, path, minPointDistance):
        while True:
            distances = ((path[:-1]-path[1:])**2).sum(1)
            position = np.argwhere(distances<minPointDistance)
            if len(position) ==0:
                break
            if position[0][0]+2 ==len(path):
                break
            path = np.delete(path, position[0][0]+1, axis = 0)
            
        return path

    def isPathInDriveDirection(self,robotPosition, path):
        if len(path)<=1:
            return False
        return self.isPointInDriveDirection(robotPosition,path[1])


    def isPointInDriveDirection(self, robotPosition, targetPoint):
        if targetPoint is None:
            return False
        
        distance = robotPosition.getRelativeOffsetsToPoint(targetPoint[0], targetPoint[1])
        return distance[1]>0

    def getNearesNeighboursGraph(self, supportPoints):
        exponent = 4
        distances = distance_matrix(supportPoints,supportPoints)**exponent
        return nx.from_numpy_matrix(distances)

