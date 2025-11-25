import streamlit as st
from app.backend import analisar_imagem

st.title("🔍 IA Classificadora e Analisadora de Imagens")

uploaded_image = st.file_uploader("Envie uma imagem", type=["jpg", "jpeg", "png"])
question = st.text_input("Pergunte algo sobre a imagem (opcional):")

if st.button("Analisar"):
    if uploaded_image:
        image_bytes = uploaded_image.read()
        resposta = analisar_imagem(image_bytes, question)
        st.image(uploaded_image, caption="Imagem enviada", width=350)
        st.write("### 📘 Resposta da IA:")
        st.write(resposta)
    else:
        st.warning("Envie uma imagem antes de analisar.")
