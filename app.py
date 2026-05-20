import os
import re
import time
from flask import Flask, render_template, request, jsonify
from pydantic import BaseModel, ValidationError
from typing import List
from mistralai.client import Mistral

app = Flask(__name__)

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())
client = Mistral(api_key=MISTRAL_API_KEY)

SISTEM_PROMPTU = """You are a dark gothic storyteller. Always output valid JSON. Write in Turkish. Do not produce excessive violence, sexual content or hate content. muhtemelAksiyonlar must always contain exactly 3 items (empty list if story ends). oldu field should be true when story irreversibly ends. Only return JSON, nothing else."""

class BaslangicCiktisi(BaseModel):
    karakterAdi: str
    karakterArkaplan: str
    karakterDt: str
    muhtemelAksiyonlar: List[str]
    olaylar: str

class DevamCiktisi(BaseModel):
    muhtemelAksiyonlar: List[str]
    olaylar: str
    oldu: bool

def mistral_json_parse(response_text: str, model_class):
    text = response_text.strip()
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    try:
        return model_class.model_validate_json(text)
    except ValidationError as e:
        raise ValueError("JSON parse hatasi: " + str(e))

KARAKTER_PROMPTLARI = {
    "vampir": "Bir vampir karakteri olustur ve asagidaki JSON formatinda dondur (sadece JSON, baska sey yazma):\n{\n  \"karakterAdi\": \"karakterin tam adi ve lakabi\",\n  \"karakterArkaplan\": \"3-4 cumle karakter gecmisi\",\n  \"karakterDt\": \"dogum yili veya Bilinmiyor\",\n  \"muhtemelAksiyonlar\": [\"aksiyon 1\", \"aksiyon 2\", \"aksiyon 3\"],\n  \"olaylar\": \"ilk sahne aciklamasi\"\n}",
    "dedektif": "Bir dedektif karakteri olustur: 1920'ler Istanbul, paranormal vakalar cozen yorgun dedektif. Asagidaki JSON formatinda dondur (sadece JSON, baska sey yazma):\n{\n  \"karakterAdi\": \"karakterin tam adi ve lakabi\",\n  \"karakterArkaplan\": \"3-4 cumle karakter gecmisi\",\n  \"karakterDt\": \"dogum yili veya Bilinmiyor\",\n  \"muhtemelAksiyonlar\": [\"aksiyon 1\", \"aksiyon 2\", \"aksiyon 3\"],\n  \"olaylar\": \"ilk sahne aciklamasi\"\n}",
    "cadi": "Bir buyucu karakteri olustur: Anadolu daglarinda yasayan, dogayla baglantili guclu bir cadi. Asagidaki JSON formatinda dondur (sadece JSON, baska sey yazma):\n{\n  \"karakterAdi\": \"karakterin tam adi ve lakabi\",\n  \"karakterArkaplan\": \"3-4 cumle karakter gecmisi\",\n  \"karakterDt\": \"dogum yili veya Bilinmiyor\",\n  \"muhtemelAksiyonlar\": [\"aksiyon 1\", \"aksiyon 2\", \"aksiyon 3\"],\n  \"olaylar\": \"ilk sahne aciklamasi\"\n}",
    "hayalet": "Bir hayalet karakteri olustur: anilarini kaybetmis, dunyaya bagli kalmis huzursuz ruh. Asagidaki JSON formatinda dondur (sadece JSON, baska sey yazma):\n{\n  \"karakterAdi\": \"karakterin tam adi ve lakabi\",\n  \"karakterArkaplan\": \"3-4 cumle karakter gecmisi\",\n  \"karakterDt\": \"dogum yili veya Bilinmiyor\",\n  \"muhtemelAksiyonlar\": [\"aksiyon 1\", \"aksiyon 2\", \"aksiyon 3\"],\n  \"olaylar\": \"ilk sahne aciklamasi\"\n}"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start():
    try:
        data = request.get_json()
        karakter_turu = data.get("karakterTuru")
        if karakter_turu not in KARAKTER_PROMPTLARI:
            return jsonify({"error": "Gecersiz karakter turu"}), 400
        print("[BASLAT] Karakter turu:", karakter_turu)
        time.sleep(1)
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": SISTEM_PROMPTU},
                {"role": "user", "content": KARAKTER_PROMPTLARI[karakter_turu]}
            ]
        )
        result = mistral_json_parse(response.choices[0].message.content, BaslangicCiktisi)
        print("[BASLAT] Basarili:", result.karakterAdi)
        return jsonify(result.model_dump())
    except Exception as e:
        print("[HATA] Baslatma hatasi:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/api/action", methods=["POST"])
def action():
    try:
        data = request.get_json()
        aksiyonu = data.get("aksiyonu")
        hikaye_metni = data.get("hikayeMetni")
        if not aksiyonu or not hikaye_metni:
            return jsonify({"error": "aksiyonu ve hikayeMetni alanlari gerekli"}), 400
        print("[AKSIYON] Secilen aksiyon:", aksiyonu[:50])
        time.sleep(1)
        hikaye_kisaltilmis = hikaye_metni[-4000:] if len(hikaye_metni) > 4000 else hikaye_metni
        prompt = "Simdiye kadar olan hikaye:\n" + hikaye_kisaltilmis + "\n\nSecilen aksiyon: " + aksiyonu + "\n\nAsagidaki JSON formatinda dondur (sadece JSON, baska sey yazma):\n{\n  \"muhtemelAksiyonlar\": [\"aksiyon 1\", \"aksiyon 2\", \"aksiyon 3\"],\n  \"olaylar\": \"Aksiyonun sonucu ve yeni sahne\",\n  \"oldu\": false\n}"
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": SISTEM_PROMPTU},
                {"role": "user", "content": prompt}
            ]
        )
        result = mistral_json_parse(response.choices[0].message.content, DevamCiktisi)
        print("[AKSIYON] Basarili:", result.olaylar[:50], "| Oldu:", result.oldu)
        return jsonify(result.model_dump())
    except Exception as e:
        print("[HATA] Aksiyon hatasi:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug_mode)
