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

#include "SonicController.h"
#include "PinAssignment.h"


int SonicController::getLeft()
{
  return getDistance(PinAssignment::ultrasonicLeft);
}

int SonicController::getRight()
{
  return getDistance(PinAssignment::ultrasonicRight);
}

int SonicController::getMiddle()
{
  return getDistance(PinAssignment::ultrasonicMiddle);
}

/*
   Methode zum Berechnen des Abstandes des Ultraschallsensors in cm
*/
int SonicController::getDistance(int sigPin)
{
  // Variablen fÃ¼r die Dauer der Messwerte
  // und der Distanz in Inches und Zentimetern:
  long duration;
  //long inches;
  int cm;

  /** -------------------------------------------------------------------
      Ultraschallsensor misst die Werte ein.
      -------------------------------------------------------------------
  */

  // Es kann ein HIGH Impuls von 2 oder mehr microseconds ausgesendet werden.
  // Damit ein klarer HIGH Impuls ausgesendet werden kann, muss vorher ein LOW Impuls ausgesendet werden.
  pinMode(sigPin, OUTPUT);
  digitalWrite(sigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(sigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(sigPin, LOW);

  // Der selbe Pin wird verwendet, um das Signal einzulesen.
  // Die Dauer (berechnet in microseconds) wird berechnet zwischen dem Aussenden des HIGH-Impuls
  // und dem Eintreffen des Echos auf den Sensor.
  pinMode(sigPin, INPUT);
  duration = pulseIn(sigPin, HIGH, 3000); //max ~50 cm

  if (duration == 0)
    return 0;

  cm = microsecondsToCentimeters(duration);
  return cm;
}

long SonicController::microsecondsToCentimeters(long microseconds)
{
  long value;
  // Zum Berechnen nimmt man an: 340 m/s or 29 microseconds per centimeter
  // Da nur der Abstand wichtig ist, muss der Wert durch 2 geteilt werden.
  value = microseconds / 29 / 2;
  return value;
}