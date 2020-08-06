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


from Camera.LocalFileStream import LocalFileStream
from MainController import MainController

basePath = 'D:/Projekte/'
localPath = 'autonomous-driving/pylon-images/driving/dataset1/'
imagePath = basePath + localPath

localFileStream = LocalFileStream(imagePath)
stream = localFileStream.run()
angleWidthCamera = localFileStream.getAngleWidth()
mainController = MainController(angleWidthCamera)
mainController.run(stream)
