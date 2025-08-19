import streamlit as st
import matplotlib.pyplot as plt

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
# 🔹 Cabeçalho da aplicação
# =========================================================
st.title("💹 Roteirizador de Investimentos")
st.markdown("### Sua rota inteligente para multiplicar patrimônio 🚀")

# =========================================================
# 🔹 Exemplo inicial de uso (para não ficar vazio)
# =========================================================
st.subheader("Exemplo rápido de gráfico:")

valores = [1000, 1200, 1400, 1700, 2100]
anos = [1, 2, 3, 4, 5]

plt.figure(figsize=(6, 4))
plt.plot(anos, valores, marker="o")
plt.title("Evolução do Investimento")
plt.xlabel("Ano")
plt.ylabel("Valor (R$)")
st.pyplot(plt)
