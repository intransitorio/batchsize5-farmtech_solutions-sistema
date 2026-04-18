#include "DHT.h"

// Definições de Hardware
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
  delay(1000); // Segurança para abertura do terminal
  
  pinMode(PIN_BTN_N, INPUT_PULLUP);
  pinMode(PIN_BTN_P, INPUT_PULLUP);
  pinMode(PIN_BTN_K, INPUT_PULLUP);
  pinMode(PIN_RELE, OUTPUT);
  
  dht.begin();
  
  Serial.println("\n--- FARMTECH SOLUTIONS: AUTOMACAO CANA ---");
  Serial.println("Umid,pH_Base,pH_Final,N,P,K,Bomba");
}

void loop() {
  // 1. Leitura de Sensores
  float umid = dht.readHumidity();
  int ldrRaw = analogRead(PIN_LDR);
  float phBase = map(ldrRaw, 0, 4095, 0, 14);

  // 2. Leitura de Botões (NPK)
  int n = (digitalRead(PIN_BTN_N) == LOW) ? 1 : 0;
  int p = (digitalRead(PIN_BTN_P) == LOW) ? 1 : 0;
  int k = (digitalRead(PIN_BTN_K) == LOW) ? 1 : 0;

  // 3. Automação: NPK alterando o pH via software
  float phFinal = phBase;
  if (n == 1) phFinal -= 0.8; // Nitrogênio acidifica
  if (p == 1) phFinal += 0.4; // Fósforo alcaliniza
  if (k == 1) phFinal += 0.4; // Potássio alcaliniza

  // Clamping de segurança (0-14)
  if (phFinal < 0.0) phFinal = 0.0;
  if (phFinal > 14.0) phFinal = 14.0;

  // 4. Lógica de Decisão (Cana: Umid < 60% e pH 5.5 a 6.5)
  bool phIdeal = (phFinal >= 5.5 && phFinal <= 6.5);
  bool precisaAgua = (umid < 60.0);
  bool ligarBomba = (precisaAgua && phIdeal);

  digitalWrite(PIN_RELE, ligarBomba ? HIGH : LOW);

  // 5. Output Serial (CSV format)
  Serial.print(umid);    Serial.print(",");
  Serial.print(phBase);  Serial.print(",");
  Serial.print(phFinal); Serial.print(",");
  Serial.print(n);       Serial.print(",");
  Serial.print(p);       Serial.print(",");
  Serial.print(k);       Serial.print(",");
  Serial.println(ligarBomba ? 1 : 0);

  delay(500); 
}