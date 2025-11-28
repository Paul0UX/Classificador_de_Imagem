from PIL import Image
import io
import base64
import requests
from app.config import API_KEY, BASE_URL

CLASSIFICADOR_PROMPT = """
Você é um CLASSIFICADOR DE IMAGENS especializado para detectar conteúdo inapropriado.

Analise EXCLUSIVAMENTE a imagem enviada e verifique a presença dos itens abaixo:

🔥 CATEGORIA 1 – Conteúdos adultos
- Nudez
- Seminudês
- Atividade sexual
- Conteúdo sugestivo

🩸 CATEGORIA 2 – Violência
- Sangue
- Ferimentos
- Armas brancas
- Armas de fogo
- Violência explícita
- Violência doméstica

🍃 CATEGORIA 3 – Drogas
- Uso de drogas ilícitas
- Consumo de álcool
- Consumo de cigarro/vape
- Paraphernália de drogas

⚠️ CATEGORIA 4 – Conteúdos perigosos
- Automutilação
- Tentativa de suicídio
- Comportamentos perigosos (ex.: perigo de queda)
- Crianças em perigo
- Conteúdo ilegal
- Conteúdo perturbador (morte, cadáver, etc.)

💬 CATEGORIA 5 – Discurso problemático
- Bullying
- Gestos ofensivos

RETORNE O RESULTADO NO FORMATO:

CLASSIFICAÇÃO: (APROPRIADA ou INAPROPRIADA)

CATEGORIAS DETECTADAS:
- Categoria X – Nome → explicação
- Categoria X – Nome → explicação

RESUMO:
Explique em poucas frases o motivo final.

NÃO invente elementos que não estão na imagem.
"""

def classificar_imagem(imagem_bytes):
    if not API_KEY:
        raise ValueError("API_KEY não encontrada. Verifique o arquivo .env")

    try:
        # Processar imagem
        img = Image.open(io.BytesIO(imagem_bytes))

        if img.mode != "RGB":
            img = img.convert("RGB")

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=95)
        imagem_jpeg = buffer.getvalue()

        imagem_base64 = base64.b64encode(imagem_jpeg).decode()

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": CLASSIFICADOR_PROMPT},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": imagem_base64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        }

        response = requests.post(BASE_URL, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        raise Exception(f"Erro ao processar: {str(e)}")
