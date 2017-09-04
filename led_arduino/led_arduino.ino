/**
 * This sketch will handle the communication between an external data source 
 * and the LED strip. It must be given a serial input in the form 
 * mode,red,green,blue 
 * 
 * After receiving this valid input, it will write to the pixel strip 
 * and display the updated colors.
 */

#include <Adafruit_NeoPixel.h>

#define NUMPIXELS      60

int counter = 0; 

Adafruit_NeoPixel pixels[] = {Adafruit_NeoPixel(NUMPIXELS, 8, NEO_GRB + NEO_KHZ800),Adafruit_NeoPixel(NUMPIXELS, 9, NEO_GRB + NEO_KHZ800)}; 
uint32_t lightstrip [NUMPIXELS];

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps

  // Set all the pixels to red 
  uint32_t red = pixels[0].Color(255, 0, 0); 
  for (int i=0; i<NUMPIXELS; i++) {
    lightstrip[i] = red;
  }
  pixels[0].begin(); // This initializes the NeoPixel library
  updateLightStrip(255, 0, 0);
  pixels[0].show();
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
        switch(mode){
          case 0:
            pixels[0].setPixelColor(0, pixels[0].Color(0,0,0));
            updateWholeLightStrip(red, green, blue);
          case 1:
            pixels[0].setPixelColor(counter, pixels[0].Color(red, green, blue));
            counter++;
            pixels[0].show();
            counter = 0;
          default:
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
  lightstrip[0] = pixels[0].Color(red, green, blue);
   
   // set pixels to the new colors
   for(int i = 0; i < NUMPIXELS; i++){
    pixels[0].setPixelColor(i, lightstrip[i]);
  }
  pixels[0].show(); // This sends the updated pixel color to the hardware.
  return true;
}

bool updateWholeLightStrip(int red, int green, int blue){
  //set pixels to new color
  for(int i = 0; i < NUMPIXELS; i++){
    pixels[0].setPixelColor(i, pixels[0].Color(red, green, blue));
  }
  pixels[0].show();
  return true;
}
