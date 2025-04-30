#include "HX711.h"

// HX711 circuit wiring (right-hand side pins)
const int LOADCELL_DOUT_PIN = 16;  // GPIO16 (physical pin 21)
const int LOADCELL_SCK_PIN = 17;   // GPIO17 (physical pin 22)

// Output pins (same side as above)
const int PIN_ONE_LID = 18;         // GPIO18 (physical pin 18)
const int PIN_MULTIPLE_LIDS = 20;   // GPIO19 (physical pin 20)

HX711 scale;

// Calibration factor obtained from calibration process
float calibration_factor = 1500 / 2.0; // Adjust this as needed

void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor); // Set the calibration factor
  scale.tare(); // Reset scale to zero

  pinMode(PIN_ONE_LID, OUTPUT);
  pinMode(PIN_MULTIPLE_LIDS, OUTPUT);

  // Ensure both outputs are LOW at start
  digitalWrite(PIN_ONE_LID, LOW);
  digitalWrite(PIN_MULTIPLE_LIDS, LOW);
}

void loop() {
  if (scale.is_ready()) {
    float weight = scale.get_units(4); // Get weight measurement
    Serial.print("Weight: ");
    Serial.print(weight);
    Serial.println(" grams");

    if (weight < 2.8 && weight > 1.0) {
      digitalWrite(PIN_ONE_LID, HIGH);
      digitalWrite(PIN_MULTIPLE_LIDS, LOW);
      Serial.println("1 lid detected");
    } else if (weight > 2.7){
      digitalWrite(PIN_ONE_LID, LOW);
      digitalWrite(PIN_MULTIPLE_LIDS, HIGH);
      Serial.println("2 + lids detected");
    }
      else if (weight < 1.0){
      digitalWrite(PIN_ONE_LID, LOW);
      digitalWrite(PIN_MULTIPLE_LIDS, LOW);
      Serial.println("No lids detected");
    }
  } else {
    Serial.println("No lid detected");
    digitalWrite(PIN_ONE_LID, LOW);
    digitalWrite(PIN_MULTIPLE_LIDS, LOW);
  }

  delay(100); // Slight delay for stable readings
}
