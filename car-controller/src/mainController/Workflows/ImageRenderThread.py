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


import threading
import queue
from CrossCutting.IterableQueue.IterableQueue import IterableQueue

from View.Render.RenderImage import RenderImage

class ImageRenderThread(threading.Thread):
    def __init__(self, videoInformationQueue):
        super(ImageRenderThread, self).__init__()
        self.imageMapper = RenderImage()
        self.sendQueueFrame = queue.Queue(maxsize = 1)
        self.videoInformationQueue = videoInformationQueue
        

    def getRenderedQueue(self):
        return self.sendQueueFrame

    def run(self):
        self.imageRenderer()

    def imageRenderer(self):
        for imgColor, pylons, areaMap, trajectoryPlanning, angleWidthCamera in IterableQueue(self.videoInformationQueue):
            completeImage = self.imageMapper.getFrame(imgColor, pylons, areaMap, trajectoryPlanning, angleWidthCamera)
            if not self.sendQueueFrame.full():
                self.sendQueueFrame.put_nowait(completeImage)
