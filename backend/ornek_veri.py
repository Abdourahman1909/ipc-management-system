# -*- coding: utf-8 -*-
"""Yalnızca kurgusal tanıtım verileri yükler: python ornek_veri.py"""
import json, os, sqlite3, random
from datetime import date, timedelta

if not os.environ.get("IPC_INITIAL_ADMIN_PASSWORD"):
    raise SystemExit(
        "Önce IPC_INITIAL_ADMIN_PASSWORD ortam değişkenini güçlü bir tanıtım "
        "parolasıyla ayarlayın."
    )

from app import init_db, DB_PATH

random.seed(2026)
init_db()
db = sqlite3.connect(DB_PATH)
firmalar = ["Örnek Akaryakıt A.Ş.", "Demo Tartı Sistemleri Ltd. Şti.",
            "Test Oto Servis", "Örnek LPG İstasyonu", "Demo Nakliyat",
            "Örnek Gıda Pazarı", "Test Taksi Kooperatifi", "Demo Kantar A.Ş."]
dayanak = ["3516.15/c", "3516.15/e", "3516.15/h", "3516.15/i"]
cins = ["Akaryakıt ve LPG Sayacı", "Taksimetre", "2. SINIF OTOMATİK OLMAYAN TARTI ALETİ",
        "Egzoz Emisyon Cihazı", "AdBlue Sayacı", "Lastik Hava Basınç Ölçer"]
vd = ["İlyasbey VD.", "Körfez VD.", "Tepecik VD.", "Yenikapı VD."]
kurum = ["İL MÜD.", "TSE", "Gebze Kalibrasyon", "Safir Servis", "Damdacı"]

for f in firmalar:
    teblig = date.today() - timedelta(days=random.choice([2, 5, 10, 13, 14, 20, 40]))
    onay = teblig - timedelta(days=7)
    d = {
        "yil": str(random.choice([2023, 2024, 2025, 2026])),
        "hukuki_dayanak": random.choice(dayanak),
        "olcu_aleti_sayisi": str(random.randint(1, 5)),
        "olcu_aleti_cinsi": random.choice(cins),
        "tablet_tutanak_no": "41-" + "".join(random.choices("ABCDEF0123456789", k=8)),
        "cezanin_muhatabi": f,
        "ceza_onay_tarihi": onay.strftime("%d.%m.%Y"),
        "ceza_tutari": str(random.choice([16000, 23900, 51000, 8400])),
        "gonderim_turu": random.choice(["ELDEN", "FİZİKİ", "UETS"]),
        "teblig_tarihi": teblig.strftime("%d.%m.%Y"),
        "dogrudan_yatirilan": "", "odeme_tarihi": "", "kesinlesme_tarihi": "",
        "vergi_bildirim_tarihi": "", "vergi_dairesi": random.choice(vd),
        "itiraz_sonucu": "", "itiraz_lehine_tutar": "",
        "itiraz_vergi_bildirim_tarihi": "",
        "tespit_kurum": random.choice(kurum),
        "ebys": f"{onay.strftime('%d.%m.%Y')}-{random.randint(1000000, 9999999)}",
    }
    db.execute("INSERT INTO companies(data,created_by) VALUES(?,?)",
               (json.dumps(d, ensure_ascii=False), "admin"))
db.commit()
db.close()
print(f"{len(firmalar)} örnek kayıt eklendi.")
