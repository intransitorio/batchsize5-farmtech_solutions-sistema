import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FarmTech Solutions - Dashboard",
    layout="wide"
)

st.title("FarmTech Solutions")
st.subheader("Dashboard de Monitoramento Agrícola - Fase 3")

df = pd.read_csv("sensores_fase3.csv", sep=";")

df["Umid"] = df["Umid"].astype(str).str.replace(",", ".").astype(float)
df["pH"] = df["pH"].astype(str).str.replace(",", ".").astype(float)

st.write("## Dados coletados dos sensores")
st.dataframe(df)

ultima = df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Umidade atual", f"{ultima['Umid']}%")
col2.metric("pH atual", f"{ultima['pH']}")
col3.metric("Deficiência P", "Sim" if ultima["Defic_P"] == 1 else "Não")
col4.metric("Deficiência K", "Sim" if ultima["Defic_K"] == 1 else "Não")

st.write("## Gráficos de monitoramento")

st.write("### Nível de umidade")
st.line_chart(df.set_index("Timestamp")["Umid"])

st.write("### Nível de pH")
st.line_chart(df.set_index("Timestamp")["pH"])

st.write("### Deficiências nutricionais P e K")
st.line_chart(df.set_index("Timestamp")[["Defic_P", "Defic_K"]])

st.write("### Status da irrigação / bomba")
st.line_chart(df.set_index("Timestamp")["Bomba"])

st.write("## Sugestão de irrigação baseada em clima")

chuva_prevista = st.selectbox(
    "Há previsão de chuva nas próximas horas?",
    ["Não", "Sim"]
)

umidade = ultima["Umid"]
ph = ultima["pH"]
deficiencia_p = ultima["Defic_P"] == 1
deficiencia_k = ultima["Defic_K"] == 1

if chuva_prevista == "Sim":
    st.info("Sugestão: manter a irrigação desligada, pois há previsão de chuva.")
elif ph < 5.5 or ph > 6.5:
    st.warning("Sugestão: não acionar fertirrigação. O pH está fora da faixa ideal.")
elif umidade >= 75:
    st.warning("Sugestão: manter a bomba desligada para evitar encharcamento.")
elif umidade < 60 or deficiencia_p or deficiencia_k:
    st.success("Sugestão: acionar irrigação/fertirrigação. Há baixa umidade ou deficiência nutricional.")
else:
    st.info("Sugestão: manter a bomba desligada. As condições estão estáveis.")
