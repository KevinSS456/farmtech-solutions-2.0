# 🗄️ Ir Além 1 — Ingestão Automática de Dados IoT no Oracle

Como extensão da Fase 3, onde a importação dos dados no Oracle foi feita manualmente via SQL Developer, foi desenvolvido um script de **ingestão automática** que elimina a necessidade de importação manual.

---

## O que o script faz

1. Conecta no banco Oracle da FIAP usando credenciais lidas de um arquivo `.env`.
2. Cria a tabela `SENSORES_FARMTECH_IOT` automaticamente, caso ela ainda não exista.
3. Realiza a **população inicial**, carregando o histórico do `sensores_farmtech_v2.csv`, executada apenas uma vez, na primeira execução.
4. Entra em um **loop contínuo**: a cada 5 segundos, gera uma nova leitura simulada e insere automaticamente no banco, sem nenhuma intervenção manual.

---

## Como executar

```bash
pip install oracledb pandas python-dotenv --break-system-packages
```

---

## Observação

Esse script foi pensado para demonstrar a evolução da solução, saindo de uma importação manual para uma ingestão automatizada de dados IoT.
