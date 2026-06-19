# 🌱 FarmTech Solutions — Sistema de Irrigação Inteligente

![FIAP](https://img.shields.io/badge/FIAP-Intelig%C3%AAncia%20Artificial-blue)
![Fase](https://img.shields.io/badge/Fase-4-brightgreen)
![Cultura](https://img.shields.io/badge/Cultura-Caf%C3%A9-brown)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)

## Visão geral

O **FarmTech Solutions** é um projeto acadêmico desenvolvido em grupo ao longo das fases 2, 3 e 4 da disciplina de Inteligência Artificial da FIAP. A proposta simula um ecossistema agrícola inteligente para lavoura de café, integrando **ESP32**, **Wokwi**, **Python**, **Oracle**, **Streamlit** e **Machine Learning**.

Nesta etapa final, o projeto evolui para uma abordagem de **previsão inteligente na agricultura**, com dashboards analíticos, ingestão automatizada de dados, modelos de regressão e recomendações baseadas em dados.

## Sumário

- [Integrantes](#integrantes)
- [Resumo do projeto](#resumo-do-projeto)
- [Entregas da Fase 4](#entregas-da-fase-4)
- [Vídeos demonstrativos](#vídeos-demonstrativos)
- [Como executar](#como-executar)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Documentação por fase](#documentação-por-fase)
- [Tecnologias utilizadas](#tecnologias-utilizadas)

## Integrantes

| Nome           |
| -------------- |
| Thiese Novaes  |
| João Vitor     |
| Talles Duran   |
| Kevin Santiago |
| Renan de Souza |

## Resumo do projeto

O projeto começa com a simulação de sensores em um **ESP32** no Wokwi, passa pela integração com dados climáticos via **OpenWeather**, avança para o armazenamento dos dados em **Oracle** e culmina em uma camada de análise com **Streamlit** e **Machine Learning**.

A cultura escolhida foi o **café**, por ser relevante para o agronegócio brasileiro e permitir a aplicação de regras agronômicas ligadas a umidade, pH e NPK.

## Entregas da Fase 4

### Parte principal da atividade

- Pipeline de Machine Learning com regressão usando Scikit-Learn
- Integração das previsões com o dashboard em Streamlit
- Exibição de métricas, previsões e gráficos analíticos

### Ir Além 1

- Ingestão automática de dados IoT no banco Oracle
- População inicial do histórico
- Atualização automática das leituras

### Ir Além 2

- Dashboard analítico com tendências de produtividade
- Comparação de rendimento real vs previsto
- Correlação entre NPK e rendimento
- Indicador de tendência do rendimento

## Vídeos demonstrativos

| Entrega                   | Link                                                               |
| ------------------------- | ------------------------------------------------------------------ |
| Fase 2 — ESP32 + Wokwi    | [Assistir no YouTube](https://www.youtube.com/watch?v=OxzF6pPU_3E) |
| Fase 3 — Banco de dados   | [Assistir no YouTube](https://youtu.be/jpHLyaU5JCU)                |
| Fase 3.1 — Dashboard e ML | [Assistir no YouTube](https://youtu.be/x8uJeT7SODM)                |
| Fase 4 — Ir Além 1        | [Assistir no YouTube](https://youtu.be/MsFykLMK8zw)                |
| Fase 4 — Ir Além 2        | [Assistir no YouTube](https://youtu.be/Y9oP9D3x01s)                |

## Como executar

### 1. Dashboard principal

```bash
cd dashboard
streamlit run dashboard.py
```

### 2. Pipeline de regressão

```bash
pip install scikit-learn pandas numpy matplotlib seaborn joblib
python ML/ml_farmtech_regressao.py
```

### 3. Ingestão automática no Oracle

```bash
pip install oracledb pandas python-dotenv --break-system-packages
python python/ingestao_sensores.py
```

### 4. Integração climática

```bash
pip install requests
python python/clima.py
```

## Estrutura do repositório

```text
farmtech-solutions/
├── dashboard/
│   ├── dashboard.py
│   ├── sensores_farmtech_v2.csv
│   └── pages/
│       ├── 2_🤖_ML_Regressao_Fase4.py
│       └── 3_📈_IrAlem2_Tendencias.py
├── docs/
│   ├── fase-2.md
│   ├── fase-3.md
│   ├── fase-4-ml-classificacao.md
│   ├── fase-4-regressao.md
│   ├── ir-alem-1.md
│   └── ir-alem-2.md
├── esp32/
├── imagens/
├── ML/
│   ├── csvs/
│   ├── docs/
│   └── outputs/
├── python/
│   ├── Base_csv/
│   ├── clima.py
│   └── ingestao_sensores.py
├── .env.example
├── diagram.json
├── README.md
└── requirements.txt
```

## Documentação por fase

A documentação completa foi separada para manter a raiz mais limpa e facilitar a leitura:

- `docs/fase-2.md`
- `docs/fase-3.md`
- `docs/fase-4-ml-classificacao.md`
- `docs/fase-4-regressao.md`
- `docs/ir-alem-1.md`
- `docs/ir-alem-2.md`

## Tecnologias utilizadas

| Tecnologia           | Uso                                  |
| -------------------- | ------------------------------------ |
| C/C++                | Programação do ESP32                 |
| Python               | Integração climática, dashboard e ML |
| Streamlit            | Interface analítica                  |
| Plotly               | Gráficos interativos                 |
| Pandas               | Manipulação dos dados                |
| Scikit-Learn         | Regressão e classificação            |
| Matplotlib / Seaborn | Visualizações do pipeline de ML      |
| Joblib               | Exportação de modelos                |
| Wokwi                | Simulação do circuito                |
| OpenWeather API      | Dados meteorológicos                 |
| Oracle SQL Developer | Banco de dados relacional            |
| python-oracledb      | Conexão Python ↔ Oracle              |
| python-dotenv        | Credenciais via .env                 |

<p align="center">
  FarmTech Solutions © 2026 — FIAP Inteligência Artificial
</p>
