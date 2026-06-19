# 🌱 FarmTech Solutions — Fase 2

![FIAP](https://img.shields.io/badge/FIAP-Inteligência%20Artificial-blue)
![Fase](https://img.shields.io/badge/Fase-2-brightgreen)
![Cultura](https://img.shields.io/badge/Cultura-Café-brown)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)

## 👥 Integrantes

| Nome           |
| -------------- |
| Thiese Novaes  |
| João Vitor     |
| Talles Duran   |
| Kevin Santiago |
| Renan de Souza |

---

## 📋 Descrição do Projeto

Este projeto foi desenvolvido como parte das fases do curso de Inteligência Artificial da FIAP,
pela startup fictícia **FarmTech Solutions**.

O objetivo é simular um sistema de irrigação inteligente para uma lavoura de **café**,
utilizando um microcontrolador **ESP32** simulado na plataforma **Wokwi.com**,
com sensores que monitoram as condições do solo em tempo real e integração com
dados climáticos via **API OpenWeather**.

---

## ☕ Cultura Agrícola — Café

O café foi escolhido por ser uma das culturas mais importantes do Brasil.
Suas necessidades ideais são:

| Parâmetro       | Valor Ideal | Valor Simulado         |
| --------------- | ----------- | ---------------------- |
| pH do solo      | 6,0 a 6,5   | 5,5 a 7,0 (via LDR)    |
| Umidade do solo | 60% a 80%   | DHT22                  |
| Nitrogênio (N)  | ≥ 80 mg/kg  | Simulado numericamente |
| Fósforo (P)     | ≥ 30 mg/kg  | Simulado numericamente |
| Potássio (K)    | ≥ 100 mg/kg | Simulado numericamente |

---

## 🔧 Componentes Utilizados

| Componente          | Função Real             | Função no Projeto         |
| ------------------- | ----------------------- | ------------------------- |
| ESP32 DevKit        | Microcontrolador        | Cérebro do sistema        |
| 3 Botões Verdes     | Sensores NPK            | Simula níveis de N, P e K |
| LDR + Resistor 10kΩ | Sensor de luz           | Simula o pH do solo       |
| DHT22               | Sensor de umidade do ar | Simula umidade do solo    |
| Módulo Relé         | Atuador                 | Simula a bomba d'água     |

---

## 🔌 Pinagem do Circuito

| Componente           | Pino ESP32 |
| -------------------- | ---------- |
| Botão Nitrogênio (N) | GPIO 12    |
| Botão Fósforo (P)    | GPIO 13    |
| Botão Potássio (K)   | GPIO 14    |
| LDR (pH)             | GPIO 35    |
| DHT22 (Umidade)      | GPIO 15    |
| Relé (Bomba)         | GPIO 26    |

---

## 🖼️ Circuito no Wokwi

![Circuito Wokwi](../imagens/circuito.png)

---

## 🧠 Lógica de Irrigação

A bomba d'água (relé) é **LIGADA** quando todas as condições abaixo são satisfeitas simultaneamente:

```text
✅ Nitrogênio ≥ 80 mg/kg
✅ Fósforo ≥ 30 mg/kg
✅ Potássio ≥ 100 mg/kg
✅ pH entre 5,5 e 7,0 (LDR na faixa correta)
✅ Umidade do solo abaixo de 60% (solo seco)
✅ Sem previsão de chuva (dado recebido pelo Python)
```

> ⚠️ **Correção aplicada na Fase 3:** O Fósforo foi incluído na lógica de decisão da bomba,
> corrigindo o apontamento do professor onde apenas N e K eram verificados (`npkOk = estadoN && estadoK`).
> A versão correta é `npkOk = estadoN && estadoP && estadoK`.

A bomba é **DESLIGADA** quando qualquer condição abaixo for verdadeira:

```text
❌ Umidade acima de 80% (solo encharcado)
❌ pH fora da faixa ideal
❌ N, P ou K abaixo do mínimo necessário
❌ Previsão de chuva detectada pelo Python (valor 1 no Serial Monitor)
```

### 🔘 Funcionamento dos botões NPK

- **1º clique** → Nutriente **presente** ✅
- **2º clique** → Nutriente **ausente** ❌

---

## 🌦️ Integração Python + OpenWeather

O arquivo `clima.py` consome a API pública da **OpenWeather** para verificar
se há previsão de chuva na cidade configurada.

### Fluxo completo

```text
🐍 Python roda clima.py
        ↓
☁️ Resultado: tem chuva ou não?
        ↓
⌨️ Usuário digita 0 ou 1 no Serial Monitor do Wokwi
        ↓
🔌 ESP32 lê o valor e decide ligar ou não a bomba
```

### Valores aceitos pelo Serial Monitor

| Valor | Significado    | Ação                  |
| ----- | -------------- | --------------------- |
| `0`   | Sem chuva      | Irrigação liberada ✅ |
| `1`   | Chuva prevista | Irrigação suspensa 🌧️ |

### Exemplo de resultado do clima.py

```text
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

### Como rodar

```bash
pip install requests
python clima.py
```

---

## 🛠️ Como Simular o Projeto (ESP32)

1. Acesse [wokwi.com](https://wokwi.com)
2. Crie um novo projeto ESP32
3. Cole o conteúdo do `diagram.json`
4. Cole o conteúdo do `sketch.ino`
5. Instale a biblioteca `DHT sensor library` no `libraries.txt`
6. Clique em **Play ▶️**
7. Interaja com os botões e sensores
8. Acompanhe o Serial Monitor
9. Digite `0` ou `1` conforme o resultado do `clima.py`
