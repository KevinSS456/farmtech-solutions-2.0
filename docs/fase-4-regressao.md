# 📈 Fase 4 — Machine Learning para Previsão de Variáveis Agrícolas (Regressão)

Como continuação do módulo de Machine Learning da FarmTech Solutions, foi desenvolvido um pipeline completo de **regressão supervisionada** para prever variáveis críticas do solo e estimar o rendimento da lavoura de café.

Diferentemente da fase anterior (classificação de culturas), esta fase foca em **prever valores numéricos contínuos** como umidade do solo, pH e um índice de rendimento estimado, gerando recomendações automáticas de manejo.

---

## 🎯 Objetivos

Dado um conjunto de leituras dos sensores:

- Nitrogênio (**N**)
- Fósforo (**P**)
- Potássio (**K**)
- Previsão de chuva
- Hora e dia da leitura

os modelos preveem:

```text
Umidade do Solo (%)
pH do Solo
Rendimento Estimado (índice 0–100)
```

---

## 🔄 Pipeline de Tratamento dos Dados

Foi implementado um pipeline completo de preparação dos dados:

✅ carregamento do dataset `sensores_farmtech_v2.csv`  
✅ conversão e ordenação por timestamp  
✅ extração de features temporais (hora e dia)  
✅ tratamento de valores nulos com mediana  
✅ remoção de duplicatas  
✅ criação do índice de rendimento estimado (feature agronômica ponderada)  

### Fórmula do Rendimento Estimado

```text
rendimento = (
    0.30 × (N / 140)    +
    0.20 × (P / 145)    +
    0.20 × (K / 205)    +
    0.20 × (umidade normalizada na faixa ideal) +
    0.10 × (pH normalizado na faixa do café)
) × 100
```

---

## 🤖 Modelos de Regressão Utilizados

Foram treinados e comparados **3 algoritmos** para cada variável-alvo:

| Modelo | Tipo | Finalidade |
| --- | --- | --- |
| Random Forest Regressor | Ensemble não-linear | Captura relações complexas entre sensores |
| Regressão Linear | Linear | Baseline interpretável |
| Regressão Polinomial (grau 2 + Ridge) | Não-linear | Captura interações entre features |

---

## ⚙️ Pipeline de Treinamento

```text
Dataset (sensores_farmtech_v2.csv)
   ↓
Pré-processamento
   ↓
Extração de features temporais
   ↓
Separação X / y por target
   ↓
Train/Test Split (80/20)
   ↓
StandardScaler + Pipeline
   ↓
Treinamento dos 3 modelos por target
   ↓
Avaliação com MAE, MSE, RMSE e R²
   ↓
Validação Cruzada (5 folds)
   ↓
Seleção do melhor modelo por R²
   ↓
Exportação dos modelos (.pkl) e previsões (.csv)
```

Configuração:

- Treino: 80%
- Teste: 20%
- random_state: 42
- Validação cruzada: 5 folds

---

## 📐 Métricas Utilizadas

Cada modelo foi avaliado com:

- MAE — Erro Médio Absoluto
- MSE — Erro Quadrático Médio
- RMSE — Raiz do Erro Quadrático Médio
- R² — Coeficiente de Determinação
- Cross-Val R² — Validação cruzada 5 folds

---

## 🏆 Resultados por Target

| Target | Melhor Modelo | MAE | RMSE | R² |
| --- | --- | --- | --- | --- |
| Umidade do Solo (%) | Random Forest | 5.79 | 6.87 | 0.72 |
| pH do Solo | Regressão Linear | 0.42 | 0.46 | -0.12 |
| Rendimento Estimado | Regressão Linear | 6.53 | 7.71 | 0.61 |

---

## 📌 Análise dos Resultados

O **Random Forest Regressor** obteve o melhor desempenho para previsão de **umidade** (R² = 0.72), confirmando que relações não-lineares entre os nutrientes do solo e a umidade são melhor capturadas por modelos de ensemble.

Para o **rendimento estimado**, a **Regressão Linear** foi suficiente (R² = 0.61), pois o índice foi construído como combinação linear ponderada das features, o que naturalmente favorece modelos lineares.

Para o **pH**, todos os modelos apresentaram R² negativo. Isso é esperado e foi documentado: a análise de correlação revelou que o pH neste dataset possui correlação próxima de zero com todas as outras variáveis, pois na realidade agrícola o pH é influenciado por fatores externos como aplicação de calcário e acidez da chuva, variáveis não presentes nos sensores simulados.

---

## 🌿 Sistema de Recomendações

Com base nas previsões dos modelos, o script gera recomendações automáticas de irrigação e manejo:

| Condição Prevista | Recomendação |
| --- | --- |
| Umidade < 60% | 💧 IRRIGAR — volume estimado em L/m² |
| Umidade > 80% | ⚠️ NÃO irrigar — solo encharcado |
| Chuva prevista | 🌧️ SUSPENDER irrigação |
| pH < 6.0 | 🧪 Aplicar calcário dolomítico |
| pH > 6.5 | 🧪 Aplicar enxofre agrícola |
| N < 80 mg/kg | 🌿 Aplicar ureia ou nitrato de amônio |
| P < 30 mg/kg | 🌿 Aplicar superfosfato simples |
| K < 100 mg/kg | 🌿 Aplicar cloreto de potássio |

---

## 📊 Gráficos Gerados

| Arquivo | Descrição |
| --- | --- |
| `01_correlacao.png` | Mapa de correlação entre todas as variáveis |
| `02_predito_vs_real.png` | Valores preditos vs reais para os 3 targets |
| `03_residuos.png` | Análise de resíduos (dispersão) |
| `04_comparacao_modelos.png` | RMSE e R² comparados entre os 3 modelos |
| `05_feature_importance.png` | Importância de cada feature no modelo de umidade |
| `06_serie_temporal_umidade.png` | Série temporal: umidade real vs predita |
| `07_tendencia_rendimento.png` | Tendência de rendimento ao longo de janeiro/2025 |
| `08_histograma_residuos.png` | Distribuição dos resíduos por target |

---

## 📁 Arquivos da Fase 4 — Regressão

```text
ML/
 ├── csvs/
 │   └── sensores_farmtech_v2.csv        → Base de dados dos sensores (200 registros)
 ├── outputs/
 │   ├── 01_correlacao.png               → Mapa de correlação
 │   ├── 02_predito_vs_real.png          → Predito vs Real
 │   ├── 03_residuos.png                 → Análise de resíduos
 │   ├── 04_comparacao_modelos.png       → Comparação de modelos
 │   ├── 05_feature_importance.png       → Importância das features
 │   ├── 06_serie_temporal_umidade.png   → Série temporal de umidade
 │   ├── 07_tendencia_rendimento.png     → Tendência de rendimento
 │   ├── 08_histograma_residuos.png      → Histograma de resíduos
 │   ├── metricas_modelos.csv            → Métricas de todos os modelos
 │   ├── previsoes_farmtech.csv          → Dataset com previsões (para o dashboard)
 │   └── todos_modelos.pkl               → Modelos treinados exportados
 └── ml_farmtech_regressao.py            → Pipeline completo de regressão
```

### Como executar

```bash
pip install scikit-learn pandas numpy matplotlib seaborn joblib
python ML/ml_farmtech_regressao.py
```

> ⚠️ Deve rodar o script a partir da raiz do projeto.
