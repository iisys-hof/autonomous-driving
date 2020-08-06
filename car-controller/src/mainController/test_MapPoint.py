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


import unittest

import numpy as np

from AreaMap.MapPoint import MapPoint


class TestMapPoint(unittest.TestCase):

    def test_fullCircle(self):
        point = MapPoint(0,0,0)
        endPoint = point.getEndpoint(1, 2*np.pi)
        self.assertEqual( point,endPoint)

    def test_halfCircle(self):
        point = MapPoint(0,0,0)
        endPoint = point.getEndpoint(1, np.pi)
        print(endPoint)
        self.assertEqual( MapPoint(2,0,np.pi),endPoint)


    def test_negativHalfCircle(self):
        point = MapPoint(0,0,0)
        endPoint = point.getEndpoint(-1, np.pi)
        
        self.assertEqual( MapPoint(-2,0,np.pi),endPoint)

    def test_rotaitionHalfCircle(self):
        point = MapPoint(0,0,np.pi)
        endPoint = point.getEndpoint(1, np.pi)
        self.assertEqual( MapPoint(-2,0,2*np.pi),endPoint)
