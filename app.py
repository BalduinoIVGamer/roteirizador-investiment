import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ================================
# FUNÇÃO PARA LER USUÁRIOS
# ================================
def carregar_usuarios():
    try:
        usuarios_df = pd.read_csv("usuarios.csv")
        return dict(zip(usuarios_df.usuario, usuarios_df.senha))
    except:
        return {}

usuarios = carregar_usuarios()

# ================================
# LOGIN
# ================================
st.sidebar.title("🔑 Acesso Restrito")
usuario = st.sidebar.text_input("E-mail")
senha = st.sidebar.text_input("Senha", type="password")

if usuario in usuarios and usuarios[usuario] == senha:
    st.sidebar.success("✅ Login realizado com sucesso!")

    # ================================
    # Banner
    # ================================
    st.image("banner.png", use_container_width=True)

    # ================================
    # Título e descrição
    # ================================
    st.title("📈 Roteirizador de Investimentos")
    st.write("Simule sua rota financeira e descubra como multiplicar seu patrimônio.")

    # ================================
    # Entrada de dados
    # ================================
    st.sidebar.header("Parâmetros da Simulação")

    aporte_inicial = st.sidebar.number_input("💰 Aporte inicial (R$)", min_value=0, value=1000, step=100)
    aporte_mensal = st.sidebar.number_input("📥 Aporte mensal (R$)", min_value=0, value=500, step=50)
    taxa_juros = st.sidebar.slider("📊 Taxa de juros ao ano (%)", 0.0, 30.0, 10.0, step=0.5)
    tempo_anos = st.sidebar.slider("⏳ Tempo de investimento (anos)", 1, 50, 10)

    # ================================
    # Simulação
    # ================================
    meses = tempo_anos * 12
    taxa_mensal = (1 + taxa_juros / 100) ** (1 / 12) - 1

    valores = []
    montante = aporte_inicial
    for mes in range(meses):
        montante = montante * (1 + taxa_mensal) + aporte_mensal
        valores.append(montante)

    # ================================
    # Gráfico principal
    # ================================
    st.subheader("📊 Crescimento do Investimento")
    fig, ax = plt.subplots()
    ax.plot(range(meses), valores, label="Valor acumulado", color="green")
    ax.set_xlabel("Meses")
    ax.set_ylabel("R$ acumulado")
    ax.legend()
    st.pyplot(fig)

    # ================================
    # Comparação com cenários
    # ================================
    st.subheader("📈 Comparação de Cenários")
    taxas_comparacao = [5, 10, 15]
    fig2, ax2 = plt.subplots()

    for taxa in taxas_comparacao:
        taxa_mensal_comp = (1 + taxa / 100) ** (1 / 12) - 1
        montante_comp = aporte_inicial
        valores_comp = []
        for mes in range(meses):
            montante_comp = montante_comp * (1 + taxa_mensal_comp) + aporte_mensal
            valores_comp.append(montante_comp)
        ax2.plot(range(meses), valores_comp, label=f"Taxa {taxa}% a.a.")

    ax2.set_xlabel("Meses")
    ax2.set_ylabel("R$ acumulado")
    ax2.legend()
    st.pyplot(fig2)

    # ================================
    # Resultado final
    # ================================
    st.subheader("📌 Resultado Final")
    st.success(f"Após {tempo_anos} anos, você terá acumulado **R$ {montante:,.2f}** 🚀")

    # ================================
    # Rodapé
    # ================================
    st.markdown("---")
    st.caption("🧩 Roteirizador de Investimentos | Acesso exclusivo para clientes Hotmart.")

else:
    st.warning("🔒 Acesso restrito. Faça login com seu e-mail e senha cadastrados.")

