import streamlit as st
import pandas as pd
import requests

# =========================
# CONFIGURAÇÕES INICIAIS
# =========================
st.set_page_config(page_title="Roteirizador de Investimentos", layout="wide")

# --- Credenciais simples ---
USER = "usuario123"
PASSWORD = "senha123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================
# FUNÇÕES
# =========================

def carregar_planilha():
    """Carrega a planilha de gastos mensais"""
    try:
        df = pd.read_excel("gastos_mensais.xlsx")
        return df
    except:
        return pd.DataFrame({"Dia": [], "Receitas": [], "Despesas": []})


def obter_noticias_crypto():
    """Puxa notícias de criptomoedas"""
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=demo&public=true"
    try:
        resp = requests.get(url)
        dados = resp.json()
        noticias = [n["title"] for n in dados["results"][:5]]
        return noticias
    except:
        return ["Notícias indisponíveis no momento."]


def calculadora(operacao, num1, num2):
    """Calculadora simples"""
    if operacao == "Adição":
        return num1 + num2
    elif operacao == "Subtração":
        return num1 - num2
    elif operacao == "Porcentagem":
        return (num1 * num2) / 100
    else:
        return None


# =========================
# LOGIN
# =========================
if not st.session_state.logged_in:
    st.title("🔑 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == USER and senha == PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha inválidos")

# =========================
# APP PRINCIPAL
# =========================
else:
    st.sidebar.title("📌 Menu")
    opcao = st.sidebar.radio("Navegação", ["Início", "Planilha de Gastos", "Notícias", "Criptomoedas 2026", "Calculadora", "Sair"])

    if opcao == "Início":
        st.title("📊 Roteirizador de Investimentos")
        st.write("Bem-vindo ao seu app de finanças e investimentos!")

    elif opcao == "Planilha de Gastos":
        st.title("📑 Controle de Gastos Mensais")
        df = carregar_planilha()
        st.dataframe(df)

    elif opcao == "Notícias":
        st.title("📰 Notícias do Mercado e Criptomoedas")
        noticias = obter_noticias_crypto()
        for n in noticias:
            st.write("- ", n)

    elif opcao == "Criptomoedas 2026":
        st.title("🚀 Criptomoedas mais promissoras para 2026")
        st.write("""
        🔹 Bitcoin (BTC) → Consolidação como reserva de valor.  
        🔹 Ethereum (ETH) → Expansão do ecossistema DeFi.  
        🔹 Solana (SOL) → Alta performance para dApps.  
        🔹 Cardano (ADA) → Expansão em contratos inteligentes.  
        🔹 Polkadot (DOT) → Interoperabilidade entre blockchains.  
        """)

    elif opcao == "Calculadora":
        st.title("🧮 Calculadora Virtual")
        operacao = st.selectbox("Operação", ["Adição", "Subtração", "Porcentagem"])
        num1 = st.number_input("Número 1", value=0.0)
        num2 = st.number_input("Número 2", value=0.0)
        if st.button("Calcular"):
            resultado = calculadora(operacao, num1, num2)
            st.success(f"Resultado: {resultado}")

    elif opcao == "Sair":
        st.session_state.logged_in = False
        st.rerun()

