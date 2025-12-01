# 🖼️ Classificador de Imagens com IA (Google Gemini + LLM)

Este projeto é um **classificador de imagens** que utiliza **IA generativa (LLM)** através da **API Gemini**, permitindo identificar conteúdos presentes em fotos enviadas pelo usuário e classificando como inapropriada ou apropriada.  
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
## 🧩Categorias de Conteudos Inapropiados:

CATEGORIA 1 – Conteúdos adultos
- Nudez
- Seminudês
- Atividade sexual
- Conteúdo sugestivo

CATEGORIA 2 – Violência
- Sangue
- Ferimentos
- Armas brancas
- Armas de fogo
- Violência explícita
- Violência doméstica

CATEGORIA 3 – Drogas
- Uso de drogas ilícitas
- Consumo de álcool
- Consumo de cigarro/vape
- Paraphernália de drogas

CATEGORIA 4 – Conteúdos perigosos
- Automutilação
- Tentativa de suicídio
- Comportamentos perigosos (ex.: perigo de queda)
- Crianças em perigo
- Conteúdo ilegal
- Conteúdo perturbador (morte, cadáver, etc.)

CATEGORIA 5 – Discurso problemático
- Bullying
- Gestos ofensivos
---

## 🔑 Como obter sua chave da API Gemini (Google AI)

1. Acesse o **Google AI Studio**:  
   https://aistudio.google.com

2. Faça login com sua conta Google.

3. No menu lateral, clique em **"API Keys"** ou **"Chaves de API"**.

4. Clique em **"Create API Key"** (Criar chave de API).

5. Selecione o tipo de chave **“Client-side”** ou **“Server-side”**, dependendo da sua necessidade  
   (para este projeto, qualquer uma funciona).

6. Uma chave será gerada. Copie o valor exibido.

7. Crie o arquivo `.env` na raiz do projeto e adicione: ''GEMINI_API_KEY=SuaChaveAqui''.

8. Salve o arquivo e já poderá utilizar o modelo Gemini no projeto.

> **Observação:** Mantenha sua chave privada e não a envie para repositórios públicos.



## 📦 Como instalar e rodar o projeto

1. Faça o download ou clone o projeto a partir da branch **main** no GitHub.

2. Certifique-se de ter o **Python 3.10 ou superior** instalado em seu sistema.

3. O **pip** já vem incluído nas instalações modernas do Python.

4. Na raiz do projeto, crie um ambiente virtual executando: ''python -m venv venv''

5. Ative o ambiente virtual no CMD do windows digitando: ''venv\Scripts\activate''.
   5.1 você deverá visualizar algo como: ''(venv) C:\Users\SeuUsuario\...''.

6. Instale todas as dependencias necessárias podendo ser no propio terminal do vscode: ''pip install -r requirements.txt''.

7. Crie um arquivo .env na raiz do projeto contendo sua chave da API Gemini: ''GEMINI_API_KEY=SuaChaveAqui''.

8. Por fim, execute a aplicação com: ''streamlit run main.py''.

## 🧐 Utilizando o programa

1. Insira uma imagem no local indicado, de preferencia JPG ou JPEG:
<img width="424" height="182" alt="image" src="https://github.com/user-attachments/assets/cb7a8e38-5b78-40e9-bebc-b429aa68fa07" />


---

2. Por fim clicar no botão ''Analisar Imagem'':
<img width="1822" height="781" alt="image" src="https://github.com/user-attachments/assets/c14b9784-b266-4330-a47f-a9f382aac9f6" />



---

3. Atente-se ao seu numero limitado de tokens, pois quando acabar, o programa não respondera mais.
