import streamlit as st
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# ===== Função para gerar relatório em PDF =====
def gerar_pdf(idade, aporte_mensal, prazo_anos, perfil, valores, anos, alocacao, taxa):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>Roteiro de Investimentos ({perfil})</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph("📌 Alocação Recomendada:", styles["Heading2"]))
    for ativo, perc in alocacao.items():
        story.append(Paragraph(f"- {ativo}: {perc*100:.0f}%", styles["Normal"]))

    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Projeção em {prazo_anos} anos com aporte de R${aporte_mensal:.2f}/mês:", styles["Heading2"]))

    # Salvar gráfico temporário
    plt.plot(anos, valores, marker="o")
    plt.title("Projeção de Crescimento do Patrimônio")
    plt.xlabel("Ano")
    plt.ylabel("Valor acumulado (R$)")
    plt.grid()
    plt.savefig("grafico.png")
    plt.close()

    story.append(Image("grafico.png", width=400, height=200))

    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Idade atual: {idade} anos", styles["Normal"]))
    story.append(Paragraph(f"Aporte mensal: R${aporte_mensal:.2f}", styles["Normal"]))
    story.append(Paragraph(f"Taxa de crescimento anual considerada: {taxa*100:.0f}%", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ===== App Streamlit =====
st.set_page_config(page_title="Roteirizador de Investimentos", page_icon="💰", layout="centered")

st.title("💰 Roteirizador de Investimentos")
st.write("Preencha os dados abaixo e gere seu plano de investimentos automatizado.")

# Entradas do usuário
idade = st.number_input("Idade", min_value=18, max_value=100, value=30)
aporte_mensal = st.number_input("Aporte mensal (R$)", min_value=100.0, value=1000.0, step=50.0)
prazo_anos = st.number_input("Prazo do investimento (anos)", min_value=1, max_value=50, value=10)
perfil = st.selectbox("Perfil de risco", ["Conservador", "Moderado", "Arrojado"])

# Alocação por perfil
alocacoes = {
    "Conservador": {"Renda Fixa": 0.8, "Fundos Imobiliários": 0.15, "Ações": 0.05},
    "Moderado": {"Renda Fixa": 0.5, "Fundos Imobiliários": 0.3, "Ações": 0.2},
    "Arrojado": {"Renda Fixa": 0.3, "Fundos Imobiliários": 0.3, "Ações": 0.4},
}
alocacao = alocacoes[perfil]

# Taxa média de crescimento
taxas = {"Conservador": 0.05, "Moderado": 0.08, "Arrojado": 0.12}
taxa = taxas[perfil]

# Simulação de crescimento
valor = 0
valores = []
anos = list(range(1, prazo_anos + 1))
for ano in anos:
    valor = (valor + (aporte_mensal * 12)) * (1 + taxa)
    valores.append(valor)

# Mostrar resultado na tela
st.subheader("📊 Projeção de Crescimento do Patrimônio")
fig, ax = plt.subplots()
ax.plot(anos, valores, marker="o")
ax.set_title("Projeção de Crescimento")
ax.set_xlabel("Ano")
ax.set_ylabel("Valor acumulado (R$)")
ax.grid()
st.pyplot(fig)

st.write("### 💡 Alocação Recomendada:")
for ativo, perc in alocacao.items():
    st.write(f"- {ativo}: **{perc*100:.0f}%**")

# Botão para gerar PDF
if st.button("📥 Baixar Relatório em PDF"):
    pdf_buffer = gerar_pdf(idade, aporte_mensal, prazo_anos, perfil, valores, anos, alocacao, taxa)
    st.download_button(
        label="⬇️ Download do PDF",
        data=pdf_buffer,
        file_name="roteiro_investimentos.pdf",
        mime="application/pdf",
    )
