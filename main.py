import streamlit as st
from PIL import Image
import io
from app.backend import classificar_imagem

st.set_page_config(
    page_title="Classificador de Imagens",
    page_icon="🖼️",
    layout="wide"
)

# -----------------------------
# CSS de estilo
# -----------------------------
st.markdown("""
<style>
    .resultado-card {
        background: #0d1117;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        color: #e6e6e6;
        font-size: 16px;
        white-space: pre-wrap;
        height: 600px;
        overflow-y: auto;
    }
    .preview-box img {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# INICIALIZA ESTADO
# -----------------------------
if "current_image" not in st.session_state:
    st.session_state.current_image = None

if "resultado" not in st.session_state:
    st.session_state.resultado = None

if "processing" not in st.session_state:
    st.session_state.processing = False


# -----------------------------
# LAYOUT EM DUAS COLUNAS
# -----------------------------
col_esq, col_dir = st.columns([1, 1])  # mesma proporção do print


# =====================================================
#   COLUNA ESQUERDA  —  UPLOAD + PRÉ-VISUALIZAÇÃO
# =====================================================
with col_esq:
    st.subheader("📁 Upload de Imagem")

    uploaded_file = st.file_uploader(
        "Escolha uma imagem para análise",
        type=["png", "jpg", "jpeg", "webp"]
    )

    # Se ainda não enviou imagem → mostra só o botão logo abaixo do uploader
    if not uploaded_file:
        st.button("🔍 Analisar Imagem", use_container_width=True, disabled=True)

    # Se enviou → mostrar prévia e mover botão para baixo da imagem
    if uploaded_file:
        img_bytes = uploaded_file.read()
        st.session_state.current_image = img_bytes

        st.markdown("### 📸 Pré-visualização")
        img = Image.open(io.BytesIO(img_bytes))
        st.image(img, width=400)

        # Botão agora aparece aqui embaixo (abaixo da imagem)
        if st.button("🔍 Analisar Imagem", use_container_width=True):
            st.session_state.processing = True
            st.session_state.resultado = None
            st.rerun()



# PROCESSAMENTO ASSÍNCRONO
if st.session_state.processing:
    with st.spinner("Analisando imagem..."):
        try:
            resultado = classificar_imagem(st.session_state.current_image)
            st.session_state.resultado = resultado
        except Exception as e:
            st.session_state.resultado = f"❌ Erro ao analisar imagem:\n{str(e)}"

    st.session_state.processing = False
    st.rerun()


# =====================================================
#   COLUNA DIREITA  —  RESULTADO DA IA
# =====================================================
with col_dir:
    st.subheader("💬 Resposta da IA")

    st.markdown(
        "<div class='resultado-card'>"
        + (st.session_state.resultado if st.session_state.resultado else "Aguardando análise...")
        + "</div>",
        unsafe_allow_html=True
    )
