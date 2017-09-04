/**
 * This sketch will handle the communication between an external data source 
 * and the LED strip. It must be given a serial input in the form 
 * mode,red,green,blue 
 * 
 * After receiving this valid input, it will write to the pixel strip 
 * and display the updated colors.
 */

#include <Adafruit_NeoPixel.h>

#define PIN            8
#define NUMPIXELS      60

Adafruit_NeoPixel pixels[] = {Adafruit_NeoPixel(NUMPIXELS, 9, NEO_GRB + NEO_KHZ800)};
uint32_t lightstrip [NUMPIXELS];

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  for (int i=0; i < sizeof(pixels); i++){
    // Set all the pixels to red 
    uint32_t red = pixels[i].Color(255,0,0); 
    for (int i=0; i<NUMPIXELS; i++) {
      lightstrip[i] = red;
    }
    pixels[i].begin(); // This initializes the NeoPixel library
    updateLightStrip(i, 255,0,0);
    pixels[i].show();
  }
}

void loop() {
  /**
   * Serial data MUST come in the form <pin>,<mode>,255,0,0
   */
   Serial.flush();
   if (Serial.available() > 0) {
      int pin = Serial.parseInt();
      int mode = Serial.parseInt(); // not used currently
      int red = Serial.parseInt();
      int green = Serial.parseInt();
      int blue = Serial.parseInt();
      if (isValidRGB(red) && isValidRGB(green) && isValidRGB(blue)) {
        updateLightStrip(pin, red, green, blue);
      }
   }
}

bool isValidRGB(int color){
  if (color >= 0 && color <= 255){
    return true;
  }else{
    return false;
  }
}

bool updateLightStrip(int pin, int red, int green, int blue){
  // shift existing colors in array
  for (int i = NUMPIXELS-1; i > 0; i--) {
    lightstrip[i] = lightstrip[i-1];
  }
  // Add the new color to the beginning
  lightstrip[0] = pixels[0].Color(red, green, blue);
   
   // set pixels to the new colors
   for(int i = 0; i < NUMPIXELS; i++){
    pixels[pin].setPixelColor(i, lightstrip[i]);
  }
  pixels[pin].show(); // This sends the updated pixel color to the hardware.
  return true;
}

