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
#include "SonicController.h"
#include <ArduinoJson.h>

MotorController *motorController;
SonicController *sonicController;
int left =0;
int right = 0;
int middle = 0;



void setup() {
    Serial.begin(9600);
    motorController = new MotorController();
    sonicController = new SonicController();
}


void loop() {
    DynamicJsonDocument inputDocument(2048);
    deserializeJson(inputDocument, Serial);
    if (inputDocument["command"] == "move") {
        motorController->setSpeeds(inputDocument["left"],inputDocument["right"]);
    }
    if (inputDocument["command"] == "sonic") {
    inputDocument["left"] = left;
    inputDocument["right"] = right;
    inputDocument["middle"] =middle;
    serializeJson(inputDocument, Serial);
    Serial.println();
    left= sonicController->getLeft();
    right = sonicController->getRight();
    middle =sonicController->getMiddle();
    }


}
//{"command":"move","left":20,"right":20}
//{"command":"sonic"}