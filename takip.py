"""
Trendyol Fiyat Takip Botu
-------------------------
Verilen bir Trendyol ürün linkinin fiyatını belirli aralıklarla kontrol eder.
Fiyat, belirlediğin eşiğin altına inerse seni uyarır.

ÖNEMLİ: Bu bot SADECE fiyatı takip edip haber verir.
Otomatik satın alma / ödeme YAPMAZ. Kararı sen verirsin.

Kullanım:
    python takip.py "<urun_linki>" <esik_fiyat> [kontrol_araligi_dakika]

Örnek:
    python takip.py "https://www.trendyol.com/...-p-123456" 500 30
"""

import sys
import re
import json
import time
from datetime import datetime

import requests

BASLIK = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}


def fiyat_al(url: str):
    """Trendyol ürün sayfasından güncel fiyatı (TL) döndürür."""
    yanit = requests.get(url, headers=BASLIK, timeout=20)
    yanit.raise_for_status()
    html = yanit.text

    # 1. Yöntem: sayfadaki JSON verisinden fiyatı çek
    eslesme = re.search(r'"sellingPrice":\s*{\s*"value":\s*([\d.]+)', html)
    if eslesme:
        return float(eslesme.group(1))

    # 2. Yöntem: JSON-LD içinden fiyat
    for blok in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            veri = json.loads(blok)
        except json.JSONDecodeError:
            continue
        teklif = veri.get("offers") if isinstance(veri, dict) else None
        if isinstance(teklif, dict) and teklif.get("price"):
            return float(teklif["price"])

    raise ValueError("Fiyat sayfada bulunamadı. Link doğru mu?")


def bildirim(baslik: str, mesaj: str):
    """Masaüstü bildirimi dener; olmazsa ekrana yazar."""
    try:
        from plyer import notification
        notification.notify(title=baslik, message=mesaj, timeout=10)
    except Exception:
        pass
    print(f"\n🔔 {baslik}\n   {mesaj}\n")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]
    esik = float(sys.argv[2])
    aralik_dk = float(sys.argv[3]) if len(sys.argv) > 3 else 30

    print("🛒 Trendyol Fiyat Takip Botu başladı")
    print(f"   Eşik fiyat : {esik:.2f} TL")
    print(f"   Kontrol    : her {aralik_dk:.0f} dakikada bir")
    print("   (Durdurmak için Ctrl+C)\n")

    while True:
        saat = datetime.now().strftime("%H:%M")
        try:
            fiyat = fiyat_al(url)
            if fiyat <= esik:
                bildirim(
                    "Fiyat düştü! 🎉",
                    f"Ürün {fiyat:.2f} TL (eşik {esik:.2f} TL). Satın almak ister misin?",
                )
                print(f"[{saat}] {fiyat:.2f} TL  ✅ eşiğin altında — takip durduruldu.")
                break
            print(f"[{saat}] {fiyat:.2f} TL  (eşik {esik:.2f} TL) — bekleniyor...")
        except Exception as hata:
            print(f"[{saat}] Hata: {hata}")

        time.sleep(aralik_dk * 60)


if __name__ == "__main__":
    main()
