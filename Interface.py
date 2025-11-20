import streamlit as st
from PIL import Image
import datetime

# Configuração da página
st.set_page_config(
    page_title="Bem vindo ao Chat Bot Classificador de imagens",
    page_icon="🤖",
    layout="wide"
)

# Inicializar histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Título principal
st.title("🤖 Chatbot + Classificador de Imagens")
st.markdown("---")

# Layout com duas colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Upload de Imagem")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Escolha uma imagem para análise",
        type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"],
        help="Formatos suportados: JPG, PNG, BMP, TIFF, WEBP"
    )
    
    # Mostrar imagem se foi carregada
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name, use_column_width=True)
        
        # Informações da imagem
        st.success("✅ Imagem carregada com sucesso!")
        st.write(f"**Detalhes:** {image.size[0]}x{image.size[1]} pixels | {uploaded_file.size/1024:.1f} KB")
        
        # Adicionar mensagem automática sobre a imagem
        if len(st.session_state.messages) == 0:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Vi que você enviou uma imagem ({uploaded_file.name}). O que gostaria de saber sobre ela?"
            })
    else:
        st.info("👆 Faça o upload de uma imagem para começar")

with col2:
    st.subheader("💬 Chatbot")
    
    # Container do chat com altura fixa
    chat_container = st.container(height=400)
    
    # Mostrar mensagens do histórico
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Simular resposta do assistente (substitua por sua IA depois)
        if uploaded_file is not None:
            # Resposta relacionada à imagem
            responses = [
                f"Analisando a imagem '{uploaded_file.name}'... Baseado no que vejo, parece ser uma imagem interessante!",
                f"Sobre a imagem que você enviou: estou processando as informações visuais para responder sua pergunta.",
                f"Vi sua pergunta sobre a imagem. Estou analisando os detalhes para te dar uma resposta precisa.",
                f"Com base na imagem carregada, posso te ajudar a entender melhor o conteúdo visual."
            ]
            response = responses[len(st.session_state.messages) % len(responses)]
        else:
            # Resposta genérica (sem imagem)
            response = "Por favor, faça o upload de uma imagem primeiro para que eu possa analisá-la e responder suas perguntas."
        
        # Adicionar resposta do assistente
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Recarregar a página para mostrar as novas mensagens
        st.rerun()

# Área de informações adicionais
st.markdown("---")
with st.expander("ℹ️ Como usar"):
    st.markdown("""
    1. **Faça o upload** de uma imagem na coluna da esquerda
    2. **Converse com o chatbot** na coluna da direita
    3. **Pergunte sobre a imagem** - o bot responderá baseado na análise visual
    4. **Exemplos de perguntas:**
       - "O que tem nesta imagem?"
       - "Descreva o que você vê"
       - "Que cores predominam?"
       - "É uma foto de interior ou exterior?"
    """)

# Rodapé
st.markdown("---")
st.caption(f"Sistema de Chatbot com Classificação de Imagens | {datetime.datetime.now().year}")