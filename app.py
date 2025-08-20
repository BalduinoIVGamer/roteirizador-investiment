import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# --- Configuração de idiomas ---
idiomas = {
    "Português": {
        "menu": ["Simulação de Investimentos", "Comparação de Estratégias", "Relatório em PDF",
                 "Carteira Simulada", "Ranking de Investimentos", "Indicador de Risco",
                 "Controle de Gastos", "Notícias do Mercado", "Cripto 2026", "Calculadora Virtual"],
        "calculadora": "Calculadora Virtual",
        "controle_gastos": "Controle de Gastos Mensais",
        "download_planilha": "📥 Baixar Planilha Modelo"
    },
    "English": {
        "menu": ["Investment Simulation", "Strategy Comparison", "PDF Report",
                 "Simulated Portfolio", "Investment Ranking", "Risk Indicator",
                 "Expense Tracker", "Market News", "Crypto 2026", "Virtual Calculator"],
        "calculadora": "Virtual Calculator",
        "controle_gastos": "Monthly Expense Tracker",
        "download_planilha": "📥 Download Template Spreadsheet"
    },
    "Español": {
        "menu": ["Simulación de Inversiones", "Comparación de Estrategias", "Informe PDF",
                 "Cartera Simulada", "Ranking de Inversiones", "Indicador de Riesgo",
                 "Control de Gastos", "Noticias del Mercado", "Cripto 2026", "Calculadora Virtual"],
        "calculadora": "Calculadora Virtual",
        "controle_gastos": "Control de Gastos Mensuales",
        "download_planilha": "📥 Descargar Planilla Modelo"
    }
}

# --- Sidebar: idioma e moeda ---
st.sidebar.title("⚙️ Configurações")
idioma_escolhido = st.sidebar.selectbox("🌍 Language / Idioma", ["Português", "English", "Español"])
textos = idiomas[idioma_escolhido]

moeda = st.sidebar.selectbox("💱 Moeda", ["BRL - Real", "USD - Dólar", "EUR - Euro", "GBP - Libra", "ARS - Peso Argentino"])
taxas = {"BRL - Real": 1.0, "USD - Dólar": 0.20, "EUR - Euro": 0.18, "GBP - Libra": 0.15, "ARS - Peso Argentino": 190.0}

# --- Menu ---
menu = st.sidebar.radio("📌 Navegação", textos["menu"])

# --- Funções ---

# Simulação de Investimentos
def simulacao_investimentos():
    st.header("📈 Simulação de Investimentos")
    valor = st.number_input("Digite o valor inicial (em R$):", min_value=0.0, step=100.0)
    taxa = st.number_input("Taxa de retorno anual (%):", min_value=0.0, step=0.5)
    anos = st.slider("Período (anos):", 1, 30, 10)
    if st.button("Simular"):
        montante = valor * ((1 + taxa/100) ** anos)
        convertido = montante * taxas[moeda]
        st.success(f"Montante final: {montante:,.2f} R$ ≈ {convertido:,.2f} {moeda}")

# Comparação de Estratégias
def comparacao_estrategias():
    st.header("📊 Comparação de Estratégias")
    st.write("🚀 Em breve: comparação entre renda fixa, bolsa e criptos.")

# Relatório em PDF
def relatorio_pdf():
    st.header("📑 Relatório em PDF")
    st.write("⚙️ Em breve: exportação automática dos resultados.")

# Carteira Simulada
def carteira_simulada():
    st.header("💼 Carteira Simulada")
    st.write("⚙️ Em breve: adição de ativos simulados.")

# Ranking de Investimentos
def ranking_investimentos():
    st.header("🏆 Ranking de Investimentos")
    st.write("⚙️ Em breve: lista de melhores opções de investimento.")

# Indicador de Risco
def indicador_risco():
    st.header("⚠️ Indicador de Risco")
    st.write("⚙️ Em breve: análise de risco automático.")

# Controle de Gastos
def controle_gastos():
    st.header(textos["controle_gastos"])

    st.subheader("📥 Upload da Planilha")
    arquivo = st.file_uploader("Envie sua planilha de gastos (Excel)", type=["xlsx"])

    # Botão para baixar planilha modelo
    with open("controle_gastos_modelo.xlsx", "rb") as f:
        st.download_button(label=textos["download_planilha"], data=f, file_name="controle_gastos_modelo.xlsx")

    if arquivo:
        df = pd.read_excel(arquivo)
        st.subheader("📊 Seus Gastos")
        st.dataframe(df)

        resumo = df.groupby("Categoria")["Valor (R$)"].sum().reset_index()
        resumo["Valor Convertido"] = resumo["Valor (R$)"] * taxas[moeda]
        resumo["Moeda"] = moeda
        st.dataframe(resumo)

        # Gráfico
        fig, ax = plt.subplots()
        ax.pie(resumo["Valor (R$)"], labels=resumo["Categoria"], autopct="%1.1f%%")
        st.pyplot(fig)

# Notícias
def noticias_mercado():
    st.header("📰 Notícias do Mercado")
    try:
        url = "https://cryptopanic.com/api/v1/posts/?auth_token=demo&public=true"
        resp = requests.get(url).json()
        for n in resp.get("results", [])[:5]:
            st.subheader(n["title"])
            st.write(f"🔗 [Ler mais]({n['url']})")
    except:
        st.warning("⚠️ Não foi possível carregar notícias agora.")

# Criptos 2026
def cripto_2026():
    st.header("🚀 Criptomoedas Promissoras 2026")
    st.write("""
    🔹 **Bitcoin (BTC)** – Reserva de valor consolidada  
    🔹 **Ethereum (ETH)** – Ecossistema DeFi/NFT  
    🔹 **Solana (SOL)** – Escalabilidade alta  
    🔹 **Polygon (MATIC)** – Solução de segunda camada  
    🔹 **Chainlink (LINK)** – Oráculos para smart contracts  
    """)

# Calculadora
def calculadora_virtual():
    st.header("🧮 " + textos["calculadora"])
    num1 = st.number_input("Digite o primeiro número:", step=1.0, format="%.2f")
    operacao = st.selectbox("Escolha a operação:", ["Adição (+)", "Subtração (-)", "Porcentagem (%)"])
    num2 = st.number_input("Digite o segundo número:", step=1.0, format="%.2f")
    if st.button("Calcular"):
        if operacao == "Adição (+)":
            resultado = num1 + num2
        elif operacao == "Subtração (-)":
            resultado = num1 - num2
        else:
            resultado = (num1 * num2) / 100
        convertido = resultado * taxas[moeda]
        st.success(f"Resultado: {resultado:.2f} R$ ≈ {convertido:.2f} {moeda}")

# --- Roteamento ---
if menu == textos["menu"][0]:
    simulacao_investimentos()
elif menu == textos["menu"][1]:
    comparacao_estrategias()
elif menu == textos["menu"][2]:
    relatorio_pdf()
elif menu == textos["menu"][3]:
    carteira_simulada()
elif menu == textos["menu"][4]:
    ranking_investimentos()
elif menu == textos["menu"][5]:
    indicador_risco()
elif menu == textos["menu"][6]:
    controle_gastos()
elif menu == textos["menu"][7]:
    noticias_mercado()
elif menu == textos["menu"][8]:
    cripto_2026()
elif menu == textos["menu"][9]:
    calculadora_virtual()


