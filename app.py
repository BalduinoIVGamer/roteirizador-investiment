import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import datetime

# ---------------------------
# LOGIN SIMPLES
# ---------------------------
def check_login(username, password):
    return username == "usuario" and password == "senha123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")
    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if check_login(user, pwd):
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()

# ---------------------------
# MENU LATERAL
# ---------------------------
st.sidebar.title("📊 Menu")
opcao = st.sidebar.radio("Escolha uma opção", [
    "🏦 Roteirizador de Investimentos",
    "📑 Controle de Gastos",
    "🧮 Calculadora",
    "💱 Conversor de Moedas",
    "🌍 Idiomas",
    "📰 Notícias Financeiras",
    "🚀 Criptomoedas 2026"
])

# ---------------------------
# ROTEIRIZADOR DE INVESTIMENTOS
# ---------------------------
if opcao == "🏦 Roteirizador de Investimentos":
    st.title("🏦 Roteirizador de Investimentos")
    valor = st.number_input("💰 Valor para investir (R$)", min_value=0.0, step=100.0)
    prazo = st.slider("Prazo do investimento (anos)", 1, 30, 5)
    risco = st.selectbox("Perfil de risco", ["Conservador", "Moderado", "Agressivo"])

    if st.button("Gerar Roteiro"):
        if risco == "Conservador":
            carteira = {"Tesouro Selic": 0.7, "CDB Bancos Grandes": 0.3}
        elif risco == "Moderado":
            carteira = {"Tesouro IPCA+": 0.4, "Fundos Multimercado": 0.4, "Ações Blue Chips": 0.2}
        else:
            carteira = {"Criptomoedas": 0.3, "Ações Tech": 0.4, "ETFs Internacionais": 0.3}

        st.subheader("📌 Sugestão de Carteira")
        df = pd.DataFrame({
            "Ativo": carteira.keys(),
            "Alocação (%)": [f"{p*100:.0f}%" for p in carteira.values()],
            "Valor Estimado (R$)": [valor * p for p in carteira.values()]
        })
        st.table(df)

# ---------------------------
# CONTROLE DE GASTOS
# ---------------------------
elif opcao == "📑 Controle de Gastos":
    st.title("📑 Controle de Gastos Mensais")

    st.write("📥 Baixe a planilha modelo para preencher seus gastos:")
    with open("controle_gastos_mensal.xlsx", "rb") as f:
        st.download_button("📊 Baixar Planilha Modelo", f, file_name="controle_gastos_mensal.xlsx")

    st.write("📤 Envie sua planilha preenchida para análise:")
    uploaded = st.file_uploader("Enviar planilha (.xlsx)", type=["xlsx"])
    if uploaded:
        df = pd.read_excel(uploaded)
        st.dataframe(df)

        # Cálculo de totais
        total_receitas = df[df["Tipo"] == "Receita"]["Valor (R$)"].sum()
        total_despesas = df[df["Tipo"] == "Despesa"]["Valor (R$)"].sum()
        saldo = total_receitas - total_despesas

        st.success(f"💵 Receitas: R$ {total_receitas:,.2f}")
        st.error(f"📉 Despesas: R$ {total_despesas:,.2f}")
        st.info(f"📊 Saldo Final: R$ {saldo:,.2f}")

# ---------------------------
# CALCULADORA
# ---------------------------
elif opcao == "🧮 Calculadora":
    st.title("🧮 Calculadora Simples")

    num1 = st.number_input("Primeiro número", value=0.0)
    operacao = st.selectbox("Operação", ["+", "-", "%"])
    num2 = st.number_input("Segundo número", value=0.0)

    if st.button("Calcular"):
        if operacao == "+":
            resultado = num1 + num2
        elif operacao == "-":
            resultado = num1 - num2
        elif operacao == "%":
            resultado = (num1 * num2) / 100
        st.success(f"Resultado: {resultado}")

# ---------------------------
# CONVERSOR DE MOEDAS
# ---------------------------
elif opcao == "💱 Conversor de Moedas":
    st.title("💱 Conversor de Moedas")

    moedas = {"Real (BRL)": "BRL", "Dólar (USD)": "USD", "Euro (EUR)": "EUR", "Libra (GBP)": "GBP", "Peso Argentino (ARS)": "ARS"}
    de = st.selectbox("De:", list(moedas.keys()))
    para = st.selectbox("Para:", list(moedas.keys()))
    valor = st.number_input("Valor", min_value=0.0, step=1.0)

    if st.button("Converter"):
        url = f"https://api.exchangerate.host/convert?from={moedas[de]}&to={moedas[para]}&amount={valor}"
        resp = requests.get(url).json()
        st.success(f"{valor} {moedas[de]} = {resp['result']:.2f} {moedas[para]}")

# ---------------------------
# IDIOMAS
# ---------------------------
elif opcao == "🌍 Idiomas":
    st.title("🌍 Idiomas Disponíveis")
    st.write("🇧🇷 Português")
    st.write("🇺🇸 Inglês")
    st.write("🇪🇸 Espanhol")
    st.info("Traduções podem ser integradas futuramente.")

# ---------------------------
# NOTÍCIAS FINANCEIRAS
# ---------------------------
elif opcao == "📰 Notícias Financeiras":
    st.title("📰 Últimas Notícias do Mercado")

    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        noticias = requests.get(url).json()["Data"][:5]
        for n in noticias:
            st.subheader(n["title"])
            st.write(n["body"][:200] + "...")
            st.markdown(f"[Leia mais]({n['url']})")
    except:
        st.error("Erro ao carregar notícias.")

# ---------------------------
# ANÁLISE CRIPTO 2026
# ---------------------------
elif opcao == "🚀 Criptomoedas 2026":
    st.title("🚀 Criptomoedas Promissoras para 2026")

    analise = {
        "Bitcoin (BTC)": "Maior segurança e reserva de valor.",
        "Ethereum (ETH)": "Liderança em contratos inteligentes e DeFi.",
        "Solana (SOL)": "Alta escalabilidade e baixas taxas.",
        "Polkadot (DOT)": "Interoperabilidade entre blockchains.",
        "Cardano (ADA)": "Foco em sustentabilidade e governança."
    }

    df = pd.DataFrame(list(analise.items()), columns=["Criptomoeda", "Motivo"])
    st.table(df)



