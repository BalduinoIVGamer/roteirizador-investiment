import os
import base64
from io import BytesIO

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(
    page_title="Roteirizador de Investimentos",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# Idiomas (menus e labels)
# -----------------------------
IDIOMAS = {
    "Português": {
        "menu": [
            "Simulação de Investimentos",
            "Comparação de Estratégias",
            "Relatório em PDF",
            "Carteira Simulada",
            "Ranking de Investimentos",
            "Indicador de Risco",
            "Controle de Gastos",
            "Notícias do Mercado",
            "Cripto 2026",
            "Calculadora Virtual"
        ],
        "login_title": "🔐 Login - Roteirizador de Investimentos",
        "username": "Usuário",
        "password": "Senha",
        "enter": "Entrar",
        "logout": "Sair",
        "welcome": "📊 Roteirizador de Investimentos",
        "logged_ok": "✅ Logado com sucesso!",
        "bad_creds": "Usuário ou senha inválidos.",
        "need_login": "Faça login para continuar.",
        "currency": "💱 Moeda",
        "lang": "🌍 Language / Idioma",
        "calc_title": "🧮 Calculadora Virtual",
        "calc_op": "Escolha a operação:",
        "calc_n1": "Digite o primeiro número:",
        "calc_n2": "Digite o segundo número:",
        "calc_btn": "Calcular",
        "calc_add": "Adição (+)",
        "calc_sub": "Subtração (-)",
        "calc_pct": "Porcentagem (%)",
        "result": "Resultado",
        "expenses_title": "📑 Controle de Gastos Mensais",
        "download_template": "📥 Baixar modelo Excel",
        "upload_prompt": "📤 Envie sua planilha preenchida (Excel)",
        "your_spends": "📊 Seus Registros",
        "total_income": "TOTAL DE RECEITAS",
        "total_expense": "TOTAL DE DESPESAS",
        "final_balance": "SALDO FINAL",
        "needs_cols": "⚠️ A planilha deve conter as colunas: 'Dia', 'Descrição', 'Categoria', 'Tipo (Receita/Despesa)', 'Valor (R$)'.",
        "pie_title": "Distribuição por Categoria (apenas Despesas)",
        "news_title": "📰 Notícias do Mercado",
        "crypto_title": "🚀 Criptomoedas Promissoras 2026",
        "sim_title": "📈 Simulação de Investimentos",
        "sim_amount": "Valor inicial (R$):",
        "sim_rate": "Taxa anual (%):",
        "sim_years": "Período (anos):",
        "sim_run": "Simular",
        "sim_final": "Montante final",
        "compare_title": "⚖️ Comparação de Estratégias (exemplo)",
        "report_title": "📑 Relatório (em breve)",
        "wallet_title": "💼 Carteira Simulada (em breve)",
        "ranking_title": "⭐ Ranking de Investimentos (exemplo)",
        "risk_title": "⚠️ Indicador de Risco (exemplo)"
    },
    "English": {
        "menu": [
            "Investment Simulation",
            "Strategy Comparison",
            "PDF Report",
            "Simulated Portfolio",
            "Investment Ranking",
            "Risk Indicator",
            "Expense Tracker",
            "Market News",
            "Crypto 2026",
            "Virtual Calculator"
        ],
        "login_title": "🔐 Login - Investment Router",
        "username": "Username",
        "password": "Password",
        "enter": "Sign in",
        "logout": "Log out",
        "welcome": "📊 Investment Router",
        "logged_ok": "✅ Logged in!",
        "bad_creds": "Invalid credentials.",
        "need_login": "Please login to continue.",
        "currency": "💱 Currency",
        "lang": "🌍 Language",
        "calc_title": "🧮 Virtual Calculator",
        "calc_op": "Choose the operation:",
        "calc_n1": "Enter the first number:",
        "calc_n2": "Enter the second number:",
        "calc_btn": "Calculate",
        "calc_add": "Addition (+)",
        "calc_sub": "Subtraction (-)",
        "calc_pct": "Percentage (%)",
        "result": "Result",
        "expenses_title": "📑 Monthly Expense Tracker",
        "download_template": "📥 Download Excel Template",
        "upload_prompt": "📤 Upload your filled spreadsheet (Excel)",
        "your_spends": "📊 Your Records",
        "total_income": "TOTAL INCOME",
        "total_expense": "TOTAL EXPENSES",
        "final_balance": "FINAL BALANCE",
        "needs_cols": "⚠️ Sheet must contain: 'Dia', 'Descrição', 'Categoria', 'Tipo (Receita/Despesa)', 'Valor (R$)'.",
        "pie_title": "Category Distribution (Expenses only)",
        "news_title": "📰 Market News",
        "crypto_title": "🚀 Promising Cryptocurrencies 2026",
        "sim_title": "📈 Investment Simulation",
        "sim_amount": "Initial amount (R$):",
        "sim_rate": "Annual rate (%):",
        "sim_years": "Period (years):",
        "sim_run": "Simulate",
        "sim_final": "Final amount",
        "compare_title": "⚖️ Strategy Comparison (sample)",
        "report_title": "📑 Report (coming soon)",
        "wallet_title": "💼 Simulated Portfolio (coming soon)",
        "ranking_title": "⭐ Investment Ranking (sample)",
        "risk_title": "⚠️ Risk Indicator (sample)"
    },
    "Español": {
        "menu": [
            "Simulación de Inversiones",
            "Comparación de Estrategias",
            "Informe PDF",
            "Cartera Simulada",
            "Ranking de Inversiones",
            "Indicador de Riesgo",
            "Control de Gastos",
            "Noticias del Mercado",
            "Cripto 2026",
            "Calculadora Virtual"
        ],
        "login_title": "🔐 Login - Enrutador de Inversiones",
        "username": "Usuario",
        "password": "Contraseña",
        "enter": "Entrar",
        "logout": "Salir",
        "welcome": "📊 Enrutador de Inversiones",
        "logged_ok": "✅ ¡Sesión iniciada!",
        "bad_creds": "Credenciales inválidas.",
        "need_login": "Inicia sesión para continuar.",
        "currency": "💱 Moneda",
        "lang": "🌍 Idioma",
        "calc_title": "🧮 Calculadora Virtual",
        "calc_op": "Elige la operación:",
        "calc_n1": "Ingresa el primer número:",
        "calc_n2": "Ingresa el segundo número:",
        "calc_btn": "Calcular",
        "calc_add": "Suma (+)",
        "calc_sub": "Resta (-)",
        "calc_pct": "Porcentaje (%)",
        "result": "Resultado",
        "expenses_title": "📑 Control de Gastos Mensuales",
        "download_template": "📥 Descargar Plantilla Excel",
        "upload_prompt": "📤 Sube tu planilla (Excel)",
        "your_spends": "📊 Tus Registros",
        "total_income": "TOTAL INGRESOS",
        "total_expense": "TOTAL GASTOS",
        "final_balance": "SALDO FINAL",
        "needs_cols": "⚠️ La planilla debe contener: 'Dia', 'Descrição', 'Categoria', 'Tipo (Receita/Despesa)', 'Valor (R$)'.",
        "pie_title": "Distribución por Categoría (solo Gastos)",
        "news_title": "📰 Noticias del Mercado",
        "crypto_title": "🚀 Criptomonedas Prometedoras 2026",
        "sim_title": "📈 Simulación de Inversiones",
        "sim_amount": "Monto inicial (R$):",
        "sim_rate": "Tasa anual (%):",
        "sim_years": "Periodo (años):",
        "sim_run": "Simular",
        "sim_final": "Monto final",
        "compare_title": "⚖️ Comparación de Estrategias (ejemplo)",
        "report_title": "📑 Informe (próximamente)",
        "wallet_title": "💼 Cartera Simulada (próximamente)",
        "ranking_title": "⭐ Ranking de Inversiones (ejemplo)",
        "risk_title": "⚠️ Indicador de Riesgo (ejemplo)"
    }
}

# -----------------------------
# Sidebar: idioma e moeda
# -----------------------------
st.sidebar.title("⚙️ Configurações / Settings")
idioma = st.sidebar.selectbox("🌍 Language / Idioma", list(IDIOMAS.keys()))
T = IDIOMAS[idioma]

moeda = st.sidebar.selectbox(
    T["currency"],
    ["BRL - Real", "USD - Dólar", "EUR - Euro", "GBP - Libra", "ARS - Peso Argentino"]
)

# taxas simples (1 BRL -> moeda-alvo)
TAXAS = {
    "BRL - Real": 1.0,
    "USD - Dólar": 0.20,
    "EUR - Euro": 0.18,
    "GBP - Libra": 0.15,
    "ARS - Peso Argentino": 190.0
}

def convert_brl(value_brl: float) -> float:
    return float(value_brl) * TAXAS.get(moeda, 1.0)

def fmt_money_brl_and_sel(value_brl: float) -> str:
    return f"R$ {value_brl:,.2f}  ≈  {convert_brl(value_brl):,.2f} {moeda}"

# -----------------------------
# LOGIN (simples em memória)
# -----------------------------
USERS = {
    "admin": "1234",
    "user": "abcd"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def do_login():
    st.title(T["login_title"])
    u = st.text_input(T["username"])
    p = st.text_input(T["password"], type="password")
    if st.button(T["enter"]):
        if u in USERS and USERS[u] == p:
            st.session_state.logged_in = True
            st.success(T["logged_ok"])
            st.experimental_rerun()
        else:
            st.error(T["bad_creds"])

def logout():
    st.session_state.logged_in = False
    st.experimental_rerun()

if not st.session_state.logged_in:
    do_login()
    st.stop()

st.sidebar.success(T["logged_ok"])
st.sidebar.button(T["logout"], on_click=logout)

# -----------------------------
# Funções das abas
# -----------------------------
def simulacao_investimentos():
    st.header(T["sim_title"])
    valor = st.number_input(T["sim_amount"], min_value=0.0, step=100.0)
    taxa = st.number_input(T["sim_rate"], min_value=0.0, step=0.5)
    anos = st.slider(T["sim_years"], 1, 40, 10)
    if st.button(T["sim_run"]):
        montante = valor * ((1 + taxa/100.0) ** anos)
        st.success(f"{T['sim_final']}: {fmt_money_brl_and_sel(montante)}")
        # gráfico simples de evolução anual
        anos_eixo = list(range(anos + 1))
        valores = [valor * ((1 + taxa/100.0) ** a) for a in anos_eixo]
        fig, ax = plt.subplots()
        ax.plot(anos_eixo, valores)
        ax.set_xlabel("Anos")
        ax.set_ylabel("Valor (R$)")
        st.pyplot(fig)

def comparacao_estrategias():
    st.header(T["compare_title"])
    col1, col2 = st.columns(2)
    with col1:
        taxa1 = st.number_input("Taxa anual Estrat. 1 (%)", value=8.0)
    with col2:
        taxa2 = st.number_input("Taxa anual Estrat. 2 (%)", value=12.0)
    anos = st.slider("Período (anos)", 1, 40, 15)
    valor_inicial = st.number_input("Valor inicial (R$)", value=1000.0, step=100.0)

    def sim(t):
        return valor_inicial * ((1 + t/100.0) ** anos)

    if st.button("Comparar"):
        v1 = sim(taxa1)
        v2 = sim(taxa2)
        st.info(f"Estratégia 1: {fmt_money_brl_and_sel(v1)}")
        st.info(f"Estratégia 2: {fmt_money_brl_and_sel(v2)}")

def relatorio_pdf():
    st.header(T["report_title"])
    st.write("Gere seus relatórios profissionais com os resultados do app (em breve).")

def carteira_simulada():
    st.header(T["wallet_title"])
    st.write("Monte sua alocação alvo e acompanhe (em breve).")

def ranking_investimentos():
    st.header(T["ranking_title"])
    dados = {
        "Investimento": ["Tesouro Selic", "CDB", "Ações", "FIIs"],
        "Rentabilidade (%) ao ano": [9.0, 11.0, 18.0, 12.0]
    }
    df = pd.DataFrame(dados).sort_values("Rentabilidade (%) ao ano", ascending=False)
    st.table(df)

def indicador_risco():
    st.header(T["risk_title"])
    perfil = st.radio("Perfil:", ["Conservador", "Moderado", "Agressivo"])
    if perfil == "Conservador":
        st.info("Sugestão: 80% Renda Fixa, 15% Fundos, 5% Ações")
    elif perfil == "Moderado":
        st.info("Sugestão: 50% Renda Fixa, 30% Fundos, 20% Ações")
    else:
        st.info("Sugestão: 20% Renda Fixa, 30% Fundos, 50% Ações")

def gerar_template_excel_bytes() -> bytes:
    """Gera um arquivo Excel de modelo (30 dias, colunas e linhas vazias + área de totais)"""
    dias = list(range(1, 31))
    df = pd.DataFrame({
        "Dia": dias,
        "Descrição": ["" for _ in dias],
        "Categoria": ["" for _ in dias],
        "Tipo (Receita/Despesa)": ["" for _ in dias],
        "Valor (R$)": ["" for _ in dias],
    })
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Controle Financeiro")
        # adiciona linhas extras de totais
        sht = writer.sheets["Controle Financeiro"]
        base = len(df) + 2  # linha após os dados + 1
        sht.cell(row=base + 0, column=1, value=T["total_income"])
        sht.cell(row=base + 1, column=1, value=T["total_expense"])
        sht.cell(row=base + 2, column=1, value=T["final_balance"])
    buffer.seek(0)
    return buffer.getvalue()

def controle_gastos():
    st.header(T["expenses_title"])

    # Download do modelo
    st.subheader(T["download_template"])
    file_name = "controle_gastos_mensal.xlsx"
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data_bytes = f.read()
    else:
        data_bytes = gerar_template_excel_bytes()

    b64 = base64.b64encode(data_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">{T["download_template"]}</a>'
    st.markdown(href, unsafe_allow_html=True)

    st.write("---")

    # Upload
    uploaded = st.file_uploader(T["upload_prompt"], type=["xlsx"])
    if uploaded is not None:
        try:
            df = pd.read_excel(uploaded)
        except Exception as e:
            st.error(f"Erro ao ler o Excel: {e}")
            return

        cols_needed = ["Dia", "Descrição", "Categoria", "Tipo (Receita/Despesa)", "Valor (R$)"]
        if not all(c in df.columns for c in cols_needed):
            st.warning(T["needs_cols"])
            st.dataframe(df)
            return

        # Normaliza a coluna de valor para numérico
        df["Valor (R$)"] = pd.to_numeric(df["Valor (R$)"], errors="coerce").fillna(0.0)

        st.subheader(T["your_spends"])
        st.dataframe(df, use_container_width=True)

        # Totais
        total_receitas = df.loc[df["Tipo (Receita/Despesa)"].str.lower() == "receita", "Valor (R$)"].sum()
        total_despesas = df.loc[df["Tipo (Receita/Despesa)"].str.lower() == "despesa", "Valor (R$)"].sum()
        saldo = total_receitas - total_despesas

        st.success(f"💚 {T['total_income']}: {fmt_money_brl_and_sel(total_receitas)}")
        st.error(f"❤️ {T['total_expense']}: {fmt_money_brl_and_sel(total_despesas)}")
        st.info(f"🟨 {T['final_balance']}: {fmt_money_brl_and_sel(saldo)}")

        # Gráfico (apenas despesas, por categoria)
        despesas = df[df["Tipo (Receita/Despesa)"].str.lower() == "despesa"]
        if not despesas.empty:
            by_cat = despesas.groupby("Categoria")["Valor (R$)"].sum().reset_index()
            fig, ax = plt.subplots()
            ax.pie(by_cat["Valor (R$)"], labels=by_cat["Categoria"], autopct="%1.1f%%")
            ax.set_title(T["pie_title"])
            st.pyplot(fig)

def noticias_mercado():
    st.header(T["news_title"])
    st.markdown("- **Bolsas Globais** — Destaques diários de S&P 500, Nasdaq, Europa e Ásia.")
    st.markdown("- **Criptomoedas** — Principais movimentos de BTC, ETH e altcoins.")
    st.markdown("- **Juros & Inflação** — Decisões de bancos centrais e indicadores.")
    st.write("Links úteis (exemplos):")
    st.markdown("- Reuters – Mercados")
    st.markdown("- Bloomberg – Markets")
    st.markdown("- CoinDesk – Crypto News")

def cripto_2026():
    st.header(T["crypto_title"])
    st.write("**BTC** — Adoção institucional e ETFs amadurecendo o mercado.")
    st.write("**ETH** — Ecossistema DeFi/NFT sólido e atualização contínua.")
    st.write("**SOL** — Alta performance e ecossistema vibrante.")
    st.write("**LINK** — Oráculos essenciais para contratos inteligentes (DeFi/TradFi).")
    st.write("**MATIC/Polygon** — Escalonamento e integrações enterprise.")

def calculadora_virtual():
    st.header(T["calc_title"])
    n1 = st.number_input(T["calc_n1"], step=1.0, format="%.2f")
    op = st.selectbox(T["calc_op"], [T["calc_add"], T["calc_sub"], T["calc_pct"]])
    n2 = st.number_input(T["calc_n2"], step=1.0, format="%.2f")
    if st.button(T["calc_btn"]):
        if op == T["calc_add"]:
            res = n1 + n2
        elif op == T["calc_sub"]:
            res = n1 - n2
        else:  # porcentagem
            res = (n1 * n2) / 100.0
        st.success(f"{T['result']}: {fmt_money_brl_and_sel(res)}")

# -----------------------------
# Menu e roteamento
# -----------------------------
menu = st.sidebar.radio("📌 Menu", T["menu"])

if menu == T["menu"][0]:
    simulacao_investimentos()
elif menu == T["menu"][1]:
    comparacao_estrategias()
elif menu == T["menu"][2]:
    relatorio_pdf()
elif menu == T["menu"][3]:
    carteira_simulada()
elif menu == T["menu"][4]:
    ranking_investimentos()
elif menu == T["menu"][5]:
    indicador_risco()
elif menu == T["menu"][6]:
    controle_gastos()
elif menu == T["menu"][7]:
    noticias_mercado()
elif menu == T["menu"][8]:
    cripto_2026()
elif menu == T["menu"][9]:
    calculadora_virtual()

