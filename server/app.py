
# ================================================================
# FARMTECH SOLUTIONS - SERVIDOR FLASK
# ESP32 -> Flask -> Oracle -> Dashboard
# ================================================================

import os
from datetime import datetime

import oracledb
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ================================================================
# CONFIGURAÇÃO DO ORACLE
# ================================================================

DB_USER = os.environ.get("DB_USER", "SEU_USUARIO")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "SUA_SENHA")
DB_DSN = os.environ.get("DB_DSN", "oracle.fiap.com.br:1521/ORCL")


def get_connection():
    """Abre conexão com o Oracle usando o modo Thin."""
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )


# ================================================================
# CONVERSÃO DOS ESTADOS BOOLEANOS
# ================================================================

def converter_booleano(valor):
    """
    Converte os estados recebidos para NUMBER(1).
    True = 1 | False = 0 | None = NULL
    """

    if valor is None:
        return None

    if isinstance(valor, bool):
        return 1 if valor else 0

    if isinstance(valor, (int, float)) and valor in (0, 1):
        return int(valor)

    if isinstance(valor, str):
        valor = valor.strip().upper()

        if valor in ("TRUE", "1", "SIM", "ATIVO", "LIGADA"):
            return 1

        if valor in ("FALSE", "0", "NAO", "NÃO", "INATIVO", "DESLIGADA"):
            return 0

    raise ValueError(f"Estado inválido: {valor}")


# ================================================================
# POST - RECEBER E SALVAR DADOS DO ESP32
# ================================================================

@app.route("/api/dados", methods=["POST"])
def receber_dados():

    conexao = None
    cursor = None

    try:
        dados = request.get_json(silent=True)

        if not isinstance(dados, dict):
            return jsonify({
                "status": "erro",
                "mensagem": "JSON inválido ou ausente."
            }), 400

        # Indicadores ambientais
        temperatura = dados.get("temperatura")
        umidade_ar = dados.get("umidade_ar")
        umidade_solo = dados.get("umidade_solo")

        if any(valor is None for valor in (
            temperatura, umidade_ar, umidade_solo
        )):
            return jsonify({
                "status": "erro",
                "mensagem": "Indicadores ambientais obrigatórios ausentes."
            }), 400

        # Novos indicadores
        estado_n = converter_booleano(dados.get("estado_n"))
        estado_p = converter_booleano(dados.get("estado_p"))
        estado_k = converter_booleano(dados.get("estado_k"))

        previsao_chuva = converter_booleano(
            dados.get("previsao_chuva")
        )

        bomba_irrigacao = converter_booleano(
            dados.get("bomba_irrigacao")
        )

        conexao = get_connection()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO FARMTECH_SENSORES (
                TEMPERATURA,
                UMIDADE_AR,
                UMIDADE_SOLO,
                ESTADO_N,
                ESTADO_P,
                ESTADO_K,
                PREVISAO_CHUVA,
                BOMBA_IRRIGACAO
            )
            VALUES (
                :temperatura,
                :umidade_ar,
                :umidade_solo,
                :estado_n,
                :estado_p,
                :estado_k,
                :previsao_chuva,
                :bomba_irrigacao
            )
            """,
            {
                "temperatura": float(temperatura),
                "umidade_ar": float(umidade_ar),
                "umidade_solo": float(umidade_solo),
                "estado_n": estado_n,
                "estado_p": estado_p,
                "estado_k": estado_k,
                "previsao_chuva": previsao_chuva,
                "bomba_irrigacao": bomba_irrigacao
            }
        )

        conexao.commit()

        print(f"[{datetime.now()}] Dados recebidos: {dados}")

        return jsonify({
            "status": "ok",
            "mensagem": "Dados FarmTech salvos com sucesso!"
        }), 201

    except Exception as erro:

        if conexao:
            conexao.rollback()

        print("Erro ao salvar dados:", erro)

        return jsonify({
            "status": "erro",
            "mensagem": str(erro)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conexao:
            conexao.close()


# ================================================================
# GET - CONSULTAR DADOS PARA O DASHBOARD
# ================================================================

@app.route("/api/dados", methods=["GET"])
def listar_dados():

    conexao = None
    cursor = None

    try:
        conexao = get_connection()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT * FROM (
                SELECT
                    TEMPERATURA,
                    UMIDADE_AR,
                    UMIDADE_SOLO,
                    ESTADO_N,
                    ESTADO_P,
                    ESTADO_K,
                    PREVISAO_CHUVA,
                    BOMBA_IRRIGACAO,
                    DATA_HORA
                FROM FARMTECH_SENSORES
                ORDER BY DATA_HORA DESC
            )
            WHERE ROWNUM <= 20
            """
        )

        colunas = [
            coluna[0].lower()
            for coluna in cursor.description
        ]

        resultado = [
            dict(zip(colunas, linha))
            for linha in cursor.fetchall()
        ]

        # Converte timestamp para texto compatível com JSON
        for linha in resultado:

            if linha.get("data_hora"):
                linha["data_hora"] = linha["data_hora"].strftime(
                    "%d/%m/%Y %H:%M:%S"
                )

        return jsonify(resultado), 200

    except Exception as erro:

        print("Erro ao buscar dados:", erro)

        return jsonify({
            "status": "erro",
            "mensagem": str(erro)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conexao:
            conexao.close()


# ================================================================
# DASHBOARD
# ================================================================

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ================================================================
# EXECUÇÃO
# ================================================================

if __name__ == "__main__":

    porta = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=porta,
        debug=False
    )
