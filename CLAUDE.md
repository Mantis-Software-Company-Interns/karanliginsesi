# CLAUDE.md — Karanlığın Sesi: Proje Geliştirme Planı

## Proje Özeti

**Karanlığın Sesi**, gotik temalı, Türkçe, yapay zeka destekli bir web tabanlı rol yapma oyunudur. Kullanıcı 4 karakter arasından birini seçer; Mistral AI her aksiyondan sonra dinamik hikaye üretir. Flask REST API backend, saf HTML/CSS/JS frontend kullanılır.

---

## Teknoloji Yığını

| Katman    | Teknoloji                     |
|-----------|-------------------------------|
| Backend   | Python 3.10+, Flask 3.1.0     |
| AI        | Mistral AI API (`mistral-small-latest`) |
| Şema      | Pydantic 2.x                  |
| Frontend  | Saf HTML5 / CSS3 / JavaScript |
| Env       | python-dotenv                 |

---

## Dosya Yapısı

```
karanlığın-sesi/
├── app.py
├── requirements.txt
├── .env                   # MISTRAL_API_KEY buraya
├── .env.example
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── game.js
```

---

## Geliştirme Aşamaları ve Promptlar

Her prompt, Claude Code veya Claude'a sırayla verilmelidir. Bir adım tamamlanmadan sonraki adıma geçme.

---

### ADIM 1 — Proje İskeleti ve Bağımlılıklar

**Prompt:**
```
Karanlığın Sesi adlı Flask projesi için temel dosya iskeletini oluştur.

Gereksinimler:
- requirements.txt oluştur: flask==3.1.0, mistralai>=1.2.5, pydantic>=2.0, python-dotenv
- .env.example dosyası oluştur: MISTRAL_API_KEY=your_key_here
- app.py içinde Flask uygulamasını başlat, sadece "/" GET endpoint'i index.html döndürsün
- templates/index.html içine placeholder bir HTML5 sayfası koy (başlık: Karanlığın Sesi)
- static/css/style.css ve static/js/game.js dosyalarını boş oluştur
- Tüm dosyalar UTF-8 encoding kullanmalı

Herhangi bir oyun mantığı ekleme, sadece çalışan bir Flask uygulaması iskeleti yeterli.
```

---

### ADIM 2 — Pydantic Şemaları ve Mistral Entegrasyonu

**Prompt:**
```
app.py dosyasına Pydantic şemalarını ve Mistral AI entegrasyonunu ekle.

Gereksinimler:

1. Pydantic modelleri (app.py içinde tanımla):

class BaslangicCiktisi(BaseModel):
    karakterAdi: str        # Karakterin tam adı ve lakabı
    karakterArkaplan: str   # 3-4 cümle karakter geçmişi
    karakterDt: str         # Doğum yılı veya 'Bilinmiyor'
    muhtemelAksiyonlar: List[str]  # Tam olarak 3 aksiyon seçeneği
    olaylar: str            # İlk sahne açıklaması

class DevamCiktisi(BaseModel):
    muhtemelAksiyonlar: List[str]  # Sonraki 3 aksiyon (son ise boş liste)
    olaylar: str            # Aksiyonun sonucu ve yeni sahne
    oldu: bool              # Hikaye sona erdiyse True

2. Mistral istemcisi:
- python-dotenv ile MISTRAL_API_KEY'i .env'den yükle
- mistralai kütüphanesi ile client oluştur
- Model: "mistral-small-latest"

3. Yardımcı fonksiyon: mistral_json_parse(response_text, model_class)
- Mistral'dan gelen ham metni alır
- Pydantic model ile parse eder
- Hata durumunda ValueError fırlatır

4. Sistem promptu sabiti (SISTEM_PROMPTU):
Türkçe gotik tema için sistem promptu yaz. Mistral'a şunu söyle:
- Sen karanlık gotik bir hikaye anlatıcısısın
- Çıktılarını her zaman geçerli JSON formatında ver
- Türkçe yaz
- Aşırı şiddet, cinsellik ve nefret içeriği üretme
- muhtemelAksiyonlar her zaman tam olarak 3 eleman içermeli (hikaye bitmişse boş liste)
- oldu alanı hikaye geri dönüşsüz sona erdiğinde true olmalı

Henüz endpoint ekleme, sadece şemaları ve Mistral bağlantısını kur.
```

---

### ADIM 3 — Backend API Endpoint'leri

**Prompt:**
```
app.py dosyasına iki REST API endpoint'i ekle:

--- ENDPOINT 1: POST /api/start ---

Girdi (JSON body):
{ "karakterTuru": "vampir" }  # vampir | dedektif | cadı | hayalet

İşlem:
1. karakterTuru değerini al ve doğrula (geçersiz türse 400 döndür)
2. Her karakter türü için özelleştirilmiş prompt oluştur:
   - vampir: Bin yıllık, soğuk, aristokrat, Osmanlı dönemi arkaplanı
   - dedektif: 1920'ler İstanbul'u, paranormal vakalar çözen yorgun dedektif  
   - cadı: Anadolu'nun dağlarında yaşayan, doğayla bağlantılı güçlü büyücü
   - hayalet: Anılarını kaybetmiş, dünyaya bağlı kalmış huzursuz ruh
3. Mistral'a BaslangicCiktisi şemasına uygun JSON üretmesini söyle
4. Yanıtı parse et ve JSON olarak döndür
5. API hatası durumunda 500 ve {"error": "açıklama"} döndür

--- ENDPOINT 2: POST /api/action ---

Girdi (JSON body):
{
  "aksiyonu": "seçilen aksiyon metni",
  "hikayeMetni": "şimdiye kadar yaşanan tüm olay örgüsü"
}

İşlem:
1. Her iki alanı doğrula
2. hikayeMetni + aksiyonu birleştirerek Mistral'a gönder
3. DevamCiktisi şemasına uygun JSON iste
4. oldu: true gelirse muhtemelAksiyonlar boş liste olabilir
5. Yanıtı parse et ve JSON olarak döndür
6. Hata durumunda 500 döndür

--- CORS ve Genel ---
- Flask-CORS gerekmez (aynı origin)
- Her endpoint için try/except ile hata yönetimi
- Rate limit için istekler arasında 1 saniye sleep ekle (time.sleep(1))
- Tüm loglar Türkçe olsun: print("[BAŞLAT]", "[AKSİYON]", "[HATA]" vb.
```

---

### ADIM 4 — Frontend HTML Yapısı

**Prompt:**
```
templates/index.html dosyasını oluştur. Flask Jinja2 şablonu olarak hazırla.

Uygulama 3 ekran/görünümden oluşuyor. Hepsi aynı HTML dosyasında olacak, JS ile göster/gizle yapılacak:

--- EKRAN 1: Karakter Seçim Ekranı (id="karakter-secim-ekrani") ---
- Büyük başlık: "Karanlığın Sesi"
- Alt başlık: "Hangi karanlığı seçersin?"
- 4 karakter kartı (CSS Grid, 2x2 veya 1x4):
  - data-tur="vampir" | ikon/emoji: 🧛 | isim: "Vampir" | kısa açıklama
  - data-tur="dedektif" | ikon: 🔍 | isim: "Dedektif" | kısa açıklama
  - data-tur="cadi" | ikon: 🧙‍♀️ | isim: "Cadı" | kısa açıklama  
  - data-tur="hayalet" | ikon: 👻 | isim: "Hayalet" | kısa açıklama

--- EKRAN 2: Oyun Ekranı (id="oyun-ekrani", başta gizli) ---
Üst kısım - Karakter Bilgi Paneli:
  - id="karakter-adi" (karakter adı)
  - id="karakter-arkaplan" (arkaplan metni)
  - id="karakter-dt" (doğum tarihi)

Orta kısım - Hikaye Kutusu:
  - id="hikaye-kutusu" (scrollable, sahneler birikir)
  - id="yukleniyor-gostergesi" (başta gizli, yükleme animasyonu)

Alt kısım - Aksiyon Butonları:
  - id="aksiyonlar-konteyner"
  - 3 adet buton: id="aksiyon-btn-0", "aksiyon-btn-1", "aksiyon-btn-2"

--- EKRAN 3: Ölüm Ekranı (id="olum-ekrani", başta gizli) ---
- Başlık: "Karanlık Seni Yuttu"
- Son sahne özeti alanı: id="son-sahne"
- Buton: id="yeniden-basla-btn" | metin: "Yeniden Uyan"

--- Genel ---
- static/css/style.css ve static/js/game.js dosyalarını link/script ile bağla
- Viewport meta tag ekle
- charset UTF-8
- Türkçe lang="tr"
```

---

### ADIM 5 — Frontend Oyun Mantığı (JavaScript)

**Prompt:**
```
static/js/game.js dosyasını yaz. Saf JavaScript kullan, hiçbir harici kütüphane olmadan.

State yönetimi için bir nesne kullan:
const oyunDurumu = {
  karakterTuru: null,
  karakterAdi: null,
  hikayeMetni: "",   // Tüm sahne metinleri birikiyor
  aktif: false
};

--- FONKSİYONLAR ---

1. ekranGoster(ekranId)
   - "karakter-secim-ekrani", "oyun-ekrani", "olum-ekrani" arasında geçiş
   - Diğer ekranları gizle, seçileni göster

2. yukleniyorGoster(durum: boolean)
   - Yükleniyor göstergesini göster/gizle
   - Aksiyon butonlarını enable/disable et

3. sahneEkle(metin)
   - hikaye-kutusu div'ine yeni paragraf ekle
   - Kutuyu en alta scroll et
   - hikayeMetni state'ine de ekle (olay örgüsü birikimi için)

4. aksiyonlarGuncelle(aksiyonlar: string[])
   - 3 aksiyon butonuna yeni metinleri yaz
   - Butonları aktif et

5. karakterSec(tur)
   - yukleniyorGoster(true)
   - fetch POST /api/start ile { karakterTuru: tur } gönder
   - Başarıda: BaslangicCiktisi parse et, oyun ekranını doldur, ekranGoster("oyun-ekrani")
   - Hata: alert ile Türkçe hata mesajı göster
   - finally: yukleniyorGoster(false)

6. aksiyonSec(aksiyonMetni)
   - yukleniyorGoster(true)
   - sahneEkle("→ " + aksiyonMetni)  // Seçilen aksiyonu hikayeye ekle
   - fetch POST /api/action ile { aksiyonu, hikayeMetni } gönder
   - Başarıda DevamCiktisi parse et:
     - sahneEkle(olaylar)
     - oldu true ise: son-sahne'yi doldur, ekranGoster("olum-ekrani")
     - oldu false ise: aksiyonlarGuncelle(muhtemelAksiyonlar)
   - Hata: hikaye-kutusu'na hata mesajı ekle
   - finally: yukleniyorGoster(false)

7. yenidenBasla()
   - oyunDurumu sıfırla
   - hikaye-kutusu'nu temizle
   - ekranGoster("karakter-secim-ekrani")

--- EVENT LISTENER'LAR ---
- DOMContentLoaded içinde:
  - Her karakter kartına click: karakterSec(card.dataset.tur)
  - Her aksiyon butonuna click: aksiyonSec(btn.textContent)
  - yeniden-basla-btn click: yenidenBasla()

--- HATA YÖNETİMİ ---
- Tüm fetch çağrıları try/catch ile sarılmalı
- HTTP hata kodu kontrolü: response.ok değilse hata fırlat
- Yükleme sırasında karakter kartlarına tıklanmasını engelle
```

---

### ADIM 6 — Gotik Tema CSS Tasarımı

**Prompt:**
```
static/css/style.css dosyasını yaz. Koyu gotik tema, saf CSS.

Renk Paleti (CSS değişkenleri):
--bg-ana: #0a0608          /* Derin siyah-mor */
--bg-panel: #12080f         /* Karanlık panel */
--bg-kart: #1a0d17          /* Kart arka planı */
--kirmizi: #8b0000          /* Kan kırmızısı */
--kirmizi-parlak: #c41e1e    /* Hover kırmızısı */
--gold: #c9a84c             /* Antik altın */
--metin-ana: #e8dcc8        /* Soluk krem */
--metin-ikincil: #9a8a7a    /* Gri-bej */
--sinir: #3d1f2d            /* Karanlık mor sınır */

Tipografi:
- Google Fonts: "Cinzel" (başlıklar, gotik serif) + "IM Fell English" (hikaye metni)
- Fallback: serif

Genel:
- body: bg-ana, min-height 100vh, overflow-x hidden
- Tüm ekranlar: width 100%, max-width 900px, margin auto

--- EKRAN 1 - Karakter Seçim ---
- Büyük "Karanlığın Sesi" başlığı: Cinzel font, gold renk, text-shadow kırmızı
- Alt başlık: IM Fell English, metin-ikincil
- Karakter kartları: CSS Grid 2x2, hover'da kırmızı border glow efekti
- Her kart: bg-kart, sinir border, padding, cursor pointer
- Kart ikon: büyük font-size (3rem)
- Kart isim: Cinzel, gold
- Kart açıklama: IM Fell English, metin-ikincil, küçük font
- Hover: bg daha açık, box-shadow kırmızı

--- EKRAN 2 - Oyun ---
- Karakter bilgi paneli: bg-panel, gold border-bottom, flex layout
- Hikaye kutusu: min-height 300px, max-height 450px, overflow-y auto, IM Fell English
- Her yeni sahne paragrafı: metin-ana, margin-bottom
- "→ aksiyon" satırları: gold renk, italic
- Yükleniyor göstergesi: pulsating nokta animasyonu (CSS keyframes), kırmızı renk
- Aksiyon butonları: bg-kart, gold border, metin-ana, hover'da bg-kirmizi
- Buton disabled: opacity 0.4, cursor not-allowed

--- EKRAN 3 - Ölüm ---
- Tam ekran karanlık overlay
- Büyük "Karanlık Seni Yuttu" başlığı: Cinzel, kırmızı, büyük
- Yeniden Uyan butonu: gold border, kırmızı bg, hover parlak

--- GENEL ---
- Scrollbar özelleştirme (webkit): ince, kırmızı thumb, karanlık track
- Tüm geçişler: transition 0.3s ease
- Responsive: max-width ile mobil uyumlu temel düzen
- CSS animasyonu: fadeIn (yeni sahneler için)
```

---

### ADIM 7 — Test ve Hata Düzeltme

**Prompt:**
```
Karanlığın Sesi projesini uçtan uca test et ve eksikleri düzelt.

Test senaryoları:

1. BACKEND TEST:
   - Flask sunucusu başlıyor mu? (python app.py)
   - /api/start POST ile {"karakterTuru": "vampir"} gönder
   - Dönen JSON'da karakterAdi, karakterArkaplan, karakterDt, muhtemelAksiyonlar (3 eleman), olaylar var mı?
   - /api/action POST ile {"aksiyonu": "...", "hikayeMetni": "..."} gönder
   - Dönen JSON'da muhtemelAksiyonlar, olaylar, oldu var mı?
   - Geçersiz karakterTuru gönderildiğinde 400 dönüyor mu?

2. FRONTEND TEST:
   - Karakter seçim ekranı açılıyor mu?
   - Bir kartı tıkladığında yükleniyor göstergesi çıkıyor mu?
   - Oyun ekranına geçiş doğru mu?
   - 3 aksiyon butonu görünüyor mu?
   - Bir aksiyon seçildiğinde hikaye birikip güncellenıyor mu?
   - Scrollbar en alta gidiyor mu?
   - oldu:true geldiğinde ölüm ekranı açılıyor mu?
   - Yeniden Uyan butonu karakter seçime dönüyor mu?

3. DÜZELT:
   - Bulunan hataları düzelt
   - Eğer Mistral JSON parse hatası veriyorsa: response_format parametresi veya prompt'a "Sadece JSON döndür, başka hiçbir şey yazma" ekle
   - Eğer CORS hatası varsa: Flask-CORS ekle
   - hikayeMetni çok uzarsa Mistral token limitine takılabilir; son 3000 karakteri kes

Sonunda çalışır durumdaki tüm dosyaları listele.
```

---

### ADIM 8 — Son Rötuşlar ve Deployment Hazırlığı

**Prompt:**
```
Karanlığın Sesi projesine son rötuşları yap:

1. README.md oluştur:
   - Türkçe, projeyi açıkla
   - Kurulum adımları: pip install -r requirements.txt, .env ayarı, python app.py
   - Kısa ekran görüntüsü açıklaması

2. .gitignore ekle:
   - .env
   - __pycache__/
   - *.pyc
   - venv/

3. app.py'de güvenlik:
   - debug=False production için (veya env variable'dan oku)
   - SECRET_KEY ekle (rastgele, env'den oku)

4. Performans:
   - Hikaye metni 4000 karakteri aşarsa son 4000 karakteri al (Mistral token limiti)
   - Yükleniyor sırasında tüm etkileşimleri engelle (karakter kartları dahil)

5. UX iyileştirmeleri:
   - Oyun ekranında karakter adını sayfa title'ına yaz: <title>Karanlığın Sesi — {karakterAdi}</title>
   - Hata mesajlarını kullanıcı dostu Türkçe yap
   - Aksiyon butonlarının üzerine gelindiğinde tooltip/title ekle

Tüm dosyaları gözden geçir ve tutarlılığı kontrol et.
```

---

## Önemli Notlar

### Mistral JSON Çıktısı
Mistral bazen ham JSON yerine markdown code block içinde JSON döndürebilir. `mistral_json_parse` fonksiyonu şunu yapmalı:
```python
import re, json
text = response.strip()
# ```json ... ``` bloğunu temizle
text = re.sub(r"```json\s*", "", text)
text = re.sub(r"```\s*", "", text)
return ModelClass.model_validate_json(text)
```

### Rate Limit
Mistral ücretsiz planında dakikada ~5-10 istek sınırı vardır. Her API çağrısından önce `time.sleep(1)` ekle. Hata `429` gelirse kullanıcıya "Lütfen birkaç saniye bekleyin" mesajı göster.

### Python Versiyonu
SRS'de belirtildiği üzere Python 3.14 ile bağımlılık uyumsuzluğu var. Python 3.10 veya 3.11 önerilir.

### Olay Örgüsü Birikimi
`hikayeMetni` her aksiyonda büyür. Mistral'a gönderirken son 4000 karakteri kullan:
```python
hikaye_kisaltilmis = hikaye_metni[-4000:] if len(hikaye_metni) > 4000 else hikaye_metni
```

---

## Hızlı Başlangıç Komutu Sırası

```bash
# 1. Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Bağımlılıkları kur
pip install -r requirements.txt

# 3. API anahtarını ayarla
cp .env.example .env
# .env dosyasını aç ve MISTRAL_API_KEY değerini gir

# 4. Uygulamayı başlat
python app.py

# 5. Tarayıcıda aç
# http://localhost:5000
```
