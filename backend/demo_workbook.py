# -*- coding: utf-8 -*-
"""Generate a small fictional workbook for demonstrating the import workflow."""

from datetime import date, timedelta
from pathlib import Path
import sys

from openpyxl import Workbook


HEADERS = [
    "Sıra No",
    "Defter Sıra No",
    "Yılı (2017-2021)",
    "İlin Adı (Sorumlu Teşkilat)",
    "HUKUKİ DAYANAK",
    "ÖLÇÜ ALETİ SAYISI",
    "ÖLÇÜ ALETİ CİNSİ",
    None,
    "TABLET TUTANAK NUMARASI",
    "Cezanın Muhatabı (Kişi/ Firma Adı)",
    "Cezanın Onay Tarihi (Kararın Verildiği Tarih, İYK Tarihi)",
    "Verilen Cezanın Tutarı (TL)",
    "GÖNDERİM TÜRÜ",
    "Cezanın İlgiliye Tebliğ Tarihi",
    "Tebligat Üzerine İlgili Tarafından Doğrudan Yatırılan Tutar (TL)",
    "ödeme tarihi",
    "İtiraz Edilmeyenlerde Kesinleşme Tarihi",
    "KALAN SÜRE",
    "İtiraz Edilmeyenlerde Tahsilat İçin İlgili Vergi Dairesine Bildirim Tarihi",
    "Bildirim Yapılan Vergi Dairesinin Adı",
    "İtirazın Sonucu (Kurum Lehine/ Kurum Aleyhine)",
    "İtiraz Üzerine Kurum Lehine Sonuçlananlarda İlgili Tarafından Doğrudan Yatırılan Tutar (TL)",
    "İtiraz Üzerine Kurum Lehine Sonuçlananlarda Tahsilat İçin İlgili Vergi Dairesine Bildirim Tarihi",
    "İlgili Vergi Dairesince Tahsil Edildiği Bildirilen Tutar (TL)",
    "İlgili Vergi Dairesince Tahsil Edildiği Bildirilen Tarih",
    "Tespiti Yapan Kurum",
    "Tespit Yazısının EBYS Tarih ve Sayısı",
    "DURUMU",
]


def build_row(number, company, instrument, amount, notified_days_ago):
    notified = date.today() - timedelta(days=notified_days_ago)
    approved = notified - timedelta(days=5)
    row = [None] * len(HEADERS)
    row[0] = number
    row[1] = "Demo Personel"
    row[2] = date.today().year
    row[3] = "KOCAELİ"
    row[4] = "3516.15/c"
    row[5] = 1
    row[6] = instrument
    row[8] = f"41-DEMO{number:04d}"
    row[9] = company
    row[10] = approved
    row[11] = amount
    row[12] = "UETS"
    row[13] = notified
    row[25] = "ÖRNEK KURUM"
    row[26] = f"{approved.strftime('%d.%m.%Y')}-DEMO{number:04d}"
    return row


def main():
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "demo-ipc.xlsx")
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "İPC Bilgi Girişi"
    sheet.append(["KURGUSAL İDARİ PARA CEZASI TANITIM VERİLERİ"])
    sheet.append(HEADERS)

    rows = [
        (1, "Örnek Akaryakıt A.Ş.", "Akaryakıt Sayacı", 12500, 4),
        (2, "Demo Tartı Sistemleri Ltd. Şti.", "Taksimetre", 18000, 9),
        (3, "Test Oto Servis", "Egzoz Emisyon Cihazı", 9500, 15),
        (4, "Örnek LPG İstasyonu", "LPG Sayacı", 22000, 33),
    ]
    for values in rows:
        sheet.append(build_row(*values))

    workbook.save(output)
    print(f"Kurgusal tanıtım dosyası oluşturuldu: {output.resolve()}")


if __name__ == "__main__":
    main()
