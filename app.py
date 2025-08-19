import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime

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
    # Menu principal
    # ================================
    menu = st.sidebar.radio("📌 Escolha uma seção:", [
        "Simulação de Investimentos",
        "Simulação de Aposentadoria",
        "Comparador de Estratégias",
        "Carteira Simulada",
        "Ranking de Investimentos",
        "Indicador de Risco",
        "Relatório em PDF"
    ])

    # ================================
    # 1 - Simulação de Investimentos
    # ================================
    if menu == "Simulação de Investimentos":
        st.title("📈 Roteirizador de Investimentos")
        st.write("Simule sua rota financeira e descubra como multiplicar seu patrimônio.")

        aporte_inicial = st.sidebar.number_input("💰 Aporte inicial (R$)", min_value=0, value=1000, step=100)
        aporte_mensal = st.sidebar.number_input("📥 Aporte mensal (R$)", min_value=0, value=500, step=50)
        taxa_juros = st.sidebar.slider("📊 Taxa de juros ao ano (%)", 0.0, 30.0, 10.0, step=0.5)
        tempo_anos = st.sidebar.slider("⏳ Tempo de investimento (anos)", 1, 50, 10)

        meses = tempo_anos * 12
        taxa_mensal = (1 + taxa_juros / 100) ** (1 / 12) - 1

        valores = []
        montante = aporte_inicial
        for mes in range(meses):
            montante = montante * (1 + taxa_mensal) + aporte_mensal
            valores.append(montante)

        st.subheader("📊 Crescimento do Investimento")
        fig, ax = plt.subplots()
        ax.plot(range(meses), valores, label="Valor acumulado", color="green")
        ax.set_xlabel("Meses")
        ax.set_ylabel("R$ acumulado")
        ax.legend()
        st.pyplot(fig)

        st.success(f"Após {tempo_anos} anos, você terá acumulado **R$ {montante:,.2f}** 🚀")

    # ================================
    # 2 - Simulação de Aposentadoria
    # ================================
    elif menu == "Simulação de Aposentadoria":
        st.title("🏖️ Simulação de Aposentadoria")

        idade_atual = st.number_input("Idade atual", 18, 100, 30)
        idade_aposentadoria = st.number_input("Idade de aposentadoria desejada", idade_atual+1, 100, 65)
        renda_mensal_desejada = st.number_input("Renda mensal desejada (R$)", 500, 50000, 5000, step=500)
        taxa_juros = st.slider("Taxa de juros ao ano (%)", 0.0, 30.0, 8.0)

        anos_investimento = idade_aposentadoria - idade_atual
        montante_necessario = renda_mensal_desejada * 12 * 20  # considera 20 anos de aposentadoria

        st.info(f"💡 Para se aposentar aos {idade_aposentadoria}, você precisará acumular **R$ {montante_necessario:,.2f}**.")

        taxa_mensal = (1 + taxa_juros/100)**(1/12) - 1
        meses = anos_investimento * 12
        aporte_mensal_necessario = montante_necessario * taxa_mensal / ((1+taxa_mensal)**meses - 1)

        st.success(f"➡️ Você precisará investir cerca de **R$ {aporte_mensal_necessario:,.2f} por mês**.")

    # ================================
    # 3 - Comparador de Estratégias
    # ================================
    elif menu == "Comparador de Estratégias":
        st.title("⚖️ Comparador de Estratégias")

        aporte_inicial = st.number_input("Aporte inicial (R$)", 0, 1000000, 1000)
        aporte_mensal = st.number_input("Aporte mensal (R$)", 0, 100000, 500)
        tempo_anos = st.slider("Tempo (anos)", 1, 50, 10)

        taxa1 = st.slider("Taxa estratégia 1 (%)", 0.0, 30.0, 8.0)
        taxa2 = st.slider("Taxa estratégia 2 (%)", 0.0, 30.0, 12.0)

        meses = tempo_anos * 12
        def simular(taxa):
            taxa_mensal = (1 + taxa/100)**(1/12) - 1
            valores, montante = [], aporte_inicial
            for _ in range(meses):
                montante = montante*(1+taxa_mensal)+aporte_mensal
                valores.append(montante)
            return valores

        valores1, valores2 = simular(taxa1), simular(taxa2)

        fig, ax = plt.subplots()
        ax.plot(range(meses), valores1, label=f"Estratégia 1 ({taxa1}% a.a.)")
        ax.plot(range(meses), valores2, label=f"Estratégia 2 ({taxa2}% a.a.)")
        ax.legend()
        st.pyplot(fig)

    # ================================
    # 4 - Carteira Simulada
    # ================================
    elif menu == "Carteira Simulada":
        st.title("📊 Carteira de Investimentos")

        st.write("Monte sua carteira com pesos e veja a evolução.")

        renda_fixa = st.slider("Renda Fixa (%)", 0, 100, 50)
        acoes = st.slider("Ações (%)", 0, 100-renda_fixa, 30)
        fundos = 100 - renda_fixa - acoes

        st.write(f"Distribuição: Renda Fixa {renda_fixa}%, Ações {acoes}%, Fundos {fundos}%")

        taxas = {"Renda Fixa": 6, "Ações": 12, "Fundos": 9}
        pesos = [renda_fixa/100, acoes/100, fundos/100]

        taxa_carteira = sum([taxas[k]*p for k,p in zip(taxas.keys(), pesos)])
        st.info(f"Taxa média estimada da carteira: {taxa_carteira:.2f}% a.a.")

    # ================================
    # 5 - Ranking de Investimentos
    # ================================
    elif menu == "Ranking de Investimentos":
        st.title("🏆 Ranking de Investimentos")

        dados = {
            "Investimento": ["Tesouro Selic", "CDB", "Fundos", "Ações"],
            "Rentabilidade (% a.a.)": [6, 8, 10, 12]
        }
        df = pd.DataFrame(dados)
        df = df.sort_values(by="Rentabilidade (% a.a.)", ascending=False)

        st.table(df)

    # ================================
    # 6 - Indicador de Risco
    # ================================
    elif menu == "Indicador de Risco":
        st.title("⚠️ Indicador de Risco")

        perfil = st.radio("Escolha seu perfil de investidor", ["Conservador", "Moderado", "Agressivo"])

        if perfil == "Conservador":
            st.success("🔹 Sugestão: 80% Renda Fixa, 15% Fundos, 5% Ações")
        elif perfil == "Moderado":
            st.success("🔹 Sugestão: 50% Renda Fixa, 30% Fundos, 20% Ações")
        else:
            st.success("🔹 Sugestão: 20% Renda Fixa, 30% Fundos, 50% Ações")

    # ================================
    # 7 - Relatório em PDF
    # ================================
    elif menu == "Relatório em PDF":
        st.title("📄 Gerar Relatório em PDF")

        nome = st.text_input("Digite seu nome")
        resumo = st.text_area("Resumo da simulação")

        if st.button("Gerar PDF"):
            doc = SimpleDocTemplate("relatorio.pdf")
            styles = getSampleStyleSheet()
            story = []

            story.append(Paragraph(f"Relatório Financeiro - {nome}", styles['Title']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Data: {datetime.date.today()}", styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(resumo, styles['Normal']))

            doc.build(story)
            with open("relatorio.pdf", "rb") as file:
                st.download_button("⬇️ Baixar Relatório", file, "relatorio.pdf")

else:
    st.warning("🔒 Acesso restrito. Faça login com seu e-mail e senha cadastrados.")


