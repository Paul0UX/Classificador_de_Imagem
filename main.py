import streamlit as st
from PIL import Image
import io
from app.backend import classificar_imagem
import re

st.set_page_config(
    page_title="Classificador de Imagens IA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
#   CSS CUSTOMIZADO - DESIGN MODERNO
# =====================================================
st.markdown("""
<style>
    /* Paleta de cores */
    :root {
        --primary: #6366f1;
        --danger: #ef4444;
        --success: #10b981;
        --warning: #f59e0b;
        --dark: #0f172a;
        --card-bg: #1e293b;
    }
    
    /* Remove padding padrão */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Cards de categoria */
    .category-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid;
        transition: transform 0.2s;
    }
    
    .category-card:hover {
        transform: translateX(5px);
    }
    
    .cat-1 { border-color: #ef4444; }
    .cat-2 { border-color: #f97316; }
    .cat-3 { border-color: #eab308; }
    .cat-4 { border-color: #dc2626; }
    .cat-5 { border-color: #8b5cf6; }
    
    .category-title {
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    
    .category-items {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.4;
    }
    
    /* Área de upload customizada */
    .upload-area {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 2px dashed #475569;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s;
    }
    
    .upload-area:hover {
        border-color: #6366f1;
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
    }
    
    /* Preview da imagem */
    .image-preview {
        border-radius: 15px;
        border: 3px solid #475569;
        overflow: hidden;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Área de resultado */
    .resultado-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 15px;
        padding: 2rem;
        min-height: 500px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .resultado-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #475569;
    }
    
    .resultado-content {
        color: #e2e8f0;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Badge de classificação */
    .badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1rem 0;
    }
    
    .badge-apropriada {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .badge-inapropriada {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    /* Categoria detectada no resultado */
    .detected-category {
        background: #334155;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 4px solid #6366f1;
    }
    
    /* Estado vazio */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #64748b;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    /* Seção "Como funciona" */
    .how-it-works {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
    }
    
    .step-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .step-number {
        display: inline-block;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: 700;
        margin-right: 1rem;
    }
    
    /* Botão customizado */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
    }
    
    .stButton > button:disabled {
        background: #475569;
        box-shadow: none;
    }
    
    /* Animação de loading */
    .loading-spinner {
        text-align: center;
        padding: 2rem;
    }
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #6366f1;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
#   INICIALIZA ESTADO DA SESSÃO
# =====================================================
if "current_image" not in st.session_state:
    st.session_state.current_image = None

if "resultado" not in st.session_state:
    st.session_state.resultado = None

if "processing" not in st.session_state:
    st.session_state.processing = False


# =====================================================
#   HEADER PRINCIPAL
# =====================================================
st.markdown("""
<div class="main-header">
    <h1>🛡️ Classificador de Imagens com IA</h1>
    <p>Sistema inteligente para detecção de conteúdo inapropriado em imagens</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
#   LAYOUT PRINCIPAL - DUAS COLUNAS
# =====================================================
col_esq, col_dir = st.columns([1, 1], gap="large")


# =====================================================
#   COLUNA ESQUERDA - UPLOAD E INFORMAÇÕES
# =====================================================
with col_esq:
    # Seção de upload
    st.markdown("### 📤 Enviar Imagem")
    st.markdown("Faça upload de uma imagem para análise automática de conteúdo")
    
    uploaded_file = st.file_uploader(
        "Escolha uma imagem",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed"
    )
    
    # Preview da imagem
    if uploaded_file:
        img_bytes = uploaded_file.read()
        st.session_state.current_image = img_bytes
        
        st.markdown("#### 🖼️ Imagem Carregada")
        img = Image.open(io.BytesIO(img_bytes))
        st.markdown('<div class="image-preview">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Informações do arquivo
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📏 Dimensões", f"{img.width}x{img.height}")
        with col2:
            st.metric("📦 Tamanho", f"{len(img_bytes)/1024:.1f} KB")
        
        # Botão de análise
        if st.button("🔍 Analisar Imagem Agora", use_container_width=True, type="primary"):
            st.session_state.processing = True
            st.session_state.resultado = None
            st.rerun()


# =====================================================
#   PROCESSAMENTO DA ANÁLISE
# =====================================================
if st.session_state.processing:
    with col_dir:
        st.markdown("""
        <div class="resultado-container">
            <div class="loading-spinner">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3>Analisando imagem...</h3>
                <p style="color: #64748b;">A IA está processando sua imagem</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    try:
        resultado = classificar_imagem(st.session_state.current_image)
        st.session_state.resultado = resultado
    except Exception as e:
        st.session_state.resultado = f"ERRO|{str(e)}"
    
    st.session_state.processing = False
    st.rerun()


# =====================================================
#   COLUNA DIREITA - RESULTADO DA ANÁLISE
# =====================================================
with col_dir:
    st.markdown("### 🤖 Resultado da Análise")
    
    if st.session_state.resultado:
        resultado_texto = st.session_state.resultado
        
        # Verifica se houve erro
        if resultado_texto.startswith("ERRO|"):
            erro_msg = resultado_texto.split("|", 1)[1]
            st.markdown(f"""
            <div class="resultado-container">
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">❌</div>
                    <h3 style="color: #ef4444;">Erro ao processar imagem</h3>
                    <p style="color: #94a3b8; margin-top: 1rem;">{erro_msg}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Processa o resultado
            # Extrai classificação
            is_apropriada = "APROPRIADA" in resultado_texto.upper() and "INAPROPRIADA" not in resultado_texto.split("CATEGORIAS")[0].upper()
            
            # Extrai e formata as categorias detectadas e resumo
            categorias_detectadas = []
            resumo_texto = ""
            
            linhas = resultado_texto.split('\n')
            in_categorias = False
            in_resumo = False
            
            for linha in linhas:
                linha_strip = linha.strip()
                
                if "CATEGORIAS DETECTADAS" in linha_strip:
                    in_categorias = True
                    in_resumo = False
                    continue
                    
                if "RESUMO" in linha_strip:
                    in_categorias = False
                    in_resumo = True
                    continue
                
                if in_categorias and linha_strip.startswith('-'):
                    texto_cat = linha_strip[1:].strip()
                    categorias_detectadas.append(texto_cat)
                    
                elif in_resumo and linha_strip:
                    resumo_texto += linha_strip + " "
            
            # 1. QUADRADO AZUL - Só com a explicação
            conteudo_quadrado = '<div class="resultado-container">'
            if resumo_texto.strip():
                conteudo_quadrado += f"<p style='color: #e2e8f0; line-height: 1.8; font-size: 1rem;'>{resumo_texto.strip()}</p>"
            else:
                conteudo_quadrado += "<p style='color: #64748b; text-align: center; padding: 2rem;'>Nenhuma explicação disponível</p>"
            conteudo_quadrado += '</div>'
            
            st.markdown(conteudo_quadrado, unsafe_allow_html=True)
            
            # 2. BADGE - Fora do quadrado
            st.markdown("<br>", unsafe_allow_html=True)
            if is_apropriada:
                st.markdown('<span class="badge badge-apropriada">✅ IMAGEM APROPRIADA</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-inapropriada">⚠️ IMAGEM INAPROPRIADA</span>', unsafe_allow_html=True)
            
            # 3. CATEGORIAS DETECTADAS - Fora do quadrado
            if categorias_detectadas:
                st.markdown("<br><h4 style='margin-top: 1rem; color: #f59e0b;'>🎯 Categorias Detectadas:</h4>", unsafe_allow_html=True)
                for cat in categorias_detectadas:
                    st.markdown(f"""
                    <div class="detected-category">
                        <strong style="color: #f59e0b;">▸</strong> {cat}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Botão para nova análise
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Analisar a mesma ou nova imagem", use_container_width=True):
                st.session_state.resultado = None
                st.session_state.current_image = None
                st.rerun()
    else:
        # Estado vazio
        st.markdown("""
        <div class="resultado-container">
            <div class="empty-state">
                <div class="empty-state-icon">💬</div>
                <h3>Aguardando análise</h3>
                <p>Faça upload de uma imagem e clique em "Analisar" para ver os resultados</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Categorias de análise (movidas para cá)
    st.markdown("---")
    st.markdown("### 📋 O que o sistema analisa?")
    st.markdown("Detectamos automaticamente 5 tipos de conteúdo inapropriado:")
    
    st.markdown("""
    <div class="category-card cat-1">
        <div class="category-title">🔥 Categoria 1 – Conteúdos Adultos</div>
        <div class="category-items">Nudez • Seminudez • Atividade sexual • Conteúdo sugestivo</div>
    </div>
    
    <div class="category-card cat-2">
        <div class="category-title">🩸 Categoria 2 – Violência</div>
        <div class="category-items">Sangue • Ferimentos • Armas brancas • Armas de fogo • Violência explícita</div>
    </div>
    
    <div class="category-card cat-3">
        <div class="category-title">🍃 Categoria 3 – Drogas</div>
        <div class="category-items">Drogas ilícitas • Álcool • Cigarro/Vape • Paraphernália</div>
    </div>
    
    <div class="category-card cat-4">
        <div class="category-title">⚠️ Categoria 4 – Conteúdos Perigosos</div>
        <div class="category-items">Automutilação • Suicídio • Perigos • Conteúdo ilegal • Conteúdo perturbador</div>
    </div>
    
    <div class="category-card cat-5">
        <div class="category-title">💬 Categoria 5 – Discurso Problemático</div>
        <div class="category-items">Bullying • Gestos ofensivos • Linguagem de ódio</div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
#   SEÇÃO "COMO FUNCIONA"
# =====================================================
st.markdown("---")
st.markdown("""
<div class="how-it-works">
    <h2 style="text-align: center; margin-bottom: 1.5rem;">💡 Como usar?</h2>
    <p style="text-align: center; color: #94a3b8; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">
        É muito simples! Basta fazer o upload de qualquer imagem usando o botão acima, clicar em "Analisar" 
        e em poucos segundos você receberá um relatório completo informando se a imagem contém algum tipo de 
        conteúdo inapropriado. Nossa inteligência artificial verifica automaticamente 5 categorias diferentes 
        e te mostra exatamente o que foi encontrado (se houver algo). Rápido, fácil e preciso! 🚀
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
#   FOOTER
# =====================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem 0;">
    <p>🛡️ Classificador de Imagens com IA • Powered by Google Gemini</p>
    <p style="font-size: 0.85rem;">Sistema de análise automática de conteúdo visual</p>
</div>
""", unsafe_allow_html=True)