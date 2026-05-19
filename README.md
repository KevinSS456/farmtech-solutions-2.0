># 🌱 FarmTech Solutions — Sistema de Irrigação Inteligente

![GitHub](https://img.shields.io/badge/FIAP-Inteligência%20Artificial-blue)
![GitHub](https://img.shields.io/badge/Fase-3-brightgreen)
![GitHub](https://img.shields.io/badge/Cultura-Café-brown)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)

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

Este projeto foi desenvolvido como parte das **Fases 2 e 3** do curso de Inteligência Artificial da FIAP,
pela startup fictícia **FarmTech Solutions**.

O objetivo é simular um sistema de irrigação inteligente para uma lavoura de **café**,
utilizando um microcontrolador **ESP32** simulado na plataforma **Wokwi.com**,
com sensores que monitoram as condições do solo em tempo real e integração com
dados climáticos via **API OpenWeather**.

Na **Fase 3**, os dados coletados pelos sensores foram importados em um **banco de dados Oracle**
e visualizados em um **dashboard interativo** desenvolvido com Python e Streamlit.

---

## ☕ Cultura Agrícola — Café

O café foi escolhido por ser uma das culturas mais importantes do Brasil.
Suas necessidades ideais são:

| Parâmetro | Valor Ideal | Valor Simulado |
|-----------|-------------|----------------|
| pH do solo | 6,0 a 6,5 | 5,5 a 7,0 (via LDR) |
| Umidade do solo | 60% a 80% | DHT22 |
| Nitrogênio (N) | ≥ 80 mg/kg | Simulado numericamente |
| Fósforo (P) | ≥ 30 mg/kg | Simulado numericamente |
| Potássio (K) | ≥ 100 mg/kg | Simulado numericamente |

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

<img width="562" height="473" alt="image" src="https://github.com/user-attachments/assets/c4d1a031-b65e-45a7-9c42-4ec2f617643a" />

![Circuito Wokwi](imagens/circuito.png)

---

## 🧠 Lógica de Irrigação

A bomba d'água (relé) é **LIGADA** quando todas as condições abaixo são satisfeitas simultaneamente:

```
✅ Nitrogênio ≥ 80 mg/kg
✅ Fósforo ≥ 30 mg/kg
✅ Potássio ≥ 100 mg/kg
✅ pH entre 5,5 e 7,0 (LDR na faixa correta)
✅ Umidade do solo abaixo de 60% (solo seco)
✅ Sem previsão de chuva (dado recebido do Python)
```

> ⚠️ **Correção aplicada na Fase 3:** O Fósforo foi incluído na lógica de decisão da bomba,
> corrigindo o apontamento do professor onde apenas N e K eram verificados (`npkOk = estadoN && estadoK`).
> A versão correta é `npkOk = estadoN && estadoP && estadoK`.

A bomba é **DESLIGADA** quando qualquer condição abaixo for verdadeira:

```
❌ Umidade acima de 80% (solo encharcado)
❌ pH fora da faixa ideal
❌ N, P ou K abaixo do mínimo necessário
❌ Previsão de chuva detectada pelo Python (valor 1 no Serial Monitor)
```

### 🔘 Funcionamento dos botões NPK:
- **1º clique** → Nutriente **presente** ✅
- **2º clique** → Nutriente **ausente** ❌

---

## 🌦️ Integração Python + OpenWeather

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

## 🗄️ Fase 3 — Banco de Dados Oracle

Os dados dos sensores foram importados no banco de dados **Oracle** da FIAP
usando o **Oracle SQL Developer**.

### Configuração da conexão:

| Campo | Valor |
|-------|-------|
| Host | oracle.fiap.com.br |
| Porta | 1521 |
| SID | ORCL |
| Usuário | RM + número (ex: RM12345) |
| Senha | Data de nascimento (DDMMYY) |

### Consulta utilizada:

```sql
SELECT * FROM SENSORES_FARMTECH;
```

> Print do banco de dados:

![Banco Oracle](imagens/oracle_print.png)

---

## 📊 Fase 3 — Dashboard Interativo

Dashboard desenvolvido em **Python + Streamlit** para visualização dos dados dos sensores.

### Como executar:

```bash
pip install streamlit plotly pandas
python -m streamlit run dashboard.py
```

> ⚠️ Deve rodar o script dentro da pasta do arquivo.

### Funcionalidades:

| Seção | Descrição |
|-------|-----------|
| 📡 Leitura Mais Recente | Cards com umidade, pH, N, P, K e chuva |
| 🚿 Status da Irrigação | Bomba ligada/desligada + sugestões automáticas |
| 📆 Visão Semanal | Médias de todas as variáveis + ativações da bomba por semana (S1–S4) |
| 💧 Umidade & pH | Série temporal com faixas ideais |
| 🌿 NPK | Evolução de N, P, K com limiares mínimos |
| 🚿 Irrigação | Barras por dia + distribuição de estados |
| 📊 Correlações | Scatter plot interativo entre variáveis |

> Print do dashboard:

![Dashboard]<img width="1200" height="600" alt="image" src="https://github.com/user-attachments/assets/950c7549-266e-4ad0-ad2f-490671a0754b" />
)
<img width="1200" height="600" alt="image" src="https://github.com/user-attachments/assets/9f0897d2-f38f-47fe-820a-95483ee33f29" />
<img width="1200" height="600" alt="image" src="https://github.com/user-attachments/assets/567d8a3c-69d6-4122-b205-6fb2fc7b6b0e" />


## 🤖 Fase 4 — Machine Learning para Predição de Culturas Agrícolas

Como extensão da solução FarmTech Solutions, foi desenvolvido um módulo de **Machine Learning supervisionado**
capaz de prever a cultura agrícola mais adequada com base em características do solo e condições climáticas.

O objetivo foi aplicar técnicas de Inteligência Artificial para auxiliar na tomada de decisão agronômica,
simulando um sistema inteligente de recomendação agrícola.

---

### 🎯 Objetivo

Dado um conjunto de atributos ambientais e químicos do solo:

- Nitrogênio (**N**)
- Fósforo (**P**)
- Potássio (**K**)
- Temperatura
- Umidade
- pH
- Índice de chuva

o modelo prevê a cultura agrícola mais compatível, como:

```text
rice
banana
maize
cotton
mango
```

### Pipeline de Tratamento dos Dados
Foi implementado um pipeline completo de preparação dos dados:

✅ carregamento do dataset <br>
✅ normalização dos tipos numéricos <br>
✅ padronização textual dos labels <br>
✅ tratamento de valores nulos usando mediana <br>
✅ remoção de duplicidades <br>
✅ aplicação de regras de validação agronômica <br>

### Análise Exploratória (EDA)
Foram geradas análises exploratórias para compreender o comportamento dos dados:

. distribuição das culturas <br>
. histograma de temperatura <br>
. histograma de pH <br>
. scatter plot de umidade vs chuva <br>
. mapa de correlação entre variáveis <br>
. boxplot comparativo de pH por cultura <br>

Além disso, foi realizado estudo de perfil médio para culturas como:

Rice
Banana
Maize

permitindo identificar padrões ideais de cultivo.

Por que escolhi eses: Para se ter melhor ideia de predições e análises, assim, comigo adotando mais plantios, poderia ter uma visão sobre o funcionamento do modelo sobre os insumos.

### Modelos de Machine Learning Utilizados

Foram treinados e comparados 5 algoritmos supervisionados:
| Modelo              | Finalidade                   |
| ------------------- | ---------------------------- |
| Logistic Regression | baseline estatístico         |
| Random Forest       | ensemble robusto             |
| Decision Tree       | árvore interpretável         |
| SVM                 | separação por hiperplano     |
| KNN                 | classificação por vizinhança |

### Pipeline de Treinamento
```text
Dataset
   ↓
Pré-processamento
   ↓
Separação X / y
   ↓
Train/Test Split (80/20)
   ↓
StandardScaler (quando necessário)
   ↓
Treinamento dos modelos
   ↓
Predição
   ↓
Avaliação comparativa
```
Configuração:

        - treino: 80%
        - teste: 20%
        - random_state: 42
        - estratificação das classes

Métricas Utilizadas

Cada modelo foi avaliado com:

        - Accuracy
        - Classification Report
        - Precision
        - Recall
        - F1-score
        - Confusion Matrix

### 🏆 Comparação Final dos Modelos

Após o treinamento e avaliação dos modelos supervisionados, foi obtido o seguinte desempenho:

| Modelo | Accuracy |
|--------|----------|
| Random Forest | 90.00% |
| Decision Tree | 90.00% |
| Logistic Regression | 77.50% |
| SVM | 77.50% |
| KNN | 67.50% |

---

### 📌 Análise dos Resultados

Os melhores desempenhos foram obtidos pelos algoritmos **Random Forest** e **Decision Tree**, ambos com **90% de acurácia**.

Esse resultado indica que o problema possui padrões de decisão mais compatíveis com algoritmos baseados em árvores, capazes de capturar relações não lineares entre nutrientes do solo, temperatura, umidade e índice de chuva.

A **Logistic Regression** e o **SVM** apresentaram desempenho intermediário (**77,5%**), sugerindo que modelos mais lineares ou dependentes de separação geométrica simples não conseguiram representar tão bem a complexidade dos dados agrícolas.

O **KNN** apresentou o menor desempenho (**67,5%**), possivelmente devido à sensibilidade à escala dos dados e à sobreposição entre classes agrícolas.

---

### ✅ Conclusão

Considerando desempenho, robustez e capacidade de generalização, o modelo **Random Forest** foi considerado a melhor escolha para este projeto.

Esse algoritmo demonstra maior potencial para aplicação em sistemas inteligentes de apoio à decisão agrícola, permitindo recomendar culturas com maior confiabilidade a partir das características ambientais e químicas do solo.

Regras aplicadas:

| Validação   | Regra          |
| ----------- | -------------- |
| Nitrogênio  | ≥ 0            |
| Fósforo     | ≥ 0            |
| Potássio    | ≥ 0            |
| Temperatura | entre 0 e 60°C |
| Umidade     | entre 0 e 100% |
| pH          | entre 0 e 14   |
| Chuva       | ≥ 0            |

---

## 🗂️ Sobre os Dados — `sensores_farmtech_v2.csv`

Base com **200 registros simulados** ao longo de janeiro de 2025:

| Coluna | Descrição | Faixa |
|--------|-----------|-------|
| `timestamp` | Data e hora da leitura | Jan/2025 |
| `umidade` | Umidade do solo (%) | 25 – 95% |
| `ph` | pH do solo | 5,5 – 7,0 |
| `nitrogenio` | Nitrogênio (mg/kg) | 10 – 140 |
| `fosforo` | Fósforo (mg/kg) | 5 – 145 |
| `potassio` | Potássio (mg/kg) | 10 – 205 |
| `chuva` | Previsão de chuva (0/1) | Binário |
| `irrigacao` | Bomba acionada (0/1) | Binário |

---

## 📁 Estrutura do Repositório

```
📦 farmtech-solutions
 ┣ 📂 esp32
 ┃ ┗ 📄 sketch.ino                  → Código C/C++ do ESP32
 ┣ 📂 python
 ┃ ┣ 📄 clima.py                    → Integração com API OpenWeather
 ┃ ┣ 📄 dashboard.py                → Dashboard Streamlit (Fase 3)
 ┃ ┗ 📄 sensores_farmtech_v2.csv    → Base de dados simulada (Fase 3)
 ┣ 📂 imagens
 ┃ ┣ 📄 circuito.png                → Print do circuito no Wokwi
 ┃ ┣ 📄 oracle_print.png            → Print do banco Oracle (Fase 3)
 ┃ ┗ 📄 dashboard_print.png         → Print do dashboard (Fase 3)
 ┣ 📄 diagram.json                  → Diagrama do circuito Wokwi
 ┗ 📄 README.md                     → Este arquivo
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

---

## 🎥 Vídeos Demonstrativos

| Fase | Link |
|------|------|
| Fase 2 — ESP32 + Wokwi | [Assistir no YouTube](https://www.youtube.com/watch?v=OxzF6pPU_3E) |
| Fase 3 — Banco de dados | [Assistir no YouTube](#) *(a adicionar)* |
| Fase 3.1 - modelagem — Dashboard e ML | [Assistir no YouTube](https://youtu.be/x8uJeT7SODM) |

---


## 📚 Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| C/C++ | Programação do ESP32 |
| Python | Integração climática + Dashboard |
| Streamlit | Framework do dashboard |
| Plotly | Gráficos interativos |
| Pandas | Manipulação dos dados |
| Wokwi | Simulação do circuito |
| OpenWeather API | Dados meteorológicos em tempo real |
| Oracle SQL Developer | Banco de dados relacional |

---

<p align="center">
  FarmTech Solutions © 2025 — FIAP Inteligência Artificial — Fases 2 & 3
</p>
