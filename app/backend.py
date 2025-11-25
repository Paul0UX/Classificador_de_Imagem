from PIL import Image
import io
import base64
import requests
from app.config import API_KEY, BASE_URL

def analisar_imagem(imagem_bytes, pergunta):
    if not API_KEY:
        return "❌ Erro: API_KEY não encontrada no .env"

    img = Image.open(io.BytesIO(imagem_bytes)).convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    imagem_jpeg = buffer.getvalue()

    imagem_base64 = base64.b64encode(imagem_jpeg).decode()

    prompt = pergunta if pergunta.strip() else "Descreva a imagem de forma técnica."

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": imagem_base64
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(BASE_URL, json=payload)
    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return f"Erro ao analisar imagem: {data}"
