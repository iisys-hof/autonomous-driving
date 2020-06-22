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

import time
import json

initTime = time.time()

class TimeMeasurement:

    def __init__ (self, moduleName, roundsToMeasure = 100):
        self.startTime = time.time()
        self.times = {}
        self.lastMeasurement = None
        self.roundsToMeasure = roundsToMeasure
        self.round = 0
        self.moduleName = moduleName
        self.lastTimeFpsShortTime = time.time()
        self.lastTimeRounds = 0

    def __call__(self, measurement):
        self.next(measurement)

    def next(self, measurement):
        self.stop()
        self.start(measurement)

    def start(self, measurement):
        self.lastMeasurement = measurement
        self.startTimeLastMeasurement = time.time()

    def stop(self):
        if self.lastMeasurement is None:
            self.firstMeasurementTime = time.time()
            return
        if self.lastMeasurement not  in self.times:
            self.times[self.lastMeasurement]=0

        self.times[self.lastMeasurement] += time.time() - self.startTimeLastMeasurement

    def __str__(self):
        self.round+=1
        if self.round % self.roundsToMeasure != 0:
            return ''
        text = '################################\n'
        text += 'Times from ' +self.moduleName +'\n'
        text += '################################\n'
        text += 'Total Rounds: ' + str(self.round) + '\n'
        text += 'Total Round Time: ' + str(round(self.getTotalRoundTime(),2)) + '\n'
        text += 'FPS: ' + str(self.getFps()) + '\n'
        text += 'FPS live: ' + str(self.getFpsShortTime()) + '\n'
        text += 'Init Time: ' + str(self.getInitTime()) + '\n'
        text += 'Startup Time: ' + str(self.getStartupTime()) + '\n'
        text += 'Not measured Time: ' + str(self.getNotMeasuredTime()) + '\n'
        text += json.dumps(self.transformInPercent(), indent=4) + '\n'
        text += json.dumps(self.transformAbsolut(), indent=4)
        text += '\n################################\n'
        return text

    def transformInPercent(self):
        measurements = self.times
        totalTime = sum(measurements.values())
        percentMeasurements = {key: round(value *100 / totalTime,3) for (key,value) in measurements.items()}
        percentMeasurementsSorted = {k: str(v) +'%' for k, v in sorted(percentMeasurements.items(), key=lambda item: item[1], reverse=True)}
        return percentMeasurementsSorted

    def transformAbsolut(self):
        measurements = self.times
        AbsolutMeasurements = {key: round(value,3) for (key,value) in measurements.items()}
        AbsolutMeasurementsSorted = {k: str(v) +'s' for k, v in sorted(AbsolutMeasurements.items(), key=lambda item: item[1], reverse=True)}
        return AbsolutMeasurementsSorted


    def getFps(self):
        totalTime = self.getTotalRoundTime()
        fps = self.round/totalTime
        fpsRounded = round(fps,2)
        return fpsRounded

    def getFpsShortTime(self):
        now = time.time()
        totalTime = now - self.lastTimeFpsShortTime
        rounds = self.round - self.lastTimeRounds
        fps = rounds/totalTime
        fpsRounded = round(fps,2)
        self.lastTimeFpsShortTime = now
        self.lastTimeRounds = self.round
        return fpsRounded

    def getStartupTime(self):
        startupTime = self.firstMeasurementTime - self.startTime
        startupTimeRounded = round(startupTime,2)
        return startupTimeRounded

    def getNotMeasuredTime(self):
        totalTime = self.getTotalRoundTime()
        notMeasuredTime = time.time() - totalTime - self.firstMeasurementTime
        notMeasouredTimeRounded = round(notMeasuredTime,2)
        return notMeasouredTimeRounded

    def getInitTime(self):
        init = self.startTime - initTime
        initTimeRounded = round(init,2)
        return initTimeRounded

    def getTotalRoundTime(self):
        totalTime = sum(self.times.values())
        return totalTime