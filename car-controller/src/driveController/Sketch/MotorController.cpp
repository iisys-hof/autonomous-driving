// @PascalPuchtler

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ==============================================================================

#include "MotorController.h"
#include "PinAssignment.h"

MotorController::MotorController() {
    motorController = new PololuQik2s12v10(PinAssignment::motorTx,PinAssignment::motorRx,PinAssignment::motorReset);
    motorController->begin(9600);     // Verbindung zu MotorController
    motorController->init(); 
}

void MotorController::setSpeeds(int m0, int m1) {
  m0 = constrain(m0,-100,100);
  m1 = constrain(m1,-100,100);
  motorController->setSpeeds(m1, m0);
}