from PIL import Image
import io
import base64
import requests
from app.config import API_KEY, BASE_URL

def analisar_imagem(imagem_bytes, pergunta):
    """
    Analisa uma imagem usando a API do Gemini.
    
    Args:
        imagem_bytes: Bytes da imagem
        pergunta: Pergunta do usuário sobre a imagem
    
    Returns:
        str: Resposta da IA
    """
    if not API_KEY:
        raise ValueError("API_KEY não encontrada. Verifique o arquivo .env")

    try:
        # Processar imagem com MAIOR QUALIDADE
        img = Image.open(io.BytesIO(imagem_bytes))
        
        # Converter para RGB se necessário
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar apenas se a imagem for MUITO grande (> 4096px)
        max_size = 4096
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Salvar com ALTA QUALIDADE
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=95, optimize=False)
        imagem_jpeg = buffer.getvalue()

        # Converter para base64
        imagem_base64 = base64.b64encode(imagem_jpeg).decode()

        # Preparar prompt - melhorado para análise mais precisa
        if pergunta.strip():
            prompt = f"{pergunta.strip()}\n\nPor favor, seja preciso e detalhado na análise."
        else:
            prompt = "Descreva esta imagem em detalhes, sendo preciso em quantidades e características."

        # Payload para a API
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
            ],
            "generationConfig": {
                "temperature": 0.4,  # Mais baixo = mais preciso
                "maxOutputTokens": 2048,
                "topP": 0.8,
                "topK": 40
            }
        }

        # Fazer requisição
        response = requests.post(
            BASE_URL,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()

        # Extrair resposta
        return data["candidates"][0]["content"]["parts"][0]["text"]
        
    except requests.exceptions.Timeout:
        raise Exception("A requisição demorou muito tempo. Tente novamente.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro na comunicação com a API: {str(e)}")
    except KeyError:
        raise Exception("Formato de resposta inesperado da API.")
    except Exception as e:
        raise Exception(f"Erro ao processar imagem: {str(e)}")