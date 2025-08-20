import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Configuração inicial da página
st.set_page_config(
    page_title="Roteirizador de Investimentos",
    page_icon="💰",
    layout="wide"
)

# --- Funções ---

# Controle de Gastos
def controle_gastos():
    st.header("📊 Controle de Gastos Mensais")

    # Upload de planilha
    arquivo = st.file_uploader("Faça upload da sua planilha de gastos (Excel)", type=["xlsx"])
    
    if arquivo is not None:
        df = pd.read_excel(arquivo)
        st.subheader("📋 Visualização da planilha")
        st.dataframe(df)

        # Resumo por categoria
        if "Categoria" in df.columns and "Valor (R$)" in df.columns:
            resumo = df.groupby("Categoria")["Valor (R$)"].sum().reset_index()

            st.subheader("📊 Resumo por categoria")
            st.dataframe(resumo)

            # Gráfico
            fig, ax = plt.subplots()
            ax.pie(resumo["Valor (R$)"], labels=resumo["Categoria"], autopct="%1.1f%%")
            ax.set_title("Distribuição de Gastos por Categoria")
            st.pyplot(fig)
        else:
            st.warning("⚠️ A planilha deve conter as colunas 'Categoria' e 'Valor (R$)'.")

    # Download da planilha modelo
    st.subheader("📥 Baixar planilha modelo")
    dados_exemplo = {
        "Data": ["01/08/2025", "03/08/2025", "05/08/2025"],
        "Categoria": ["Alimentação", "Transporte", "Moradia"],
        "Descrição": ["Supermercado", "Uber", "Aluguel"],
        "Valor (R$)": [350, 45, 1200]
    }
    df_exemplo = pd.DataFrame(dados_exemplo)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_exemplo.to_excel(writer, index=False, sheet_name="Gastos Mensais")

    st.download_button(
        label="📥 Clique aqui para baixar o modelo de planilha",
        data=buffer,
        file_name="controle_gastos_modelo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# Notícias sobre Cripto 2026
def noticias_cripto2026():
    st.header("🚀 Criptomoedas Promissoras em 2026")

    st.subheader("Bitcoin (BTC)")
    st.write("Poderia alcançar **US$150.000 até o final de 2026**, impulsionado pelos ETFs e adoção institucional contínua.")
    st.markdown("[Fonte – Business Upturn](https://www.businessupturn.com/finance/cryptocurrency/cryptocurrencies-expected-to-boom-in-price-in-2026/)")

    st.subheader("Chainlink (LINK)")
    st.write("Com o protocolo CCIP e uso crescente em DeFi/IA, pode chegar a **US$100–120 em 2026**.")
    st.markdown("[Fonte – Business Upturn](https://www.businessupturn.com/finance/cryptocurrency/cryptocurrencies-expected-to-boom-in-price-in-2026/)")

    st.subheader("XRP (Ripple)")
    st.write("Com avanços regulatórios e adoção em remessas internacionais, pode atingir **US$2,50–3,00** até 2026.")
    st.markdown("[Fonte – Business Upturn](https://www.businessupturn.com/finance/cryptocurrency/cryptocurrencies-expected-to-boom-in-price-in-2026/)")

    st.subheader("Sui (SUI) e Solana (SOL)")
    st.write("- **SUI**: design ultra-eficiente e rápido, com potencial de destaque em pagamentos on-chain.\n"
             "- **Solana**: forte ecossistema de NFTs/DeFi e altíssima performance técnica.")
    st.markdown("[Fonte – CryptoNews](https://cryptonews.com/news/grok-picks-top-4-altcoins-to-10x-before-2026-xrp-sol-sui/)")


# --- Menu lateral ---
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
        "Notícias do Mercado",
        "Cripto 2026"
    ]
)

# --- Rotas ---
if menu == "Controle de Gastos":
    controle_gastos()

elif menu == "Cripto 2026":
    noticias_cripto2026()

else:
    st.write("🚧 Essa seção ainda está em desenvolvimento.")

