#include "HX711.h"

// HX711 wiring
const int LOADCELL_DOUT_PIN = 21;
const int LOADCELL_SCK_PIN = 20;

const int PIN_ONE_LID = 17;
const int PIN_MULTIPLE_LIDS = 16;

HX711 scale;

float calibration_factor = 1500 / 2.0;

// State tracking
bool wasAnyPinHigh = false;
bool tareInProgress = false;

void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(calibration_factor);
  scale.tare();

  pinMode(PIN_ONE_LID, OUTPUT);
  pinMode(PIN_MULTIPLE_LIDS, OUTPUT);

  digitalWrite(PIN_ONE_LID, LOW);
  digitalWrite(PIN_MULTIPLE_LIDS, LOW);
}

void loop() {
  if (scale.is_ready()) {
    float weight = scale.get_units(4);
    Serial.print("Weight: ");
    Serial.print(weight);
    Serial.println(" grams");

    // Set pin outputs based on weight
    if (weight < 2.8 && weight > 1.0) {
      digitalWrite(PIN_ONE_LID, HIGH);
      digitalWrite(PIN_MULTIPLE_LIDS, LOW);
      Serial.println("1 lid detected");
    } else if (weight > 2.7) {
      digitalWrite(PIN_ONE_LID, LOW);
      digitalWrite(PIN_MULTIPLE_LIDS, HIGH);
      Serial.println("2+ lids detected");
    } else {
      digitalWrite(PIN_ONE_LID, LOW);
      digitalWrite(PIN_MULTIPLE_LIDS, LOW);
      Serial.println("No lids detected");
    }

    // Read current pin states
    int stateOneLid = digitalRead(PIN_ONE_LID);
    int stateMultipleLids = digitalRead(PIN_MULTIPLE_LIDS);

    // Check if any pin was HIGH in the last loop
    if (stateOneLid == HIGH || stateMultipleLids == HIGH) {
      wasAnyPinHigh = true;
    }

    // Now check if both pins are LOW after being HIGH before
    if (wasAnyPinHigh && stateOneLid == LOW && stateMultipleLids == LOW && !tareInProgress) {
      // Trigger tare sequence
      Serial.println("Taring in 5 seconds...");
      tareInProgress = true; // Prevent retriggering during delay
      delay(5000);
      scale.tare();
      Serial.println("Scale tared.");
      wasAnyPinHigh = false;
      tareInProgress = false;
    }

    // Optional debug
    Serial.print("PIN_ONE_LID state: ");
    Serial.println(stateOneLid);
    Serial.print("PIN_MULTIPLE_LIDS state: ");
    Serial.println(stateMultipleLids);

  } else {
    Serial.println("Scale not ready.");
  }

  delay(100); // Loop pacing
}
