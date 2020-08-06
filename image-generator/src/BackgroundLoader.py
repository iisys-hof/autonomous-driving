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

class BackgroundLoader:
    def __init__(self, backgroundPath):
        self.imageLoader = ImageLoader()
        self.backgrounds = self.imageLoader.loadImagesFromPath(backgroundPath)

    def getRandomBackground(self):
        return self.randomImage(self.backgrounds)

    def __str__(self):
        return '#backgrounds: ' + str(len(self.backgrounds))

    def randomImage(self, images):
        choice = np.random.randint(0,len(images))
        return images[choice]
