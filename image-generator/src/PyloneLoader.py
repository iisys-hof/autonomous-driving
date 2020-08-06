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

from ImageLoader import ImageLoader
import numpy as np

class PyloneLoader:
    def __init__(self, pylonsPaths):
        self.imageLoader = ImageLoader()
        self.pylons = self.loadPylons(pylonsPaths)

    def loadPylons(self, pylons):
        for color in pylons:
            color['images'] = self.imageLoader.loadImagesFromPath(color['path'])
        return pylons

    def getRandomPylon(self):
        choice = np.random.randint(0,len(self.pylons))
        color = self.pylons[choice]
        return self.randomImage(color['images']), color['label']


    def __str__(self):
        pyloneCounts = ['#' + color['label']+ ': ' + str(len(color['images'] ))for color in self.pylons]
        return '\n'.join(pyloneCounts)

    def randomImage(self, images):
        choice = np.random.randint(0,len(images))
        return images[choice]
