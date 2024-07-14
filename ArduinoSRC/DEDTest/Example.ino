#include <LiquidCrystal.h>
#define DCSBIOS_DEFAULT_SERIAL
#include "DcsBios.h"

// Initialize the library by associating any needed LCD interface pin
// with the Arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Define the pin for the joystick button
const int buttonPin = 6;

DcsBios::Switch2Pos icpBtn6("ICP_BTN_6", buttonPin);
DcsBios::Potentiometer icpHudBrtKnb("ICP_HUD_BRT_KNB", A0);

void setup() {
  // Set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Initialize serial communication:
  
  // Print initial messages to the LCD:
  lcd.setCursor(0, 0);

  lcd.print("Waiting for data");
  Serial.begin(250000);

}

void loop() {
  
  
  static String incomingString = "";
  static boolean newData = false;

  // Check if data is available to read
  while (Serial.available() > 0 && newData == false) {
    char incomingChar = Serial.read();
    //Serial.print(incomingChar);  
    // Print each received character to the Serial Monitor for debugging
    if (incomingChar == '\n') {
      newData = true;
    } else {
      incomingString += incomingChar;
    }
  }

  // If a new message is available
  if (newData) {

    int separatorIndex = incomingString.indexOf(',');
    if (separatorIndex != -1) {
      String line1 = incomingString.substring(0, separatorIndex);
      String line2 = incomingString.substring(separatorIndex + 1);

      // Display the lines on the LCD
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(line1);
      lcd.setCursor(0, 1);
      lcd.print(line2);
    } else {
      // If no separator is found, display the incoming string on the first line
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(incomingString);
      lcd.setCursor(0, 1);
      lcd.print("");
    }

    // Clear the incomingString and reset newData flag
    incomingString = "";
    newData = false;

  }
  // Poll inputs for DCS BIOS
  DcsBios::PollingInput::pollInputs();
}
