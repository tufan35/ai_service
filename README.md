# AI Service - Çok Modelli Metin Üretme API'si

Bu proje, farklı AI modellerini kullanarak metin üretimi yapabilen bir REST API servisidir.

## Özellikler

- İki güçlü AI model desteği:
  - Mistral-7B-Instruct-v0.2
  - Mixtral-8x7B-Instruct-v0.1
- Türkçe dil desteği
- FastAPI tabanlı modern API
- Otomatik dil algılama
- Özelleştirilebilir model parametreleri

## Gereksinimler

- Python 3.9+
- pip (Python paket yöneticisi)

## Kurulum

1. Projeyi klonlayın:
```bash
git clone [repository-url]
cd ai_service
```

2. Python sanal ortamı oluşturun:
```bash
python3 -m venv .venv
```

3. Sanal ortamı aktifleştirin:
```bash
# MacOS/Linux
source .venv/bin/activate

# Windows
.\venv\Scripts\activate
```

4. Projenin ana dizinine gidin:
```bash
cd /path/to/ai_service
```

5. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

6. `.env` dosyasını oluşturun ve gerekli değişkenleri ekleyin:
```bash
# .env dosyası örneği
HUGGINGFACE_TOKEN=your_token_here
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY_ID=your_key_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
```

7. Uygulamayı çalıştırın:
```bash
python3 main.py
```

Not: Uygulama varsayılan olarak 8083 portunda çalışacaktır.

## Çalıştırma

Projeyi başlatmak için:
```bash
python3 main.py
```

Servis varsayılan olarak http://localhost:8082 adresinde çalışacaktır.

## API Kullanımı

### Mevcut Modelleri Listeleme
```bash
curl http://localhost:8082/api/v1/models
```

### Mistral ile Metin Üretme
```bash
curl -X POST http://localhost:8082/api/v1/mistral \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": "Yapay zeka nedir?",
           "parameters": {
               "temperature": 0.7,
               "max_length": 200
           }
         }'
```

### Mixtral ile Metin Üretme
```bash
curl -X POST http://localhost:8082/api/v1/mixtral \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": "Python programlama dili nedir?",
           "parameters": {
               "temperature": 0.7,
               "max_length": 200
           }
         }'
```

### Parametre Açıklamaları

- `temperature`: (0.0 - 1.0) Yüksek değerler daha yaratıcı, düşük değerler daha tutarlı yanıtlar üretir
- `max_length`: Üretilecek maksimum token sayısı
- `top_p`: (0.0 - 1.0) Nucleus sampling için olasılık eşiği
- `top_k`: Seçilecek en olası token sayısı
- `repetition_penalty`: Tekrarları önlemek için ceza faktörü

## API Dökümantasyonu

Swagger UI dökümantasyonuna erişmek için:
```
http://localhost:8082/docs
```

## Hata Ayıklama

1. Port hatası alırsanız:
   - `app/main.py` dosyasında port numarasını değiştirin
   - Örneğin: `port=8083` olarak değiştirip tekrar deneyin

2. Token hatası alırsanız:
   - HuggingFace token'ınızın doğru olduğundan emin olun
   - `.env` dosyasının doğru konumda olduğunu kontrol edin
   - Token'ı yeniden oluşturmayı deneyin

## Güvenlik Notları

- `.env` dosyasını asla git repository'sine eklemeyin
- HuggingFace token'ınızı güvende tutun
- Üretim ortamında CORS ayarlarını güvenli bir şekilde yapılandırın
