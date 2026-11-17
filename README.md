# 🛒 Trendyol Fiyat Takip Botu

Bir Trendyol ürününün fiyatını düzenli olarak kontrol eder ve fiyat, belirlediğin
eşiğin **altına inince seni uyarır**. Böylece indirimi kaçırmazsın.

> ⚠️ **Not:** Bu bot yalnızca fiyatı takip eder ve haber verir.
> Otomatik satın alma veya ödeme **yapmaz** — son kararı her zaman sen verirsin.
> (Otomatik satın alma hem site kurallarına aykırıdır hem de yanlış bir alışverişe yol açabilir.)

## ✨ Özellikler

- 🔗 Ürün linkinden güncel fiyatı otomatik okur
- 🎯 Belirlediğin eşik fiyatla karşılaştırır
- ⏱️ İstediğin aralıkta (dakika) tekrar tekrar kontrol eder
- 🔔 Fiyat düşünce masaüstü bildirimi + ekran uyarısı verir

## 🛠️ Kullanılan Teknolojiler

- Python 3
- `requests` (sayfa verisini almak için)
- `plyer` (masaüstü bildirimi — isteğe bağlı)

## 🚀 Kurulum

```bash
pip install -r requirements.txt
```

## ▶️ Kullanım

```bash
python takip.py "<urun_linki>" <esik_fiyat> [kontrol_araligi_dakika]
```

Örnek — ürün 500 TL altına inince, 30 dakikada bir kontrol:

```bash
python takip.py "https://www.trendyol.com/...-p-123456" 500 30
```

Durdurmak için `Ctrl+C`.

---

💚 Berra Hilal tarafından geliştirildi.
