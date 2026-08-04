# -*- coding: utf-8 -*-

import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook

from importer import ImportWorkbookError, parse_workbook


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
    None,
    None,
]


def make_workbook(path, rows, headers=HEADERS):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "İPC Bilgi Girişi"
    sheet.append(["İDARİ PARA CEZALARINA İLİŞKİN TABLO"])
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    workbook.save(path)


class ImporterTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "gercek-veri.xlsx"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parses_and_preserves_unheaded_notes(self):
        row = [None] * 30
        row[0] = 1
        row[1] = "D-17"
        row[2] = 2017
        row[3] = "KOCAELİ"
        row[4] = "3516.15/C"
        row[5] = 2
        row[6] = "Taksimetre"
        row[7] = "DİKKAT"
        row[9] = "Örnek Firma"
        row[10] = datetime(2017, 2, 21)
        row[11] = "2.752,50 TL"
        row[13] = datetime(2017, 3, 3)
        row[18] = datetime(2017, 3, 20)
        row[19] = "İLYASBEY VD."
        row[25] = "TSE"
        row[26] = "01.02.2017-1234567"
        row[27] = "ÖDEMESİ YAPILDI"
        row[28] = "TEBLİGAT TARİHİ BİLİNMİYOR"
        make_workbook(self.path, [row])

        parsed = parse_workbook(self.path)

        self.assertEqual(parsed["record_count"], 1)
        self.assertEqual(parsed["source_nonempty_row_count"], 1)
        self.assertEqual(parsed["ignored_row_count"], 0)
        self.assertEqual(parsed["record_row_range"], "3")
        self.assertEqual(parsed["total_amount"], "2752.5")
        column_b = next(item for item in parsed["mapping"] if item["column"] == "B")
        self.assertEqual(column_b["source"], "Defter Sıra No")
        self.assertEqual(column_b["target"], "Sorumlu Personel")
        data = parsed["records"][0]["data"]
        self.assertEqual(data["ceza_onay_tarihi"], "21.02.2017")
        self.assertEqual(data["ceza_tutari"], "2752.5")
        self.assertEqual(
            data["olcu_aletleri"],
            [{"cinsi": "Taksimetre", "sayisi": 2}],
        )
        self.assertEqual(data["olcu_aleti_sayisi"], "2")
        self.assertEqual(data["olcu_aleti_cinsi"], "Taksimetre (2)")
        self.assertIn("H: DİKKAT", data["kaynak_notu"])
        self.assertIn("AC: TEBLİGAT TARİHİ BİLİNMİYOR", data["kaynak_notu"])

    def test_parses_multiple_instrument_type_quantity_pairs(self):
        row = [None] * 30
        row[0] = 1
        row[2] = 2026
        row[3] = "KOCAELİ"
        row[4] = "3516.15/c"
        row[5] = 5
        row[6] = "Taksimetre (3); Tanker sayacı (2)"
        row[9] = "Çoklu Alet Firması"
        row[11] = 1000
        make_workbook(self.path, [row])

        parsed = parse_workbook(self.path)

        data = parsed["records"][0]["data"]
        self.assertEqual(
            data["olcu_aletleri"],
            [
                {"cinsi": "Taksimetre", "sayisi": 3},
                {"cinsi": "Tanker sayacı", "sayisi": 2},
            ],
        )
        self.assertEqual(data["olcu_aleti_sayisi"], "5")
        self.assertEqual(
            data["olcu_aleti_cinsi"],
            "Taksimetre (3); Tanker sayacı (2)",
        )
        self.assertEqual(
            parsed["option_values"]["olcu_aleti_cinsi"],
            ["Taksimetre", "Tanker sayacı"],
        )

    def test_invalid_typed_value_is_warned_and_kept_as_note(self):
        row = [None] * 30
        row[0] = 8
        row[2] = 2021
        row[4] = "3516.15/c"
        row[9] = "Örnek Firma"
        row[11] = 2000
        row[13] = "?"
        make_workbook(self.path, [row])

        parsed = parse_workbook(self.path)

        self.assertEqual(parsed["warning_count"], 1)
        data = parsed["records"][0]["data"]
        self.assertEqual(data["teblig_tarihi"], "")
        self.assertIn("N (Cezanın İlgiliye Tebliğ Tarihi): ?", data["kaynak_notu"])

    def test_skips_prefilled_template_rows_without_business_data(self):
        real_row = [None] * 30
        real_row[0] = 1
        real_row[2] = 2026
        real_row[3] = "KOCAELİ"
        real_row[4] = "3516.15/c"
        real_row[9] = "Gerçek Firma"
        real_row[11] = 1000

        template_row = [None] * 30
        template_row[0] = 2
        template_row[2] = 2026
        template_row[3] = "KOCAELİ"
        template_row[4] = "3516.15/c"
        template_row[16] = datetime(1900, 1, 30)
        template_row[17] = -46197
        make_workbook(self.path, [real_row, template_row])

        parsed = parse_workbook(self.path)

        self.assertEqual(parsed["record_count"], 1)
        self.assertEqual(parsed["source_nonempty_row_count"], 2)
        self.assertEqual(parsed["ignored_row_count"], 1)
        self.assertEqual(parsed["template_row_count"], 1)
        self.assertEqual(parsed["rejected_row_count"], 0)
        self.assertEqual(parsed["record_row_range"], "3")
        self.assertEqual(parsed["template_row_range"], "4")
        self.assertEqual(parsed["records"][0]["sira_no"], 1)
        self.assertEqual(
            parsed["normalizations"]["Boş şablon satırı aktarılmadan atlandı"],
            1,
        )

    def test_reports_separate_ranges_for_real_and_template_rows(self):
        first_real = [None] * 30
        first_real[0] = 1
        first_real[2] = 2026
        first_real[4] = "3516.15/c"
        first_real[9] = "Birinci Firma"
        first_real[11] = 1000

        second_real = first_real.copy()
        second_real[0] = 2
        second_real[9] = "İkinci Firma"

        template_row = [None] * 30
        template_row[0] = 3
        template_row[2] = 2026
        template_row[3] = "KOCAELİ"
        template_row[4] = "3516.15/c"
        template_row[16] = datetime(1900, 1, 30)
        template_row[17] = -46197

        make_workbook(self.path, [first_real, second_real, template_row])

        parsed = parse_workbook(self.path)

        self.assertEqual(parsed["source_nonempty_row_count"], 3)
        self.assertEqual(parsed["record_count"], 2)
        self.assertEqual(parsed["template_row_count"], 1)
        self.assertEqual(parsed["record_row_range"], "3–4")
        self.assertEqual(parsed["template_row_range"], "5")

    def test_rejects_foreign_workbook(self):
        make_workbook(self.path, [[1, "x"]], headers=["Ad", "Tutar"])
        with self.assertRaises(ImportWorkbookError):
            parse_workbook(self.path)

    def test_rejects_duplicate_source_numbers(self):
        rows = []
        for _ in range(2):
            row = [None] * 30
            row[0] = 1
            row[2] = 2026
            row[4] = "3516.15/c"
            row[9] = "Örnek Firma"
            row[11] = 500
            rows.append(row)
        make_workbook(self.path, rows)
        with self.assertRaises(ImportWorkbookError):
            parse_workbook(self.path)


if __name__ == "__main__":
    unittest.main()
