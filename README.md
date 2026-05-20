# Karanlığın Sesi

Gotik temalı, Türkçe, yapay zeka destekli web tabanlı rol yapma oyunu. Mistral AI ile dinamik hikaye üretimi.

## Özellikler

- 4 farklı karakter: Vampir, Dedektif, Cadı, Hayalet
- Mistral AI ile dinamik hikaye ve aksiyon seçenekleri
- Gotik tema tasarım
- Saf HTML/CSS/JS frontend, Flask REST API backend

## Kurulum

```bash
# 1. Sanal ortam oluştur
python -m venv venv

# 2. Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Bağımlılıkları kur
pip install -r requirements.txt

# 4. Ortam değişkenini ayarla
# Windows PowerShell:
$env:MISTRAL_API_KEY="api-anahtariniz"
# Windows CMD:
set MISTRAL_API_KEY=api-anahtariniz
# Linux/Mac:
export MISTRAL_API_KEY="api-anahtariniz"

# 5. Uygulamayı başlat
python app.py

# 6. Tarayıcıda aç
# http://localhost:5000
```

## API Anahtarı

Mistral API anahtarı almak için: https://console.mistral.ai/

## Kullanım

1. Tarayıcıda `http://localhost:5000` adresine git
2. 4 karakterden birini seç
3. Hikayeyi takip et ve aksiyon seçeneklerinden birine tıkla
4. Hikaye sona erdiğinde "Yeniden Uyan" butonuna bas

## Teknolojiler

- **Backend:** Python, Flask 3.1.0
- **AI:** Mistral AI API (mistral-small-latest)
- **Schema:** Pydantic 2.x
- **Frontend:** Saf HTML5, CSS3, JavaScript

## Proje Yapısı

```
karanliginsesi/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── game.js
```
