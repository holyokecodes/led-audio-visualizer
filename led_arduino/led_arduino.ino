/**
 * This sketch will handle the communication between an external data source 
 * and the LED strip. It must be given a serial input in the form 
 * mode,red,green,blue 
 * 
 * After receiving this valid input, it will write to the pixel strip 
 * and display the updated colors.
 */

#include <Adafruit_NeoPixel.h>

#define PIN           6
#define PIN2           7
#define NUMPIXELS      60

int counter = 0; 

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800); 
Adafruit_NeoPixel pixels2 = Adafruit_NeoPixel(NUMPIXELS, PIN2, NEO_GRB + NEO_KHZ800); 

uint32_t lightstrip [NUMPIXELS];

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps

  // Set all the pixels to red 
  pixels.begin(); // This initializes the NeoPixel library
  pixels2.begin();
  updateWholeLightStrip(0, 0, 100);
}

void loop() {
  /**
   * Serial data MUST come in the form <mode>,255,0,0
   */
   Serial.flush();
   if (Serial.available() > 0) {
      int mode = Serial.parseInt(); // not used currently
      int red = Serial.parseInt();
      int green = Serial.parseInt();
      int blue = Serial.parseInt();
      if (isValidRGB(red) && isValidRGB(green) && isValidRGB(blue)) {
        // runner = 0 whole string = 1 image = 2
        if (mode == 1){
          //pixels.setPixelColor(0, pixels.Color(0,0,0));
          updateWholeLightStrip(red, green, blue);
        }else if (mode == 2){
          pixels.setPixelColor(counter, pixels.Color(red, green, blue));
          counter++;
          pixels.show();
          counter = 0;
        }else{
          updateLightStrip(red, green, blue);
        }
       
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

bool updateLightStrip(int red, int green, int blue){
  // shift existing colors in array
  for (int i = NUMPIXELS-1; i > 0; i--) {
    lightstrip[i] = lightstrip[i-1];
  }
  // Add the new color to the beginning
  lightstrip[0] = pixels.Color(red, green, blue);
   
   // set pixels to the new colors
   for(int i = 0; i < NUMPIXELS; i++){
    pixels.setPixelColor(i, lightstrip[i]);
    pixels2.setPixelColor(i, lightstrip[i]);
  }
  pixels.show(); // This sends the updated pixel color to the hardware.
  pixels2.show();
  return true;
}

bool updateWholeLightStrip(int red, int green, int blue){
  //set pixels to new color
  for(int i = 0; i < NUMPIXELS; i++){
    pixels.setPixelColor(i, pixels.Color(red, green, blue));
    pixels2.setPixelColor(i, pixels.Color(red, green, blue));
  }
  pixels.show();
  pixels2.show();
  return true;
}

