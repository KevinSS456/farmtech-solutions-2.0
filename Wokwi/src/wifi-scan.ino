#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include "DHT.h"

// ================================================================
// FARMTECH SOLUTIONS - Monitoramento de Solo e Clima com ESP32
// Sensores: DHT22 (temperatura/umidade do ar) + Umidade do Solo
// Envio dos dados via HTTP POST para servidor Flask (Python)
// ================================================================

// ===== WI-FI DO WOKWI =====
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// ===== ENDEREÇO DO SERVIDOR FLASK =====
// Hospedado no Render - não depende do seu PC estar ligado
const char* serverURL = "https://farmtech-solutions-2-0.onrender.com/api/dados";

// ===== DHT22 =====
#define DHTPIN 15
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ===== UMIDADE DO SOLO =====
#define SOIL_PIN 34

void setup() {
  Serial.begin(115200);
  dht.begin();

  Serial.println();
  Serial.println("================================");
  Serial.println("       FARMTECH MONITOR");
  Serial.println("================================");

  // Conecta ao Wi-Fi
  Serial.print("Conectando ao Wi-Fi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Wi-Fi conectado!");
  Serial.print("IP do ESP32: ");
  Serial.println(WiFi.localIP());
  Serial.println("Sensores inicializados!");
}

void loop() {
  // ===== LEITURA DO DHT22 =====
  float temperatura = dht.readTemperature();
  float umidadeAr = dht.readHumidity();

  // ===== LEITURA DO SENSOR DE UMIDADE DO SOLO =====
  int valorSolo = analogRead(SOIL_PIN);
  int umidadeSolo = map(valorSolo, 0, 4095, 0, 100);

  // ===== EXIBE OS DADOS NO SERIAL =====
  if (isnan(temperatura) || isnan(umidadeAr)) {
    Serial.println("Erro ao ler o DHT22!");
  } else {
    Serial.println("-------------------------------");
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.println(" °C");

    Serial.print("Umidade do ar: ");
    Serial.print(umidadeAr);
    Serial.println(" %");

    Serial.print("Umidade do solo: ");
    Serial.print(umidadeSolo);
    Serial.println(" %");
    Serial.println("-------------------------------");

    // ===== ENVIA OS DADOS PARA O SERVIDOR FLASK =====
    enviarDados(temperatura, umidadeAr, umidadeSolo);
  }

  delay(2000);
}

// Monta o JSON e envia via HTTP POST para o servidor Flask
void enviarDados(float temperatura, float umidadeAr, int umidadeSolo) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi desconectado! Não foi possível enviar os dados.");
    return;
  }

  WiFiClientSecure client;
  client.setInsecure(); // ignora validação do certificado SSL
  client.setHandshakeTimeout(120); // mais tempo para negociar o TLS

  HTTPClient http;
  http.begin(client, serverURL);
  http.addHeader("Content-Type", "application/json");

  // Monta o corpo da requisição em formato JSON manualmente
  String jsonPayload = "{";
  jsonPayload += "\"temperatura\":" + String(temperatura, 2) + ",";
  jsonPayload += "\"umidade_ar\":" + String(umidadeAr, 2) + ",";
  jsonPayload += "\"umidade_solo\":" + String(umidadeSolo);
  jsonPayload += "}";

  int httpResponseCode = http.POST(jsonPayload);

  if (httpResponseCode > 0) {
    Serial.print("Dados enviados! Código HTTP: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Erro ao enviar dados. Código: ");
    Serial.println(httpResponseCode);
    Serial.print("Detalhe: ");
    Serial.println(http.errorToString(httpResponseCode));
  }

  http.end();
}