#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include <ESP8266WiFi.h>
#include "wifi_config.h"
//some dirty globals (can't really help it)
const char* ssid = "derpnet";
WiFiServer server(80);
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT);
#ifdef SSID
void initWifi () {
  Serial.print("[wifi] connecting to ");
  Serial.println(SSID);
  #ifdef PSK
    int status = WiFi.begin(SSID, PSK);
  #else
    int status = WiFi.begin(SSID);
  #endif
  while (status != WL_CONNECTED) {
    Serial.print('.');
    delay(5000);
    #ifdef PSK
      status = WiFi.begin(SSID, PSK);
    #else
      status = WiFi.begin(SSID);
    #endif
  }
  Serial.print('\n');
  Serial.println("[wifi] connected");
  Serial.print("[wifi] ip: ");
  Serial.println(WiFi.localIP());
}
#else
void initWifi () {
  Serial.print("[wifi] creating ssid: ");
  Serial.println(ssid);
  WiFi.softAP(ssid);
  Serial.println("[wifi] connected");
  Serial.print("[wifi] ip: ");
  Serial.println(WiFi.softAPIP());
}
#endif
void initSensor() {
  Serial.print("[sensor] initializing: ");
  if (!tsl.begin()) return;
  tsl.enableAutoRange(true);
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);
  Serial.println("done.");
}
float getSensorReading() {
  sensors_event_t ev;
  tsl.getEvent(&ev);
  return(ev.light);
}
void respond(WiFiClient* wc, float reading) {
  wc->print("HTTP/1.1 200 OK\r\n");
  wc->println("Content-type: text/plain\r\n\r\n");
  Serial.println("[server] sent header");
  wc->println(reading);
  wc->flush();
  wc->stop();
  Serial.print("[server] sent reading of ");
  Serial.print(reading);
  Serial.println(" lux");
}
void setup () {
  //initialize serial uart and wait 1 second
  Serial.begin(115200);
  delay(1000);
  //start the sensor
  initSensor();
  //start the wifi client
  initWifi();
  //start the webserver
  server.begin();
  Serial.println("[server] started");
}
void loop() {
  float sensorReading = getSensorReading();
  //attempt to get a client
  WiFiClient wc = server.available();
  if (!wc) { //fail and try again
    return;
  }
  //we've got a client, tell the terminal
  Serial.print("[server] client: ");
  Serial.println(wc.remoteIP());
  while (!wc.available()) {
    delay(1);
  }
  String req = wc.readStringUntil('\r');
  Serial.print("[server] request: ");
  Serial.println(req);
  wc.flush();
  if (req.indexOf("/lux") != -1) {
    Serial.println("[server] received lux request");
    respond(&wc, sensorReading);
  }
  delay(1);
}
