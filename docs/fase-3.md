# 🌱 FarmTech Solutions — Fase 3

![FIAP](https://img.shields.io/badge/FIAP-Inteligência%20Artificial-blue)
![Fase](https://img.shields.io/badge/Fase-3-brightgreen)
![Cultura](https://img.shields.io/badge/Cultura-Café-brown)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)

## 👥 Integrantes

| Nome           |
| -------------- |
| Thiese Novaes  |
| João Vitor     |
| Talles Duran   |
| Kevin Santiago |
| Renan de Souza |

---

## 🗄️ Fase 3 — Banco de Dados Oracle

Realizamos a instalação do Oracle SQL Developer (Windows), através do link
https://www.oracle.com/database/sqldeveloper/technologies/download/.

![Download Oracle](../imagens/Oracle_Download.png)

Após a instalação, descompactamos o arquivo e executamos o programa SQLDeveloper.

![EXE Oracle](../imagens/Oracle_exe.png)

Ao abrir o programa, clicamos no ícone "+" (Nova conexão) em verde.

![Conexão Oracle](../imagens/Oracle_Conexao.png)

Estabelecemos uma conexão com o banco de dados Oracle:

| Campo   | Valor                     |
| ------- | ------------------------- |
| Host    | oracle.fiap.com.br        |
| Porta   | 1521                      |
| SID     | ORCL                      |
| Usuário | RM + número (ex: RM12345) |
| Senha   | Data de nascimento (DDMMYY) |

![Conexão DB Oracle](../imagens/Oracle_Db.png)

Depois, testamos a conexão para garantir sucesso.

![Conexão Success Oracle](../imagens/Oracle_Success.png)

Assim que conectado, clicamos no campo "Tabelas (Filtrado)", e selecionamos o campo
"Importar Dados".

![Import Oracle](../imagens/Oracle_Import.png)

Importamos os dados coletados da Fase 2, clicando em "Procurar...".

![Import Csv Oracle](../imagens/Oracle_Import_Csv.png)

Clicamos em "Próximo", e editamos o nome da nossa tabela para "SENSORES_FARMTECH" no campo
"Nome da Tabela", garantindo que não possua espaços, nem caracteres especiais ou mais que 30 caracteres.

![Rename Table Oracle](../imagens/Oracle_Rename.png)

Novamente clicamos em "Próximo", e importamos todos os dados coletados no arquivo csv, selecionando
"Próximo" mais uma vez.

![Filter Table Oracle](../imagens/Oracle_no_Filter.png)

Após, temos a opção de alterar o nome das colunas e seu tipo de dado.
Clicamos novamente em "Próximo".

![Column Table Oracle](../imagens/Oracle_Column.png)

Por fim, clique em "Próximo", e depois "Finalizar" e aparecerá uma mensagem informando que a tarefa foi bem-sucedida.

![Import Table Success Oracle](../imagens/Oracle_Import_Success.png)

Realizamos a consulta SQL na tabela importada.

![Query Oracle](../imagens/Oracle_Query.png)

A consulta foi realizada com sucesso, permitindo validar que os dados da Fase 2 foram importados corretamente para o banco Oracle.

---

## 📊 Fase 3 — Dashboard Interativo

Dashboard desenvolvido em **Python + Streamlit** para visualização dos dados dos sensores.

### Como executar

```bash
pip install streamlit plotly pandas
python -m streamlit run dashboard.py
```

> ⚠️ Deve rodar o script dentro da pasta do arquivo.

### Funcionalidades

| Seção                   | Descrição                                                            |
| ----------------------- | -------------------------------------------------------------------- |
| 📡 Leitura Mais Recente | Cards com umidade, pH, N, P, K e chuva                               |
| 🚿 Status da Irrigação  | Bomba ligada/desligada + sugestões automáticas                       |
| 📆 Visão Semanal        | Médias de todas as variáveis + ativações da bomba por semana (S1–S4) |
| 💧 Umidade & pH         | Série temporal com faixas ideais                                     |
| 🌿 NPK                  | Evolução de N, P, K com limiares mínimos                             |
| 🚿 Irrigação            | Barras por dia + distribuição de estados                             |
| 📊 Correlações          | Scatter plot interativo entre variáveis                              |

### Print do dashboard

![Dashboard](../imagens/dashboard_print.png)

![Dashboard](https://github.com/user-attachments/assets/950c7549-266e-4ad0-ad2f-490671a0754b)

![Dashboard](https://github.com/user-attachments/assets/9f0897d2-f38f-47fe-820a-95483ee33f29)

![Dashboard](https://github.com/user-attachments/assets/567d8a3c-69d6-4122-b205-6fb2fc7b6b0e)

---

## 📁 Estrutura do Repositório

```text
📦 farmtech-solutions
 ┣ 📂 esp32
 ┃ ┗ 📄 sketch.ino                  → Código C/C++ do ESP32
 ┣ 📂 dashboard
 ┃ ┣ 📄 dashboard.py
 ┃ ┣ 📄 sensores_farmtech_v2.csv
 ┃ ┗ 📂 pages
 ┃    ┣ 📄 2_🤖_ML_Regressao_Fase4.py
 ┃    ┗ 📄 3_📈_IrAlem2_Tendencias.py
 ┣ 📂 python
 ┃ ┣ 📄 clima.py                    → Integração com API OpenWeather
 ┃ ┣ 📄 ingestao_sensores.py
 ┣ 📂 ML
 ┃ ┣ 📂 csvs
 ┃ ┃ ┗ 📄 sensores_farmtech_v2.csv  → Base de dados dos sensores
 ┃ ┣ 📂 outputs                     → Gráficos, métricas e modelos exportados
 ┃ ┣ 📄 ml_farmtech_regressao.py    → Pipeline de regressão (Fase 4)
 ┃ ┣ 📄 modelos.py                  → Pipeline de classificação (Fase anterior)
 ┃ ┣ 📄 eda.py                      → Análise exploratória
 ┃ ┗ 📄 pipeline.py                 → Preparação de dados
 ┣ 📂 imagens
 ┃ ┣ 📄 circuito.png                → Print do circuito no Wokwi
 ┃ ┣ 📄 oracle_print.png            → Print do banco Oracle (Fase 3)
 ┃ ┗ 📄 dashboard_print.png         → Print do dashboard (Fase 3)
 ┣ 📄 diagram.json                  → Diagrama do circuito Wokwi
 ┗ 📄 README.md                     → Este arquivo
```
