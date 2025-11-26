import streamlit as st
from app.backend import analisar_imagem # Certifique-se de que o caminho está correto

# --- 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS ---

# Configurações iniciais
st.set_page_config(
    page_title="IA Classificadora de Imagens",
    layout="wide", # Layout mais largo para melhor uso do espaço
    initial_sidebar_state="collapsed"
)

# Estilos CSS customizados para título, subtítulo e, crucialmente, ALINHAMENTO VERTICAL
st.markdown(
    """
    <style>
    /* Estilizando o Título Principal */
    .big-title {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.2em;
        color: #4A90E2; /* Azul vibrante */
    }
    /* Estilizando o Subtítulo */
    .subtitle {
        font-size: 1.1em;
        text-align: center;
        margin-bottom: 1.5em;
        color: #A0A0A0; /* Cor mais suave */
    }
    /* Estilo para garantir o ALINHAMENTO VERTICAL (centro) na coluna de pré-visualização */
    /* Este seletor (st-emotion-cache-1jm6gjm) é o que geralmente envolve o conteúdo das colunas no Streamlit */
    .st-emotion-cache-1jm6gjm > div:nth-child(1) { 
        display: flex;
        flex-direction: column;
        justify-content: center; /* Centraliza verticalmente */
        height: 100%;
    }
    /* Centralizando o botão para preencher a largura */
    div.stButton > button {
        width: 100%;
        font-size: 1.1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. TÍTULO E CABEÇALHO ---

st.markdown('<p class="big-title">🔍 IA Classificadora e Analisadora de Imagens</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Faça o upload de uma imagem e pergunte qualquer coisa sobre ela!</p>', unsafe_allow_html=True)

st.divider() # Linha divisória

# --- 3. ÁREA DE INPUT (UPLOAD E PERGUNTA) ---

# Usando colunas para organizar o uploader (esquerda) e a pré-visualização (direita)
col_upload, col_preview = st.columns([1, 1])

# COLUNA DE UPLOAD
with col_upload:
    uploaded_image = st.file_uploader(
        "1. Upload de Imagem", 
        type=["jpg", "jpeg", "png"],
        help="Limite de 300MB por arquivo. Tipos aceitos: JPG, JPEG, PNG."
    )

# COLUNA DE PRÉ-VISUALIZAÇÃO (Alinhada verticalmente pelo CSS)
with col_preview:
    # Usando um container para garantir que o st.info preencha o espaço
    if uploaded_image:
        with st.expander("🖼️ Pré-visualização da Imagem Enviada", expanded=True):
            st.image(uploaded_image, width='stretch')
    else:
        st.info("Aguardando o upload de uma imagem na coluna ao lado.")

# Input de texto da pergunta
question = st.text_input(
    "2. Pergunta Opcional",
    placeholder="Ex: Qual é o objeto principal? Descreva o fundo.",
    help="Deixe vazio para uma descrição técnica padrão."
)

st.divider()

# --- 4. LÓGICA DE ANÁLISE ---

# Botão de Análise (o tipo="primary" deixa ele em destaque)
if st.button("✨ 3. Analisar Imagem", use_container_width=True, type="primary"):
    if uploaded_image:
        # Usa o st.spinner para dar feedback visual de processamento
        with st.spinner("⏳ Analisando imagem com a IA..."):
            try:
                # Chama a função de backend
                image_bytes = uploaded_image.read()
                resposta = analisar_imagem(image_bytes, question)
                
                # Exibição da Resposta
                st.success("✅ Análise Concluída!")
                st.markdown("### 🤖 Resposta da IA:")
                st.info(resposta) # Usa st.info para destacar o bloco de texto da resposta

            except Exception as e:
                # Captura erros durante a análise
                st.error(f"❌ Ocorreu um erro durante a análise: {e}")
                
    else:
        # Aviso se o botão for clicado sem imagem
        st.warning("⚠️ Por favor, envie uma imagem no campo '1. Upload de Imagem' antes de analisar.")