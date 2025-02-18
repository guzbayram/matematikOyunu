# Matematik Oyunu

İlkokul ve ortaokul öğrencileri için eğlenceli bir matematik öğrenme platformu.

## Özellikler

- 🎮 3 Farklı Oyun Modu:
  - Çarpım Tablosu
  - Hızlı Matematik
  - Alıştırma Modu
- 👤 Kullanıcı Profili
- 🏆 Başarı Rozetleri
- 📊 Detaylı İstatistikler
- 🎯 İlerleme Takibi

## Teknolojiler

- Django 5.1.6
- Python 3.12
- Bootstrap 5
- SQLite3

## Kurulum

1. Repository'yi klonlayın:

```bash
git clone https://github.com/yourusername/matematikOyunu.git
cd matematikOyunu
```

2. Virtual environment oluşturun ve aktif edin:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

4. Veritabanını oluşturun:

```bash
python manage.py migrate
```

5. Sunucuyu başlatın:

```bash
python manage.py runserver
```

6. Tarayıcınızda http://127.0.0.1:8000 adresine gidin

## Kullanım

1. Kayıt olun veya giriş yapın
2. Ana sayfadan bir oyun modu seçin
3. Zorluk seviyesini belirleyin
4. Oyunu başlatın ve soruları cevaplayın
5. Profilinizden ilerlemenizi takip edin

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch'i oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Detaylar'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
