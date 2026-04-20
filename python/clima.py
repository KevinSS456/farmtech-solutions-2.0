import requests

# ========== CONFIGURAÇÃO ==========
API_KEY = "5df915f30899a112c0fb6dfa3d64e8cd"
CIDADE = "São Paulo"
UNIDADE = "metric"


# ========== BUSCA O CLIMA ==========
def buscar_clima():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CIDADE}&appid={API_KEY}&units={UNIDADE}&lang=pt_br"

    try:
        resposta = requests.get(url)
        dados = resposta.json()

        if resposta.status_code != 200:
            print(f"Erro na API: {dados.get('message', 'Desconhecido')}")
            return None

        return dados

    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None


# ========== ANALISA O CLIMA ==========
def analisar_irrigacao(dados):
    if not dados:
        return

    cidade = dados["name"]
    temperatura = dados["main"]["temp"]
    umidade = dados["main"]["humidity"]
    descricao = dados["weather"][0]["description"]
    chuva = "rain" in dados["weather"][0]["main"].lower()

    print("====================================")
    print(" FarmTech Solutions - Café")
    print(" Análise Climática para Irrigação")
    print("====================================")
    print(f" Cidade      : {cidade}")
    print(f" Temperatura : {temperatura}°C")
    print(f" Umidade     : {umidade}%")
    print(f" Condição    : {descricao}")
    print("------------------------------------")

    if chuva:
        print(" 🌧️  CHUVA PREVISTA!")
        print(" ❌ Irrigação SUSPENSA para economizar água")
        nivel_chuva = 1
    elif umidade > 80:
        print(" 🌥️  Alta umidade no ar")
        print(" ⚠️  Irrigação REDUZIDA")
        nivel_chuva = 0
    else:
        print(" ☀️  Sem chuva prevista")
        print(" ✅ Irrigação LIBERADA")
        nivel_chuva = 0

    print("====================================")

    with open("resultado_clima.txt", "w") as f:
        f.write(str(nivel_chuva))

    print(f"\n Resultado salvo em 'resultado_clima.txt'")
    print(f" Valor: {nivel_chuva} (1 = tem chuva, 0 = sem chuva)")


# ========== EXECUTA ==========
if __name__ == "__main__":
    dados = buscar_clima()
    analisar_irrigacao(dados)