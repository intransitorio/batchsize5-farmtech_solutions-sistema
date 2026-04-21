#include "DHT.h"

#define DHTPIN 15
#define DHTTYPE DHT22
#define PIN_LDR 34
#define PIN_BTN_N 12
#define PIN_BTN_P 13
#define PIN_BTN_K 14
#define PIN_RELE 2

DHT dht(DHTPIN, DHTTYPE);

// Inicia em FALSE (Não há deficiência / Tudo OK)
bool deficienciaN = false;
bool deficienciaP = false;
bool deficienciaK = false;

int lastN = HIGH;
int lastP = HIGH;
int lastK = HIGH;

unsigned long tempoAnterior = 0;
const long intervalo = 2000; 

void setup() {
  Serial.begin(115200);
  delay(1000); 
  
  pinMode(PIN_BTN_N, INPUT_PULLUP);
  pinMode(PIN_BTN_P, INPUT_PULLUP);
  pinMode(PIN_BTN_K, INPUT_PULLUP);
  pinMode(PIN_RELE, OUTPUT);
  
  dht.begin();
  
  Serial.println("\n--- FarmTech: Monitoramento de Deficiencias ---");
  Serial.println("Umid,pH,Defic_N,Defic_P,Defic_K,Bomba");
}

void loop() {
  // BLOCO 1: DETECÇÃO DE CLIQUES (Toggle Logic)
  int currN = digitalRead(PIN_BTN_N);
  int currP = digitalRead(PIN_BTN_P);
  int currK = digitalRead(PIN_BTN_K);
  
  // Ao clicar, alterna o estado de deficiência
  if (lastN == HIGH && currN == LOW) { deficienciaN = !deficienciaN; delay(50); }
  if (lastP == HIGH && currP == LOW) { deficienciaP = !deficienciaP; delay(50); }
  if (lastK == HIGH && currK == LOW) { deficienciaK = !deficienciaK; delay(50); }
  
  lastN = currN;
  lastP = currP;
  lastK = currK;
  
  // BLOCO 2: PROCESSAMENTO E DECISÃO
  unsigned long tempoAtual = millis();
  
  if (tempoAtual - tempoAnterior >= intervalo) {
    tempoAnterior = tempoAtual;
    
    float umid = dht.readHumidity();
    int ldrRaw = analogRead(PIN_LDR);
    float ph = map(ldrRaw, 0, 4095, 0, 14);
    
    // --- Lógica Refinada para Cana-de-Açúcar ---
    bool precisaAgua = (umid < 60.0);
    bool soloCarente = (deficienciaN || deficienciaP || deficienciaK);
    bool phOk = (ph >= 5.5 && ph <= 6.5);
    
    // Nova Trava de Segurança: Evita afogar a planta e lavar o adubo
    bool riscoEncharcamento = (umid >= 75.0); 
    
    // A bomba liga se: pH OK + Sem risco de encharcar + (Precisa de água OU precisa adubar)
    bool ligarBomba = (phOk && !riscoEncharcamento && (precisaAgua || soloCarente));
    
    digitalWrite(PIN_RELE, ligarBomba ? HIGH : LOW);
    
    // Output Serial formatado para CSV
    Serial.print(umid);         Serial.print(",");
    Serial.print(ph);           Serial.print(",");
    Serial.print(deficienciaN); Serial.print(",");
    Serial.print(deficienciaP); Serial.print(",");
    Serial.print(deficienciaK); Serial.print(",");
    Serial.println(ligarBomba ? 1 : 0);
  }
}