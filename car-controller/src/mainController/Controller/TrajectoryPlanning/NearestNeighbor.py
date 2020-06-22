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

import numpy as np
from sklearn.neighbors import KDTree


class NearestNeighbor:

    def getNearestNeighbor(self,left,right):
        nearestNeighbor = {}
        dataRight = np.array([[lm['x'], lm['y']]for lm in right])
        dataLeft = np.array([[lm['x'], lm['y']]for lm in left])

        rightTree = KDTree(dataRight, leaf_size=2)
        index = rightTree.query(dataLeft, k=1, return_distance = False)
        for indexLeft, indexRight in enumerate(index):
            l = indexLeft
            r = indexRight[0]
            nearestNeighbor[(l, r)] = self.getCentralPoint(l,r, dataLeft, dataRight)

        leftTree = KDTree(dataLeft, leaf_size=2)
        index = leftTree.query(dataRight, k=1, return_distance = False)
        for indexRight, indexLeft in enumerate(index):
            l = indexLeft[0]
            r = indexRight
            nearestNeighbor[(l, r)] = self.getCentralPoint(l,r, dataLeft, dataRight)
        return nearestNeighbor

    def getCentralPoint(self,l,r, dataLeft, dataRight):
        return self.getPercentPoint(l,r, dataLeft, dataRight,0.5)

    def getPercentPoint(self, l,r, dataLeft, dataRight, percent):
        invPercent = 1-percent
        return [dataLeft[l][0]*percent + dataRight[r][0]*invPercent,dataLeft[l][1]*percent + dataRight[r][1]*invPercent]
