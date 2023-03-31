#include <Adafruit_PCD8544.h>

// Pin definitions
#define SCLK 18
#define DIN 23
#define DC 19
#define CS 5
#define RST 17

// Create an instance of the PCD8544 class
Adafruit_PCD8544 display = Adafruit_PCD8544(SCLK, DIN, DC, CS, RST);

void setup() {
  // Initialize the display
  display.begin();

  // Set the contrast of the display
  display.setContrast(50);

  // Clear the display
  display.clearDisplay();
  
}

int i=65;//simulated speedometer
void loop() {
  // Set the cursor to (0, 0)
  display.setCursor(0, 0);

  // Print "Hello, world!"
  // display.println("L            R\n\n\n        65km/h");
  display.println("L            R\n\n\n        ");
  delay(600);
  display.println(i++);
  display.print("km/h");
  // Display the contents of the buffer
  display.display();
  display.clearDisplay();
}
