import streamlit as st
import matplotlib.pyplot as plt

# Mostrar banner do produto
st.image("banner.png", use_column_width=True)

# =========================================================
# 🔹 Configurações da página
# =========================================================
st.set_page_config(
    page_title="Roteirizador de Investimentos",
    page_icon="💹",
    layout="centered",
)

# =========================================================
# 🔹 Estilo customizado (CSS aplicado no Streamlit)
# =========================================================
st.markdown("""
    <style>
        .main {
            background-color: #f9fafb;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 🔹 Logo + Cabeçalho
# =========================================================
st.image("https://i.ibb.co/zGbYrM2/logo.png", width=200)  # substitua pelo seu logo
st.title("💹 Roteirizador de Investimentos")
st.markdown("### Sua rota inteligente para multiplicar patrimônio 🚀")

# =========================================================
# 🔹 Abas de Navegação
# =========================================================
aba1, aba2 = st.tabs(["📊 Simulação única", "📈 Comparação de cenários"])

# ---------------------------------------------------------
# 📊 Simulação única
# ---------------------------------------------------------
with aba1:
    st.subheader("Simulação de um investimento")

    valor_inicial = st.number_input("Valor inicial (R$)", min_value=1000, value=5000, step=500)
    aporte_mensal = st.number_input("Aporte mensal (R$)", min_value=0, value=500, step=100)
    taxa = st.number_input("Rentabilidade anual (%)", min_value=1.0, value=8.0, step=0.5)
    anos = st.slider("Período (anos)", 1, 30, 10)

    # Cálculo da evolução
    valores = [valor_inicial]
    for i in range(anos):
        valor_futuro = valores[-1] * (1 + taxa/100) + (aporte_mensal * 12)
        valores.append(valor_futuro)

    plt.style.use("seaborn-v0_8")
    plt.figure(figsize=(7,4))
    plt.plot(range(anos+1), valores, marker="o", label="Simulação")
    plt.title("Evolução do Investimento")
    plt.xlabel("Ano")
    plt.ylabel("Valor acumulado (R$)")
    plt.legend()
    st.pyplot(plt)

# ---------------------------------------------------------
# 📈 Comparação de cenários
# ---------------------------------------------------------
with aba2:
    st.subheader("Comparação entre diferentes estratégias")

    valor_inicial = 5000
    anos = 10

    # Três cenários com taxas diferentes
    taxas = {
        "Tesouro Selic (6% a.a.)": 6,
        "Renda Fixa (8% a.a.)": 8,
        "Bolsa (12% a.a.)": 12
    }

    resultados = {}
    for nome, taxa in taxas.items():
        valores = [valor_inicial]
        for i in range(anos):
            valores.append(valores[-1] * (1 + taxa/100))
        resultados[nome] = valores

    plt.style.use("seaborn-v0_8")
    plt.figure(figsize=(7,4))
    for nome, valores in resultados.items():
        plt.plot(range(anos+1), valores, marker="o", label=nome)
    plt.title("Comparação de Investimentos")
    plt.xlabel("Ano")
    plt.ylabel("Valor acumulado (R$)")
    plt.legend()
    st.pyplot(plt)

# =========================================================
# 🔹 Rodapé
# =========================================================
st.markdown("""
---
💡 Desenvolvido com Streamlit  
📧 Contato: **seuemail@exemplo.com**  
📱 Instagram: [@seu_perfil](https://instagram.com/seu_perfil)  
💼 LinkedIn: [Seu Nome](https://linkedin.com/in/seu_nome)
""")


