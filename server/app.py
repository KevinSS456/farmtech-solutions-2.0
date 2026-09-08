# ================================================================
# FARMTECH SOLUTIONS - Servidor Flask
# Recebe dados do ESP32 (HTTP POST), grava no Oracle e disponibiliza
# um dashboard HTML com os últimos dados coletados.
# ================================================================

import os
from flask import Flask, request, jsonify, render_template
import oracledb
from datetime import datetime

app = Flask(__name__)

# ==========================================================
# CONFIGURAÇÃO DO BANCO ORACLE
# Em produção (Render), configure essas variáveis em
# Settings > Environment no painel do Render.
# Localmente, você pode só trocar os valores padrão abaixo.
# ==========================================================
DB_USER = os.environ.get("DB_USER", "SEU_USUARIO")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "SUA_SENHA")
DB_DSN = os.environ.get("DB_DSN", "oracle.fiap.com.br:1521/ORCL")


def get_connection():
    """Abre uma nova conexão com o Oracle (modo thin, sem precisar instalar Oracle Client)."""
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)


@app.route("/api/dados", methods=["POST"])
def receber_dados():
    """Recebe o JSON enviado pelo ESP32 e grava no banco Oracle."""
    try:
        dados = request.get_json(force=True)

        temperatura = dados.get("temperatura")
        umidade_ar = dados.get("umidade_ar")
        umidade_solo = dados.get("umidade_solo")

        conexao = get_connection()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO FARMTECH_SENSORES (TEMPERATURA, UMIDADE_AR, UMIDADE_SOLO)
            VALUES (:1, :2, :3)
            """,
            [temperatura, umidade_ar, umidade_solo],
        )

        conexao.commit()
        cursor.close()
        conexao.close()

        print(f"[{datetime.now()}] Dados recebidos: {dados}")
        return jsonify({"status": "ok", "mensagem": "Dados salvos com sucesso!"}), 201

    except Exception as erro:
        print("Erro ao salvar dados:", erro)
        return jsonify({"status": "erro", "mensagem": str(erro)}), 500


@app.route("/api/dados", methods=["GET"])
def listar_dados():
    """Retorna os últimos 20 registros em JSON, usados pelo dashboard."""
    try:
        conexao = get_connection()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT * FROM (
                SELECT TEMPERATURA, UMIDADE_AR, UMIDADE_SOLO, DATA_HORA
                FROM FARMTECH_SENSORES
                ORDER BY DATA_HORA DESC
            ) WHERE ROWNUM <= 20
            """
        )

        colunas = [col[0].lower() for col in cursor.description]
        resultado = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

        # Converte timestamp para string (para virar JSON válido)
        for linha in resultado:
            if linha.get("data_hora"):
                linha["data_hora"] = linha["data_hora"].strftime("%d/%m/%Y %H:%M:%S")

        cursor.close()
        conexao.close()

        return jsonify(resultado), 200

    except Exception as erro:
        print("Erro ao buscar dados:", erro)
        return jsonify({"status": "erro", "mensagem": str(erro)}), 500


@app.route("/")
def dashboard():
    """Página HTML do dashboard."""
    return render_template("dashboard.html")


if __name__ == "__main__":
    # O Render define a porta via variável de ambiente PORT.
    # Localmente, se PORT não existir, usa 5000 como padrão.
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=True)
