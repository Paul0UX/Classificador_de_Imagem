# 🖼️ Classificador de Imagens com IA (Google Gemini + LLM)

Este projeto é um **classificador de imagens** que utiliza **IA generativa (LLM)** através da **API Gemini**, permitindo identificar conteúdos presentes em fotos enviadas pelo usuário.  
A interface é construída em **Streamlit**, proporcionando uma experiência simples, rápida e intuitiva.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit**
- **Google Gemini 2.5 flash API (LLM multimodal)**
- **python-dotenv**
- **Pillow (PIL)**
- **Bibliotecas para processamento de imagem**

O classificador utiliza modelos multimodais do **Google Gemini**, capazes de interpretar imagens e gerar descrições inteligentes sobre seu conteúdo.

---

## ⚠️ Aviso Importante

Este projeto **não deve ser utilizado como fonte de verdade absoluta**, especialmente em cenários que envolvem riscos.  
A IA **pode errar**, portanto:

### ❌ Não utilize este classificador para:
- Identificar alimentos potencialmente venenosos  
- Verificar se plantas ou cogumelos são tóxicos  
- Avaliar segurança de animais, insetos ou substâncias  
- Tomar decisões que envolvam **saúde**, **segurança** ou **riscos à vida**

> **Use apenas para fins educacionais, experimentais ou demonstração.**

---

## 📦 Como instalar e rodar o projeto

1. Faça o download ou clone o projeto a partir da branch **main** no GitHub.

2. Certifique-se de ter o **Python 3.10 ou superior** instalado em seu sistema.

3. O **pip** já vem incluído nas instalações modernas do Python.

4. Na raiz do projeto, crie um ambiente virtual executando: ''python -m venv venv''

5. Ative o ambiente virtual no CMD do windows digitando: ''venv\Scripts\activate''.
  5.1 você deverá visualizar algo como: ''(venv) C:\Users\SeuUsuario\...''.

6. Instale todas as dependencias necessárias podendo ser no propio terminal do vscode: ''pip install -r requirements.txt''.

7. Crie um arquivo .env na raiz do projeto contendo sua chave da API Gemini: GEMINI_API_KEY=SuaChaveAqui

8. Por fim, execute a aplicação com: ''streamlit run main.py''
