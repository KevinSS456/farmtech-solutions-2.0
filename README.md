# 🌱 FarmTech Solutions — Sistema de Irrigação Inteligente

![GitHub](https://img.shields.io/badge/FIAP-Inteligência%20Artificial-blue)
![GitHub](https://img.shields.io/badge/Fase-2-green)
![GitHub](https://img.shields.io/badge/Cultura-Café-brown)

## 👥 Integrantes

| Nome |
|------|
| Thiese Novaes |
| João Vitor |
| Talles Duran |
| Kevin Santiago |
| Renan de Souza |

---

## 📋 Descrição do Projeto

Este projeto foi desenvolvido como parte da **Fase 2** do curso de Inteligência Artificial da FIAP,
pela startup fictícia **FarmTech Solutions**.

O objetivo é simular um sistema de irrigação inteligente para uma lavoura de **café**,
utilizando um microcontrolador **ESP32** simulado na plataforma **Wokwi.com**,
com sensores que monitoram as condições do solo em tempo real e integração com
dados climáticos via **API OpenWeather**.

---

## ☕ Cultura Agrícola — Café

O café foi escolhido por ser uma das culturas mais importantes do Brasil.
Suas necessidades ideais são:

| Parâmetro | Valor Ideal | Valor Simulado |
|-----------|-------------|----------------|
| pH do solo | 6,0 a 6,5 | 5,5 a 7,0 (via LDR) |
| Umidade do solo | 60% a 80% | DHT22 |
| Nitrogênio (N) | Alta necessidade | Botão toggle |
| Fósforo (P) | Média necessidade | Botão toggle |
| Potássio (K) | Alta necessidade | Botão toggle |

---

## 🔧 Componentes Utilizados

| Componente | Função Real | Função no Projeto |
|------------|-------------|-------------------|
| ESP32 DevKit | Microcontrolador | Cérebro do sistema |
| 3 Botões Verdes | Sensores NPK | Simula níveis de N, P e K |
| LDR + Resistor 10kΩ | Sensor de luz | Simula o pH do solo |
| DHT22 | Sensor de umidade do ar | Simula umidade do solo |
| Módulo Relé | Atuador | Simula a bomba d'água |

---

## 🔌 Pinagem do Circuito

| Componente | Pino ESP32 |
|------------|------------|
| Botão Nitrogênio (N) | GPIO 12 |
| Botão Fósforo (P) | GPIO 13 |
| Botão Potássio (K) | GPIO 14 |
| LDR (pH) | GPIO 35 |
| DHT22 (Umidade) | GPIO 15 |
| Relé (Bomba) | GPIO 26 |

---

## 🖼️ Circuito no Wokwi

> Insira aqui o print do circuito montado no Wokwi

![Circuito Wokwi](imagens/circuito.png)

---

## 🧠 Lógica de Irrigação

A bomba d'água (relé) é **LIGADA** quando todas as condições abaixo são satisfeitas simultaneamente:

```
✅ Nitrogênio presente (botão N ligado)
✅ Potássio presente (botão K ligado)
✅ pH entre 5,5 e 7,0 (LDR na faixa correta)
✅ Umidade do solo abaixo de 60% (solo seco)
✅ Sem previsão de chuva (dado recebido do Python)
```

A bomba é **DESLIGADA** quando qualquer condição abaixo for verdadeira:

```
❌ Umidade acima de 80% (solo encharcado)
❌ pH fora da faixa ideal
❌ Nitrogênio ou Potássio ausentes
❌ Previsão de chuva detectada pelo Python (valor 1 no Serial Monitor)
```

### 🔘 Funcionamento dos botões NPK:
- **1º clique** → Nutriente **presente** ✅
- **2º clique** → Nutriente **ausente** ❌

---

## 🌦️ Opcional 1 — Integração Python + OpenWeather

O arquivo `clima.py` consome a API pública da **OpenWeather** para verificar
se há previsão de chuva na cidade configurada.

### Fluxo completo:

```
🐍 Python roda clima.py
        ↓
☁️ Resultado: tem chuva ou não?
        ↓
⌨️ Usuário digita 0 ou 1 no Serial Monitor do Wokwi
        ↓
🔌 ESP32 lê o valor e decide ligar ou não a bomba
```

### Valores aceitos pelo Serial Monitor:

| Valor | Significado | Ação |
|-------|-------------|------|
| `0` | Sem chuva | Irrigação liberada ✅ |
| `1` | Chuva prevista | Irrigação suspensa 🌧️ |

### Exemplo de resultado do clima.py:

```
====================================
 FarmTech Solutions - Café
 Análise Climática para Irrigação
====================================
 Cidade      : São Paulo
 Temperatura : 19.03°C
 Umidade     : 87%
 Condição    : algumas nuvens
------------------------------------
 🌥️  Alta umidade no ar
 ⚠️  Irrigação REDUZIDA
====================================
 Resultado salvo em 'resultado_clima.txt'
 Valor: 0 (1 = tem chuva, 0 = sem chuva)
```

### Como rodar:

```bash
pip install requests
python clima.py
```

---

## 📁 Estrutura do Repositório

```
📦 farmtech-solutions
 ┣ 📂 esp32
 ┃ ┗ 📄 sketch.ino         → Código C/C++ do ESP32
 ┣ 📂 python
 ┃ ┗ 📄 clima.py           → Integração com API OpenWeather
 ┣ 📂 imagens
 ┃ ┗ 📄 circuito.png       → Print do circuito no Wokwi
 ┣ 📄 diagram.json         → Diagrama do circuito Wokwi
 ┗ 📄 README.md            → Este arquivo
```

---

## 🛠️ Como Simular o Projeto

1. Acesse [wokwi.com](https://wokwi.com)
2. Crie um novo projeto ESP32
3. Cole o conteúdo do `diagram.json`
4. Cole o conteúdo do `sketch.ino`
5. Instale a biblioteca `DHT sensor library` no `libraries.txt`
6. Clique em **Play ▶️**
7. Interaja com os botões e sensores
8. Acompanhe o Serial Monitor
9. Digite `0` ou `1` conforme o resultado do `clima.py`

---

## 🎥 Vídeo Demonstrativo

> [Clique aqui para assistir ao vídeo no YouTube]([https://youtube.com/link-do-video](https://youtu.be/OxzF6pPU_3E))

---

## 📚 Tecnologias Utilizadas

- **C/C++** — Programação do ESP32
- **Python** — Integração com API climática
- **Wokwi** — Simulação do circuito
- **OpenWeather API** — Dados meteorológicos em tempo real
