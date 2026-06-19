# 🤖 Fase 4 — Machine Learning para Previsão de Culturas Agrícolas

Como extensão da solução FarmTech Solutions, foi desenvolvido um módulo de **Machine Learning supervisionado** capaz de prever a cultura agrícola mais adequada com base em características do solo e condições climáticas.

O objetivo foi aplicar técnicas de Inteligência Artificial para auxiliar na tomada de decisão agronômica, simulando um sistema inteligente de recomendação agrícola.

---

## 🎯 Objetivo

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

---

## Pipeline de Tratamento dos Dados

Foi implementado um pipeline completo de preparação dos dados:

✅ carregamento do dataset  
✅ normalização dos tipos numéricos  
✅ padronização textual dos labels  
✅ tratamento de valores nulos usando mediana  
✅ remoção de duplicidades  
✅ aplicação de regras de validação agronômica  

---

## Análise Exploratória (EDA)

Foram geradas análises exploratórias para compreender o comportamento dos dados:

- distribuição das culturas  
- histograma de temperatura  
- histograma de pH  
- scatter plot de umidade vs chuva  
- mapa de correlação entre variáveis  
- boxplot comparativo de pH por cultura  

Além disso, foi realizado estudo de perfil médio para culturas como:

- Rice
- Banana
- Maize

permitindo identificar padrões ideais de cultivo.

---

## Modelos de Machine Learning Utilizados

Foram treinados e comparados 5 algoritmos supervisionados:

| Modelo | Finalidade |
| --- | --- |
| Logistic Regression | baseline estatístico |
| Random Forest | ensemble robusto |
| Decision Tree | árvore interpretável |
| SVM | separação por hiperplano |
| KNN | classificação por vizinhança |

---

## Pipeline de Treinamento

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

---

## Métricas Utilizadas

Cada modelo foi avaliado com:

- Accuracy
- Classification Report
- Precision
- Recall
- F1-score
- Confusion Matrix

---

## 🏆 Comparação Final dos Modelos

Após o treinamento e avaliação dos modelos supervisionados, foi obtido o seguinte desempenho:

| Modelo | Accuracy |
| --- | --- |
| Random Forest | 90.00% |
| Decision Tree | 90.00% |
| Logistic Regression | 77.50% |
| SVM | 77.50% |
| KNN | 67.50% |

---

## 📌 Análise dos Resultados

Os melhores desempenhos foram obtidos pelos algoritmos **Random Forest** e **Decision Tree**, ambos com **90% de acurácia**.

Esse resultado indica que o problema possui padrões de decisão mais compatíveis com algoritmos baseados em árvores, capazes de capturar relações não lineares entre nutrientes do solo, temperatura, umidade e índice de chuva.

A **Logistic Regression** e o **SVM** apresentaram desempenho intermediário (**77,5%**), sugerindo que modelos mais lineares ou dependentes de separação geométrica simples não conseguiram representar tão bem a complexidade dos dados agrícolas.

O **KNN** apresentou o menor desempenho (**67,5%**), possivelmente devido à sensibilidade à escala dos dados e à sobreposição entre classes agrícolas.

---

## ✅ Conclusão

Considerando desempenho, robustez e capacidade de generalização, o modelo **Random Forest** foi considerado a melhor escolha para este projeto.

Esse algoritmo demonstra maior potencial para aplicação em sistemas inteligentes de apoio à decisão agrícola, permitindo recomendar culturas com maior confiabilidade a partir das características ambientais e químicas do solo.

---

## Regras aplicadas

| Validação | Regra |
| --- | --- |
| Nitrogênio | ≥ 0 |
| Fósforo | ≥ 0 |
| Potássio | ≥ 0 |
| Temperatura | entre 0 e 60°C |
| Umidade | entre 0 e 100% |
| pH | entre 0 e 14 |
| Chuva | ≥ 0 |
