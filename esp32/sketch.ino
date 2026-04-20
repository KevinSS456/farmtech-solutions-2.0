#include "DHT.h"

// ========== PINOS ==========
#define BTN_N    12
#define BTN_P    13
#define BTN_K    14
#define LDR_PIN  35
#define DHT_PIN  15
#define RELE_PIN 26

DHT dht(DHT_PIN, DHT22);

// ========== VARIAVEIS ==========
bool estadoN = false;
bool estadoP = false;
bool estadoK = false;
bool ultimoN = HIGH;
bool ultimoP = HIGH;
bool ultimoK = HIGH;
int previsaoChuva = 0; // 0 = sem chuva, 1 = tem chuva

void setup() {
  Serial.begin(9600);

  pinMode(BTN_N, INPUT_PULLUP);
  pinMode(BTN_P, INPUT_PULLUP);
  pinMode(BTN_K, INPUT_PULLUP);
  pinMode(RELE_PIN, OUTPUT);
  digitalWrite(RELE_PIN, LOW);

  dht.begin();
  delay(2000);

  Serial.println("====================================");
  Serial.println(" FarmTech Solutions - Cafe");
  Serial.println(" Sistema de Irrigacao Inteligente");
  Serial.println("====================================");
  Serial.println("Digite 0 = sem chuva | 1 = tem chuva");
}

// ========== FUNCAO TOGGLE ==========
void verificarBotao(int pino, bool &estado, bool &ultimo) {
  bool leitura = digitalRead(pino);
  if (ultimo == HIGH && leitura == LOW) {
    estado = !estado;
    delay(50);
  }
  ultimo = leitura;
}

// ========== LEITURA DO SERIAL (Python) ==========
void lerPrevisaoChuva() {
  if (Serial.available() > 0) {
    char dado = Serial.read();
    if (dado == '0') {
      previsaoChuva = 0;
      Serial.println(">> Previsao atualizada: SEM CHUVA");
    } else if (dado == '1') {
      previsaoChuva = 1;
      Serial.println(">> Previsao atualizada: TEM CHUVA - Irrigacao suspensa!");
    }
  }
}

void loop() {
  // ---- Leitura do Serial (previsao do Python) ----
  lerPrevisaoChuva();

  // ---- Toggle dos botoes ----
  verificarBotao(BTN_N, estadoN, ultimoN);
  verificarBotao(BTN_P, estadoP, ultimoP);
  verificarBotao(BTN_K, estadoK, ultimoK);

  // ---- Leitura do LDR (pH) ----
  int ldr = analogRead(LDR_PIN);
  float ph = (ldr / 4095.0) * 14.0;

  // ---- Leitura do DHT22 ----
  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();

  if (isnan(umidade) || isnan(temperatura)) {
    Serial.println("Erro na leitura do DHT22!");
    delay(2000);
    return;
  }

  // ========== LOGICA DE IRRIGACAO ==========
  bool phIdeal      = (ph >= 5.5 && ph <= 7.0);
  bool umidadeBaixa = (umidade < 60.0);
  bool umidadeAlta  = (umidade > 80.0);
  bool npkOk        = (estadoN && estadoK);

  bool ligar = false;

  if (umidadeBaixa && phIdeal && npkOk) {
    ligar = true;
  }
  if (umidadeAlta) {
    ligar = false;
  }
  if (previsaoChuva == 1) {
    ligar = false; // Python detectou chuva!
  }

  digitalWrite(RELE_PIN, ligar ? HIGH : LOW);

  // ========== MONITOR SERIAL ==========
  Serial.println("----------------------------");
  Serial.print("Nitrogenio : "); Serial.println(estadoN ? "Presente" : "Ausente");
  Serial.print("Fosforo    : "); Serial.println(estadoP ? "Presente" : "Ausente");
  Serial.print("Potassio   : "); Serial.println(estadoK ? "Presente" : "Ausente");
  Serial.print("pH         : "); Serial.println(ph, 1);
  Serial.print("Umidade    : "); Serial.print(umidade, 1); Serial.println("%");
  Serial.print("Temperatura: "); Serial.print(temperatura, 1); Serial.println("C");
  Serial.print("Chuva      : "); Serial.println(previsaoChuva == 1 ? "SIM" : "NAO");
  Serial.println("----------------------------");
  Serial.print("Bomba      : "); Serial.println(ligar ? "LIGADA" : "DESLIGADA");
  Serial.println("============================");

  delay(3000);
}