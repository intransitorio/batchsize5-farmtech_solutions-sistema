#include "DHT.h"

#define DHTPIN 15
#define DHTTYPE DHT22
#define PIN_LDR 34
#define PIN_BTN_N 12
#define PIN_BTN_P 13
#define PIN_BTN_K 14
#define PIN_RELE 2

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  
  pinMode(PIN_BTN_N, INPUT_PULLUP);
  pinMode(PIN_BTN_P, INPUT_PULLUP);
  pinMode(PIN_BTN_K, INPUT_PULLUP);
  pinMode(PIN_RELE, OUTPUT);
  
  dht.begin();
  
  // Se você ver isso no terminal, a placa não travou
  Serial.println("\n--- SISTEMA FARMTECH INICIADO ---");
  Serial.println("Umid,pH,N,P,K,Bomba");
}

void loop() {
  float umid = dht.readHumidity();
  int ldrRaw = analogRead(PIN_LDR);
  float ph = map(ldrRaw, 0, 4095, 0, 14);

  // Lê os botões adequadamente sem curto
  int n = digitalRead(PIN_BTN_N) == LOW ? 1 : 0;
  int p = digitalRead(PIN_BTN_P) == LOW ? 1 : 0;
  int k = digitalRead(PIN_BTN_K) == LOW ? 1 : 0;

  // Lógica de irrigação para Cana
  bool bombaOn = (umid < 60.0 && ph >= 5.5 && ph <= 6.5);
  digitalWrite(PIN_RELE, bombaOn ? HIGH : LOW);

  // Output CSV para o Python/R
  Serial.print(umid); Serial.print(",");
  Serial.print(ph);   Serial.print(",");
  Serial.print(n);    Serial.print(",");
  Serial.print(p);    Serial.print(",");
  Serial.print(k);    Serial.print(",");
  Serial.println(bombaOn ? 1 : 0);

  delay(1000); 
}