import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ========================
# LOGIN
# ========================
def autenticar(usuario, senha):
    try:
        df = pd.read_csv("usuarios.csv")
        if ((df["usuario"] == usuario) & (df["senha"] == senha)).any():
            return True
        else:
            return False
    except:
        return False

st.image("banner.png", use_container_width=True)
st.sidebar.title("🔑 Login")
usuario = st.sidebar.text_input("Usuário (e-mail)")
senha = st.sidebar.text_input("Senha", type="password")
login = st.sidebar.button("Entrar")

if not (usuario and senha and login and autenticar(usuario, senha)):
    st.warning("Por favor, faça login para acessar o app.")
    st.stop()

# ========================
# FUNÇÕES DO APP
# ========================

# --- Simulação de Investimentos ---
def simulacao_investimentos():
    st.header("📈 Simulação de Investimentos")

    valor_inicial = st.number_input("💰 Valor inicial investido (R$)", min_value=0.0, value=1000.0, step=100.0)
    aporte_mensal = st.number_input("📥 Aporte mensal (R$)", min_value=0.0, value=200.0, step=50.0)
    taxa = st.number_input("📊 Taxa de juros anual (%)", min_value=0.0, value=10.0, step=0.5) / 100
    anos = st.slider("⏳ Prazo (anos)", 1, 50, 20)

    meses = anos * 12
    taxa_mensal = (1 + taxa) ** (1/12) - 1

    valores = []
    montante = valor_inicial
    for m in range(meses):
        montante = montante * (1 + taxa_mensal) + aporte_mensal
        valores.append(montante)

    st.subheader("💵 Evolução do investimento")
    fig, ax = plt.subplots()
    ax.plot(range(meses), valores)
    ax.set_xlabel("Meses")
    ax.set_ylabel("Valor acumulado (R$)")
    st.pyplot(fig)

    st.success(f"✨ Em {anos} anos você terá aproximadamente **R$ {montante:,.2f}**")

# --- Comparação de Estratégias ---
def comparacao_estrategias():
    st.header("⚖️ Comparação de Estratégias de Investimento")

    col1, col2 = st.columns(2)
    with col1:
        taxa1 = st.number_input("📊 Taxa anual da Estratégia 1 (%)", value=8.0) / 100
    with col2:
        taxa2 = st.number_input("📊 Taxa anual da Estratégia 2 (%)", value=12.0) / 100

    anos = st.slider("⏳ Prazo (anos)", 1, 50, 20)

    meses = anos * 12
    valor_inicial = 1000
    aporte = 200

    def simular(taxa):
        taxa_mensal = (1 + taxa) ** (1/12) - 1
        montante = valor_inicial
        valores = []
        for _ in range(meses):
            montante = montante * (1 + taxa_mensal) + aporte
            valores.append(montante)
        return valores

    v1 = simular(taxa1)
    v2 = simular(taxa2)

    fig, ax = plt.subplots()
    ax.plot(range(meses), v1, label="Estratégia 1")
    ax.plot(range(meses), v2, label="Estratégia 2")
    ax.legend()
    ax.set_xlabel("Meses")
    ax.set_ylabel("Valor acumulado (R$)")
    st.pyplot(fig)

# --- Relatório PDF ---
def relatorio_pdf():
    st.header("🧾 Gerar Relatório em PDF")
    st.info("⚠️ Aqui você pode exportar um relatório. (Implementação completa pode ser adicionada depois)")

# --- Carteira Simulada ---
def carteira_simulada():
    st.header("💼 Carteira Simulada")

    renda_fixa = st.slider("📊 % em Renda Fixa", 0, 100, 50)
    acoes = st.slider("📊 % em Ações", 0, 100 - renda_fixa, 30)
    fundos = 100 - renda_fixa - acoes

    st.write(f"📌 Sua carteira: {renda_fixa}% Renda Fixa, {acoes}% Ações, {fundos}% Fundos")

# --- Ranking de Investimentos ---
def ranking_investimentos():
    st.header("⭐ Ranking de Investimentos")

    dados = {
        "Investimento": ["Tesouro Selic", "CDB", "Ações", "Fundos Imobiliários"],
        "Rentabilidade (%)": [9, 11, 18, 12]
    }
    df = pd.DataFrame(dados).sort_values("Rentabilidade (%)", ascending=False)
    st.table(df)

# --- Indicador de Risco ---
def indicador_risco():
    st.header("⚖️ Indicador de Risco")

    perfil = st.radio("Qual seu perfil de investidor?", ["Conservador", "Moderado", "Agressivo"])

    if perfil == "Conservador":
        st.info("👉 Recomendado: 80% Renda Fixa, 15% Fundos, 5% Ações")
    elif perfil == "Moderado":
        st.info("👉 Recomendado: 50% Renda Fixa, 30% Fundos, 20% Ações")
    else:
        st.info("👉 Recomendado: 20% Renda Fixa, 30% Fundos, 50% Ações")

# --- Controle de Gastos (Excel) ---
def controle_gastos():
    st.header("📊 Controle de Gastos Mensais")

    uploaded_file = st.file_uploader("📂 Envie sua planilha de gastos (Excel)", type=["xlsx", "xls"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        st.subheader("📑 Dados da sua planilha")
        st.dataframe(df)

        if "Categoria" in df.columns and "Valor" in df.columns:
            st.subheader("📊 Gráfico de Gastos por Categoria")
            fig, ax = plt.subplots()
            df.groupby("Categoria")["Valor"].sum().plot(kind="bar", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("⚠️ Sua planilha precisa ter as colunas: 'Categoria' e 'Valor'.")

# --- Notícias do Mercado ---
def noticias_mercado():
    st.header("📰 Notícias do Mercado Financeiro")

    st.subheader("📉 S&P 500 pode recuar até o fim de 2025")
    st.write("O índice S&P 500 deve terminar o ano abaixo dos níveis recorde atuais, com otimismo contido devido a tensões tarifárias.")
    st.markdown("[🔗 Leia mais](https://www.reuters.com/business/sp-500-seen-stalling-ai-rally-meets-tariff-jitters-reuters-poll-2025-08-19/?utm_source=chatgpt.com)")

    st.subheader("🚀 Criptomoedas em alta sustentada até 2027")
    st.write("Especialistas projetam que a fase de crescimento do mercado cripto continuará até 2027, impulsionada por capital institucional.")
    st.markdown("[🔗 Leia mais](https://news.bitcoin.com/analysts-see-multi-year-crypto-bull-market-as-institutional-floodgates-swing-open/?utm_source=chatgpt.com)")

    st.subheader("💴 China avalia stablecoins lastreadas em yuan")
    st.write("O país discute a implementação de stablecoins lastreadas em yuan para ampliar o uso global de sua moeda.")
    st.markdown("[🔗 Leia mais](https://www.reuters.com/business/finance/china-considering-yuan-backed-stablecoins-boost-global-currency-usage-sources-2025-08-20/?utm_source=chatgpt.com)")

# ========================
# MENU DE NAVEGAÇÃO
# ========================
menu = st.sidebar.radio(
    "📌 Navegação",
    [
        "Simulação de Investimentos",
        "Comparação de Estratégias",
        "Relatório em PDF",
        "Carteira Simulada",
        "Ranking de Investimentos",
        "Indicador de Risco",
        "Controle de Gastos",
        "Notícias do Mercado"
    ]
)

if menu == "Simulação de Investimentos":
    simulacao_investimentos()
elif menu == "Comparação de Estratégias":
    comparacao_estrategias()
elif menu == "Relatório em PDF":
    relatorio_pdf()
elif menu == "Carteira Simulada":
    carteira_simulada()
elif menu == "Ranking de Investimentos":
    ranking_investimentos()
elif menu == "Indicador de Risco":
    indicador_risco()
elif menu == "Controle de Gastos":
    controle_gastos()
elif menu == "Notícias do Mercado":
    noticias_mercado()



