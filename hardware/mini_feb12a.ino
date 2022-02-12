#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "noi";
const char* password = "noi12445";


int led1 = 5;
int led2 = 22;
int led3 = 21;
int ldr1 = 34;
int ldr2 = 32;
int ldr3 = 33;

static TaskHandle_t Task1 = NULL;
static TaskHandle_t Task2 = NULL;
static TaskHandle_t Task3 = NULL;

char str[50];
const int _size = 2*JSON_OBJECT_SIZE(4);

StaticJsonDocument<_size> JSONPost;

void WiFi_Connect(){
  WiFi.disconnect();
  WiFi.begin(ssid,password);
  while(WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.println("Connecting....");
  }
   Serial.println("Connected");
}

void _post(char rn, bool iu, char *url) {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    JSONPost["Room_Number"] = rn;
    JSONPost["InUse"] = iu;
    serializeJson(JSONPost, str);
    int httpCode = http.POST(str);

    if(httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(httpCode);
      Serial.println(payload);
      }else {
          Serial.println(httpCode);
          Serial.println("ERROR on HTTP Request");
      }
    }else {
            WiFi_Connect();
          }
    delay(100);
  }

void Room1(void *parameter){
  while (1){
    if (analogRead(ldr1) > 1000){
      digitalWrite(led1, HIGH);
    }else{
      digitalWrite(led1, LOW);
    }
  }
}
void Room2(void *parameter){
  while (1){
    if (analogRead(ldr2) < 1000){
      digitalWrite(led2, HIGH);
    }else{
      digitalWrite(led2, LOW);
    }
  }
}
void Room3(void *param) {
   while (1){
    if (analogRead(ldr3) > 500){
      digitalWrite(led3, LOW);
    }else{
      digitalWrite(led3, HIGH);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(ldr1, INPUT);
  pinMode(ldr2, INPUT);
  pinMode(ldr3, INPUT);
  digitalWrite(led1, HIGH);
  digitalWrite(led2, LOW); 
  digitalWrite(led3, LOW);

  xTaskCreatePinnedToCore(Room1, "Task_1", 1024, NULL, 1, &Task1, 1);
  xTaskCreatePinnedToCore(Room2, "Task_2", 1024, NULL, 1, &Task2, 1);
  xTaskCreatePinnedToCore(Room3, "Task_3", 1024, NULL, 1, &Task3, 1);
}


void loop() {
  if(analogRead(ldr1) > 1000) {
      _post('1', false, "https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/change/1/false");
    }else {
      _post('1', true, "https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/change/1/true");
    }
  if(analogRead(ldr2) < 1000) {
      _post('2', false, "https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/change/2/true");
    }else {
      _post('2', true,"https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/change/2/false");
    }
  if(analogRead(ldr3) > 500) {
      _post('3', false, "https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/change/3/false");
    }else {
      _post('3', false,"https://ecourse.cpe.ku.ac.th/exceed10/api/bathroom/change/3/true");
    }
}
