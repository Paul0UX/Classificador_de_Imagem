import streamlit as st
from app.backend import analisar_imagem
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Chat analisador de imagem",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS CUSTOMIZADOS ---
st.markdown(
    """
    <style>
    /* Fundo escuro geral */
    .stApp {
        background-color: #1a1d24;
    }
    
    /* Container principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Títulos das seções */
    .section-title {
        font-size: 1.2em;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Área do chat - Container Streamlit */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background-color: #242830;
        border-radius: 12px;
        padding: 1.5rem;
        height: 500px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    
    /* Mensagens do chat */
    .message {
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 8px;
        animation: fadeIn 0.3s ease-in;
    }
    
    .user-message {
        background-color: #2d3340;
        border-left: 3px solid #4A90E2;
    }
    
    .ai-message {
        background-color: #1e2128;
        border-left: 3px solid #10b981;
    }
    
    .loading-message {
        background-color: #2d3340;
        border-left: 3px solid #f59e0b;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Animação de loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-dots {
        display: inline-flex;
        gap: 0.25rem;
    }
    
    .loading-dots span {
        width: 8px;
        height: 8px;
        background-color: #4A90E2;
        border-radius: 50%;
        animation: pulse 1.4s infinite;
    }
    
    .loading-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .loading-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Welcome screen */
    .welcome-screen {
        text-align: center;
        color: #6b7280;
        padding: 3rem 1rem;
    }
    
    /* Input de pergunta */
    .stTextInput input {
        background-color: #2d3340;
        color: #ffffff;
        border: 1px solid #4a5568;
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    .stTextInput input:focus {
        border-color: #4A90E2;
        box-shadow: 0 0 0 1px #4A90E2;
    }
    
    /* Botão customizado */
    .stButton button {
        background-color: #4A90E2;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #357ABD;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
    }
    
    /* Botão desabilitado */
    .stButton button:disabled {
        background-color: #4a5568;
        cursor: not-allowed;
        transform: none;
    }
    
    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* File uploader customizado */
    .uploadedFile {
        background-color: #2d3340;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Footer customizado */
    .custom-footer {
        color: #6b7280;
        font-size: 0.85em;
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
    }
    
    /* Limpar chat button */
    .clear-chat-btn button {
        background-color: #dc2626 !important;
        font-size: 0.9em;
        padding: 0.4rem 1rem;
    }
    
    .clear-chat-btn button:hover {
        background-color: #b91c1c !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- INICIALIZAR SESSION STATE ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# --- LAYOUT PRINCIPAL (2 COLUNAS) ---
col_left, col_right = st.columns([1, 1.5])

# ===== COLUNA ESQUERDA: UPLOAD =====
with col_left:
    st.markdown('<p class="section-title">📁 Upload de Imagem</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #9ca3af; font-size: 0.9em; margin-bottom: 1rem;">Escolha uma imagem para análise</p>', unsafe_allow_html=True)
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=["jpg", "jpeg", "png", "webp"],
        help="Limit 200MB per file • JPG, JPEG, PNG, WEBP",
        label_visibility="collapsed"
    )
    
    # Mostrar preview se houver imagem
    if uploaded_file:
        # Salvar bytes da imagem
        image_bytes = uploaded_file.read()
        st.session_state.current_image = image_bytes
        uploaded_file.seek(0)  # Reset para mostrar preview
        
        st.markdown("---")
        st.markdown("### 🖼️ Pré-visualização")
        st.image(uploaded_file, width="stretch")  # ← CORRIGIDO
        
        # Informações do arquivo
        st.markdown(f"<p style='color: #9ca3af; font-size: 0.85em;'>📄 {uploaded_file.name}</p>", unsafe_allow_html=True)
    else:
        st.session_state.current_image = None
        st.info("👆 Faça upload de uma imagem para começar", icon="ℹ️")

# ===== COLUNA DIREITA: CHAT =====
with col_right:
    st.markdown('<p class="section-title">💬 Chat com a IA </p>', unsafe_allow_html=True)
    
    # Container do chat usando st.container() com altura fixa via CSS
    chat_container = st.container(height=500)
    
    with chat_container:
        # Renderizar mensagens do chat
        if not st.session_state.chat_history:
            st.markdown(
                """
                <div class="welcome-screen">
                    <h3 style="color: #9ca3af;">💡 Como começar?</h3>
                    <p>1. Faça upload de uma imagem à esquerda</p>
                    <p>2. Digite sua pergunta abaixo</p>
                    <p>3. Clique em enviar e receba a análise da IA!</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(
                        f"""
                        <div class="message user-message">
                            <strong style="color: #4A90E2;">👤 Você:</strong>
                            <p style="color: #e5e7eb; margin-top: 0.5rem; margin-bottom: 0;">{msg['content']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                elif msg['role'] == 'loading':
                    st.markdown(
                        """
                        <div class="message loading-message">
                            <strong style="color: #f59e0b;">⏳ Analisando</strong>
                            <div class="loading-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:  # assistant
                    st.markdown(
                        f"""
                        <div class="message ai-message">
                            <strong style="color: #10b981;">🤖 AI:</strong>
                            <p style="color: #e5e7eb; margin-top: 0.5rem; margin-bottom: 0; white-space: pre-wrap;">{msg['content']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    # Input e botão de envio
    st.markdown("---")
    
    col_input, col_send = st.columns([4, 1])
    
    with col_input:
        user_question = st.text_input(
            "Pergunta",
            placeholder="Pergunte sobre a imagem...",
            label_visibility="collapsed",
            key="question_input",
            disabled=st.session_state.processing
        )
    
    with col_send:
        send_button = st.button(
            "➤", 
            width="stretch",  # ← CORRIGIDO
            disabled=st.session_state.processing
        )
    
    # Botão limpar chat
    if st.session_state.chat_history:
        st.markdown('<div class="clear-chat-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Limpar Chat", width="stretch", disabled=st.session_state.processing):  # ← CORRIGIDO
            st.session_state.chat_history = []
            st.session_state.processing = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE PROCESSAMENTO ---
if send_button and not st.session_state.processing:
    if not st.session_state.current_image:
        st.error("⚠️ Por favor, faça upload de uma imagem primeiro!")
    elif not user_question.strip():
        st.warning("⚠️ Por favor, digite uma pergunta!")
    else:
        # Marcar como processando
        st.session_state.processing = True
        
        # Adicionar pergunta do usuário ao histórico
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_question
        })
        
        # Adicionar indicador de loading
        st.session_state.chat_history.append({
            'role': 'loading',
            'content': ''
        })
        
        # Recarregar para mostrar loading no chat
        st.rerun()

# --- PROCESSAMENTO EM BACKGROUND ---
if st.session_state.processing and st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == 'loading':
    try:
        # Pegar a pergunta (penúltima mensagem)
        user_question = st.session_state.chat_history[-2]['content']
        
        # Processar com a IA (passa os bytes da imagem)
        resposta = analisar_imagem(st.session_state.current_image, user_question)
        
        # Remover loading e adicionar resposta
        st.session_state.chat_history.pop()
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': resposta
        })
        
    except Exception as e:
        # Remover loading e adicionar erro
        st.session_state.chat_history.pop()
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"❌ Erro ao processar: {str(e)}"
        })
    
    finally:
        # Desmarcar processamento
        st.session_state.processing = False
        # Recarregar para mostrar resposta
        st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div class="custom-footer">
        Analisador de Imagem
        <br>
        <span style="font-size: 0.75em;">Powered by Gemini AI</span>
    </div>
    """,
    unsafe_allow_html=True
)