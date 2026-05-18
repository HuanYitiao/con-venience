#include <Arduino.h>
#include <GxEPD2_BW.h>
#include <Fonts/FreeMonoBold9pt7b.h>
#include <SPI.h>

SPIClass hspi(HSPI);

GxEPD2_BW<GxEPD2_290_T94, GxEPD2_290_T94::HEIGHT> display(
    GxEPD2_290_T94(/*CS=*/15, /*DC=*/27, /*RST=*/26, /*BUSY=*/25));

void setup() {
    Serial.begin(115200);
    hspi.begin(13, -1, 14, 15); // SCK, MISO, MOSI, CS
    display.epd2.selectSPI(hspi, SPISettings(4000000, MSBFIRST, SPI_MODE0));
    
    display.init(115200);
    display.clearScreen();
    
    display.setRotation(1);
    display.setFont(&FreeMonoBold9pt7b);
    display.setTextColor(GxEPD_BLACK);
    
    display.setFullWindow();
    display.firstPage();
    do {
        display.fillScreen(GxEPD_WHITE);
        display.setCursor(10, 30);
        display.print("Hello fur!");
    } while (display.nextPage());
    
    Serial.println("done");
}

void loop() {}