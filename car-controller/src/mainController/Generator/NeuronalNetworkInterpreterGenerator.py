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

class NeuronalNetworkInterpreterGenerator:
    def getInterpreter(self, modelPath, imageScaler):
        try:
            from Controller.NetworkAnalysis.NvidiaInterpreter import NvidiaInterpreter
            interpreter = NvidiaInterpreter(modelPath,imageScaler)
            return interpreter
        except:
            pass

        try:
            from Controller.NetworkAnalysis.CoralInterpreter import CoralInterpreter
            interpreter = CoralInterpreter(modelPath,imageScaler)
            return interpreter
        except:
            pass

        try:
            from Controller.NetworkAnalysis.NCS2Interpreter import NCS2Interpreter
            interpreter = NCS2Interpreter(modelPath,imageScaler)
            return interpreter
        except:
            pass

        from Controller.NetworkAnalysis.CpuInterpreter import CpuInterpreter
        interpreter = CpuInterpreter(modelPath,imageScaler)
        return interpreter