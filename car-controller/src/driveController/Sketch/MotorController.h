// Copyright 2020 @PascalPuchtler

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

#ifndef MotorController_H
#define MotorController_H

#include "Arduino.h"
#include <PololuQik.h>

class MotorController{
    private:
      PololuQik2s12v10 *motorController;
    public:
      MotorController();
      void setSpeeds(int m0, int m1);
};
#endif
