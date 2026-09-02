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

- [Entrega 1 — Machine Learning](#entrega-1--machine-learning)
- [Entrega 2 — Computação em Nuvem](#entrega-2--computação-em-nuvem)
  - [Contexto](#contexto)
  - [Requisitos da atividade](#requisitos-da-atividade)
  - [Comparação de custos (AWS Pricing Calculator)](#comparação-de-custos-aws-pricing-calculator)
  - [Latência](#latência)
  - [Arquitetura](#arquitetura)
  - [Integração com a Entrega 1](#integração-com-a-entrega-1)
  - [LGPD e restrição de armazenamento no exterior](#lgpd-e-restrição-de-armazenamento-no-exterior)
  - [Matriz de decisão](#matriz-de-decisão)
  - [Decisão final](#decisão-final)
- [Apresentação visual complementar](#apresentação-visual-complementar)
- [Referências](#referências)

## Integrantes

| Nome           |
| -------------- |
| Thiese Novaes | 572659 |
| João Vitor | 572969 |
| Talles Duran | 572772 |
| Kevin Santiago | 573808 |
| Renan Souza | 568958 |

## Resumo do projeto

O projeto começa com a simulação de sensores em um **ESP32** no Wokwi, passa pela integração com dados climáticos via **OpenWeather**, avança para o armazenamento dos dados em **Oracle** e culmina em uma camada de análise com **Streamlit** e **Machine Learning**.

A cultura escolhida foi o **café**, por ser relevante para o agronegócio brasileiro e permitir a aplicação de regras agronômicas ligadas a umidade, pH e NPK. (revisar)

## Entregas da Fase 4

### Parte principal da atividade

- Pipeline de Machine Learning com regressão usando Scikit-Learn (revisar)
- Integração das previsões com o dashboard em Streamlit
- Exibição de métricas, previsões e gráficos analíticos

### Ir Além 1

- Ingestão automática de dados IoT no banco Oracle (revisar)
- População inicial do histórico
- Atualização automática das leituras

### Ir Além 2

- Dashboard analítico com tendências de produtividade (revisar)
- Comparação de rendimento real vs previsto
- Correlação entre NPK e rendimento
- Indicador de tendência do rendimento

## Vídeos demonstrativos

> 📌 A entrega principal da Fase 4 está documentada no vídeo "Parte 1 e Parte 2 (Entrega Final)". Os vídeos Ir Além 1 e Ir Além 2 apresentam funcionalidades complementares desenvolvidas além dos requisitos obrigatórios. (revisar)

| Entrega                                    | Link                                                               |
| ------------------------------------------ | ------------------------------------------------------------------ |
| Fase 2 — ESP32 + Wokwi                     | [Assistir no YouTube](https://www.youtube.com/watch?v=OxzF6pPU_3E) |
| Fase 3 — Banco de dados                    | [Assistir no YouTube](https://youtu.be/jpHLyaU5JCU)                |
| Fase 3.1 — Dashboard e ML                  | [Assistir no YouTube](https://youtu.be/x8uJeT7SODM)                |
| Fase 4 — Ir Além 1                         | [Assistir no YouTube](https://youtu.be/MsFykLMK8zw)                |
| Fase 4 — Ir Além 2                         | [Assistir no YouTube](https://youtu.be/Y9oP9D3x01s)                |
| Fase 5 — Parte 1 (EDA)                     | [Assistir no YouTube](SEU_LINK_AQUI)                               |
| Fase 5 — Parte 2 (AWS)                     | [Assistir no YouTube](SEU_LINK_AQUI)                               |

## Como executar

## Entrega 1 — EDA e Machine Learning

### Objetivo

A Entrega 1 utiliza o dataset `crop_yield.csv` para desenvolver uma solução de **Machine Learning capaz de prever o rendimento agrícola (`Yield`)** a partir da cultura e de variáveis ambientais.

O fluxo implementado no notebook `pbl_fase5.ipynb` cobre preparação dos dados, análise exploratória, investigação de outliers, clusterização, treinamento de cinco modelos de regressão, comparação por métricas e validação cruzada.

### Dataset

A base analisada possui **156 registros e 6 variáveis**, distribuídos igualmente entre quatro culturas, com **39 observações por cultura**:

- `Cocoa, beans`;
- `Oil palm fruit`;
- `Rice, paddy`;
- `Rubber, natural`.

| Variável | Tipo | Papel |
|---|---|---|
| `Crop` | Categórica | Cultura agrícola |
| `Precipitation (mm day-1)` | Numérica | Precipitação |
| `Specific Humidity at 2 Meters (g/kg)` | Numérica | Umidade específica |
| `Relative Humidity at 2 Meters (%)` | Numérica | Umidade relativa |
| `Temperature at 2 Meters (C)` | Numérica | Temperatura |
| `Yield` | Numérica | Variável-alvo de rendimento |

A validação inicial confirmou que a base não possui valores ausentes, registros duplicados, valores infinitos, precipitação negativa, umidade específica negativa, umidade relativa fora da faixa de 0% a 100% ou `Yield` menor ou igual a zero.

### Etapas realizadas

1. preparação do ambiente e definição de `RANDOM_STATE = 42`;
2. carregamento e validação do dataset;
3. verificação da qualidade dos dados;
4. estatística descritiva;
5. análise exploratória dos dados (EDA);
6. identificação e análise de outliers com IQR;
7. clusterização com K-Means;
8. preparação das variáveis para regressão;
9. divisão estratificada em treino e teste;
10. treinamento de cinco modelos de regressão;
11. avaliação com MAE, RMSE e R²;
12. validação cruzada com 5 folds;
13. comparação entre valores reais e previstos;
14. análise de importância das variáveis;
15. análise das limitações e escolha do modelo final.

### Principais resultados da EDA

A análise exploratória mostrou que as quatro culturas possuem escalas de rendimento muito diferentes. As médias aproximadas de `Yield` foram:

| Cultura | Yield médio aproximado |
|---|---:|
| `Oil palm fruit` | 175,8 mil |
| `Rice, paddy` | 32,1 mil |
| `Cocoa, beans` | 8,9 mil |
| `Rubber, natural` | 7,8 mil |

Também foram identificados **39 perfis ambientais únicos**, cada um repetido quatro vezes — uma vez para cada cultura. Isso indica que as culturas foram observadas sob os mesmos conjuntos de condições ambientais.

Na correlação global, `Yield` apresenta baixa correlação linear com as variáveis ambientais. Porém, quando a análise é realizada por cultura, surgem relações mais claras, principalmente em `Rice, paddy` e `Rubber, natural`. Esse comportamento reforça que `Crop` é uma variável central para a modelagem.

### Análise de outliers

O método do **Intervalo Interquartil (IQR)** foi utilizado para investigar possíveis valores discrepantes.

Quando `Yield` é analisado globalmente, o IQR sinaliza **35 potenciais outliers**. Entretanto, esse resultado é causado principalmente pela diferença estrutural de escala entre as culturas, especialmente por `Oil palm fruit`.

Ao repetir o cálculo separadamente por cultura, o resultado é:

- `Cocoa, beans`: 0 outliers de `Yield`;
- `Oil palm fruit`: 0 outliers de `Yield`;
- `Rice, paddy`: 0 outliers de `Yield`;
- `Rubber, natural`: 0 outliers de `Yield`.

Por isso, **nenhuma observação foi removida**. Os 156 registros originais foram preservados para as etapas seguintes.

### Clusterização

A clusterização foi realizada com **K-Means**, utilizando as variáveis ambientais padronizadas. A escolha do número de grupos considerou o método do cotovelo e o **Silhouette Score**.

O melhor resultado foi obtido com:

- **k = 3**;
- Silhouette Score próximo de **0,40**.

Os clusters representam três cenários ambientais distintos. A distribuição encontrada foi:

| Cluster | Quantidade de registros |
|---|---:|
| 0 | 68 |
| 1 | 44 |
| 2 | 44 |

A análise mostrou que o efeito desses cenários sobre o rendimento varia conforme a cultura. Portanto, os clusters ajudam a descrever padrões ambientais, mas não substituem a informação contida em `Crop`.

### Preparação para a modelagem

A variável-alvo foi definida como `Yield`. Para as variáveis de entrada:

- `Crop` foi transformada com **OneHotEncoder**;
- as variáveis numéricas foram padronizadas com **StandardScaler**;
- o pré-processamento foi integrado aos modelos por meio de **Pipeline** e **ColumnTransformer**.

A base foi dividida em **80% treino e 20% teste**, com estratificação por cultura:

- treino: **124 registros**;
- teste: **32 registros**;
- cada cultura ficou com 31 registros no treino e 8 no teste.

### Modelos avaliados

Foram implementados cinco algoritmos de regressão:

1. **Regressão Linear**;
2. **Random Forest Regressor**;
3. **Gradient Boosting Regressor**;
4. **Support Vector Regression — SVR (RBF)**;
5. **K-Nearest Neighbors Regressor — KNN**.

### Resultado no conjunto de teste

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| Regressão Linear | 4.988,89 | 8.543,63 | 0,98 |
| Random Forest | **4.632,55** | 9.569,82 | 0,98 |
| Gradient Boosting | 5.892,41 | 9.993,33 | 0,98 |
| SVR (RBF) | 12.506,41 | 18.228,57 | 0,93 |
| KNN Regressor | 14.965,66 | 31.432,05 | 0,78 |

Os três primeiros modelos apresentaram resultados muito próximos. Nesta divisão específica, a Regressão Linear obteve o menor RMSE, enquanto o Random Forest apresentou o menor MAE.

### Validação cruzada

Para reduzir a dependência de uma única divisão treino/teste, foi aplicada **validação cruzada com 5 folds**.

| Modelo | R² médio | Desvio R² | MAE médio | RMSE médio |
|---|---:|---:|---:|---:|
| Gradient Boosting | 0,99 | 0,00 | 5.027,52 | 7.600,36 |
| Random Forest | 0,99 | 0,01 | **4.297,35** | **7.591,18** |
| Regressão Linear | 0,99 | 0,01 | 5.087,74 | 7.874,35 |
| SVR (RBF) | 0,93 | 0,03 | 11.977,87 | 18.153,26 |
| KNN Regressor | 0,82 | 0,08 | 14.320,86 | 29.256,18 |

A validação cruzada confirma que **Gradient Boosting, Random Forest e Regressão Linear** são os modelos mais consistentes para esta base.

### Modelo final escolhido

O **Random Forest Regressor** foi escolhido como modelo final prático.

A escolha considera em conjunto:

- desempenho elevado;
- menor MAE médio na validação cruzada;
- menor RMSE médio entre os modelos avaliados na validação cruzada;
- estabilidade entre diferentes partições dos dados;
- possibilidade de analisar a importância das variáveis.

A análise de importância também confirmou que a categoria `Oil palm fruit` domina grande parte das decisões do Random Forest, reforçando que a variável `Crop` explica uma parcela importante das diferenças de escala do rendimento.

### Limitações

Os resultados devem ser interpretados dentro das limitações do dataset:

- apenas 156 observações;
- somente 39 perfis ambientais únicos;
- forte influência da variável `Crop`;
- ausência de variáveis agrícolas como solo, fertilização, irrigação, pragas, manejo, variedade genética e radiação solar;
- correlação, clusterização e importância de variáveis não demonstram causalidade.

Assim, o modelo representa uma demonstração preditiva para o conjunto analisado e não deve ser entendido como uma solução universal para qualquer cenário agrícola.

### Arquivos e demonstração

- **Notebook principal:** [`pbl_fase5.ipynb`](./pbl_fase5.ipynb)
- **Dataset:** `crop_yield.csv`
- **Vídeo demonstrativo da Entrega 1:** *(inserir link do YouTube após a gravação)*

> PS: O vídeo também estará disponível na aba de Vídeos Ilustrativos

---

## Entrega 2 — Computação em Nuvem

### Contexto

O problema desta entrega não é apenas hospedar a Machine Learning da Entrega 1 — é escolher **onde** essa operação vai acontecer. A infraestrutura precisa receber, armazenar e processar dados dos sensores da fazenda (200 hectares) com previsibilidade e baixa latência. Para isso, comparamos as regiões **São Paulo (sa-east-1)** e **N. Virgínia (us-east-1)** sob três critérios: custo, proximidade da operação e governança de dados.

### Requisitos da atividade

| Requisito | Configuração escolhida | Status |
|---|---|---|
| Região | São Paulo (sa-east-1) × N. Virgínia (us-east-1) | ✅ Atende |
| Sistema operacional | Linux | ✅ Atende |
| Modelo de cobrança | On-Demand — 100% | ✅ Atende |
| vCPU | 2 | ✅ Atende |
| Memória | 1 GiB | ✅ Atende |
| Rede | Até 5 Gbps | ✅ Atende |
| Instância | t3.micro | ✅ Atende |
| Armazenamento | 50 GB — Amazon EBS gp3 | ✅ Atende |

A **t3.micro** foi selecionada por atender simultaneamente aos requisitos mínimos de 2 vCPU, 1 GiB de RAM e até 5 Gbps de rede, conforme a especificação oficial da AWS para esse tipo de instância — sendo a menor configuração da família T3 que cumpre todos os critérios do enunciado ao mesmo tempo.

> **⚠️ Ressalva técnica:** a t3.micro é uma instância *burstable* (família T3), com créditos de CPU acumulados por hora e desempenho de baseline por vCPU. Ela atende aos requisitos mínimos desta atividade, mas seus recursos são limitados para cargas de Machine Learning mais intensivas. Em produção, a instância deverá ser redimensionada conforme os resultados de monitoramento e consumo.

### Comparação de custos (AWS Pricing Calculator)

| Região | Total mensal (AWS Pricing Calculator) |
|---|---|
| N. Virgínia (us-east-1) | **US$ 11,59** ✅ *(confirmado via print)* |
| São Paulo (sa-east-1) | **US$ 19,86** ✅ *(confirmado via print)* |
| **Diferença** | **US$ 8,27/mês** (São Paulo é ~71% mais cara) |

![Comparação de custo mensal entre regiões](./assets/grafico-custo.png)

**Figura 1 — AWS Pricing Calculator: us-east-1**
`![Figura 1 — AWS Pricing Calculator us-east-1](./assets/print-us-east-1.png)`

**Figura 2 — AWS Pricing Calculator: sa-east-1**

![Figura 2 — AWS Pricing Calculator sa-east-1](./assets/print-sa-east-1.png)

Valores estimados utilizando a AWS Pricing Calculator, modelo On-Demand (100%), Linux/Unix, EC2 t3.micro e EBS gp3 de 50 GB. O valor de São Paulo foi confirmado diretamente na calculadora (US$ 19,86/mês); o de N. Virgínia o valor foi de US$ 11,59, mas a decisão não deve ser tomada apenas pelo menor preço.

### Latência

| Região | Latência estimada (RTT) |
|---|---|
| São Paulo (sa-east-1) | ~15 ms |
| N. Virgínia (us-east-1) | ~135 ms |

![Latência estimada por região](./assets/grafico-latencia.png)

Para IoT agrícola, distância física vira tempo de resposta: cada leitura de sensor e cada decisão automatizada de irrigação depende de ida e volta rápida entre o campo e a API.

 **Os valores devem ser validados por testes de conectividade realizados a partir do ambiente onde os sensores estarão instalados** — não representam benchmark oficial da AWS.

### Arquitetura

```
Sensores (ESP32)
      │
      ▼
   Internet
      │
      ▼
AWS São Paulo (sa-east-1)
┌───────────────────────┐
│  EC2 t3.micro          │
│  API + Machine Learning│
└───────────┬────────────┘
            │
            ▼
     EBS gp3 · 50 GB
   (armazenamento persistente)
```

- **Baixa latência:** dados e processamento ficam próximos da operação agrícola.
- **Escalabilidade:** a base pode evoluir para serviços gerenciados, filas, bancos e analytics.
- **Observabilidade:** monitoramento e métricas podem ser incorporados conforme a solução cresce.
- **Segurança:** IAM, criptografia, logs, backups e segmentação devem acompanhar a evolução.

> **Sobre o armazenamento:** para uma instância EC2, o armazenamento persistente é provisionado como **Amazon EBS**, e não como um disco físico interno. Foi utilizado o volume **gp3**, de uso geral, com 50 GB — cobrado conforme a capacidade provisionada, com desempenho de baseline incluído.

### Integração com a Entrega 1

Os sensores definidos na Entrega 1 produzem as variáveis (precipitação, umidade, temperatura) utilizadas pela solução FarmTech. Nesta etapa, a infraestrutura AWS é responsável por receber esses dados por meio de uma API, armazená-los e disponibilizá-los para o processamento e execução dos modelos de Machine Learning.

```
Entrega 1               API                 Armazenamento         Modelos de ML
Sensores (ESP32)  ──▶  EC2 t3.micro   ──▶   EBS gp3 (50GB)  ──▶   Previsão de
precipitação,          São Paulo             persistência          rendimento
umidade, temp.         sa-east-1             dos dados             de safra
```

### LGPD e restrição de armazenamento no exterior

- **Minimização:** coletar somente dados necessários para as finalidades definidas no projeto.
- **Segurança:** aplicar controles de acesso, criptografia, monitoramento e gestão de incidentes.
- **Governança:** definir responsabilidades, retenção, finalidade e trilhas de auditoria.
- **Transferência internacional:** se houver transferência internacional de dados pessoais, é necessário observar a LGPD e os mecanismos regulamentados pela ANPD.

**Ponto de atenção:** hospedar na região brasileira não significa, isoladamente, que toda operação esteja livre de transferências internacionais. A análise deve considerar o fluxo efetivo dos dados e os serviços utilizados.

> **Justificativa objetiva:** considerando a premissa do enunciado de que existe restrição ao armazenamento de dados no exterior, a FarmTech escolhe a região **sa-east-1 (São Paulo)**, pois mantém a infraestrutura de armazenamento principal no Brasil e reduz a complexidade associada ao fluxo internacional de dados. A arquitetura deve ainda verificar se outros serviços utilizados realizam processamento ou transferência internacional.

### Matriz de decisão

| Critério | São Paulo | N. Virgínia |
|---|---|---|
| Custo | 63 | 90 |
| Latência | 92 | 35 |
| Operação local / governança | 95 | 45 |

*Matriz qualitativa para apoio à decisão acadêmica; não representa benchmark oficial da AWS.*

### Decisão final

## São Paulo (sa-east-1) — escolhido por necessidade, não por preço.

1. **IoT:** menor latência estimada para uma operação agrícola localizada no Brasil.
2. **Governança:** arquitetura local simplifica a análise de fluxo de dados, sem substituir os controles de LGPD.
3. **Custo consciente:** diferença de referência de **+ US$ 8,27/mês** — um custo adicional conhecido e justificado pelo contexto, não ignorado.

---

## Apresentação visual complementar

Este README é o entregável oficial da atividade. Como material de apoio, o grupo também desenvolveu uma apresentação visual em HTML com o mesmo conteúdo, disponível em [`FarmTech_FIAP_Calculadora_AWS_v2.html`](./FarmTech_FIAP_Calculadora_AWS_v2.html).

**Vídeo (Entrega 2):** *(inserir link do YouTube, não listado, demonstrando a comparação de recursos na calculadora AWS)*

---

## Referências

- AWS. *AWS Pricing Calculator* e documentação de preços de Amazon EC2 e Amazon EBS. Consulta de referência: ago/2026.
- BRASIL. Lei nº 13.709/2018 — Lei Geral de Proteção de Dados Pessoais (LGPD).
- ANPD. Resolução CD/ANPD nº 19, de 23 de agosto de 2024 — Regulamento de Transferência Internacional de Dados.

<p align="center">
  FarmTech Solutions © 2026 — FIAP Inteligência Artificial
</p>
