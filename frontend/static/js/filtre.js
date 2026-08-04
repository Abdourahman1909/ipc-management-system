/* ============================================================
   filtre.js — çoklu filtre satırı yönetimi
   Hem "Kayıtlı Şirketleri Görüntüle" hem "Rapor Oluştur"
   sayfası bu dosyayı kullanır.
   ============================================================ */

/* Seçilen sütunun veri tipine göre örnek yazıyı (placeholder) günceller */
function filtreIpucuGuncelle(secim) {
  const satir = secim.closest(".filtre-satiri");
  const kutu  = satir.querySelector("input");
  const tip   = secim.options[secim.selectedIndex].dataset.tip || "TEXT";
  let ornek;
  if (tip.startsWith("TARİH") || tip.startsWith("DATETIME")) {
    ornek = "30.10.2024  veya  30.10.2024-02.04.2026";
  } else if (tip === "INT") {
    ornek = "2025  veya  2025-2026";
  } else if (tip === "DECIMAL" || tip === "FLOAT / DOUBLE") {
    ornek = "16000  veya  16000-51000";
  } else {
    ornek = "Aranacak değer";
  }
  kutu.placeholder = ornek;
}

/* Yeni bir filtre satırı ekler (istenildiği kadar filtre eklenebilir) */
function filtreSatiriEkle(btn) {
  const form  = btn.closest("form");
  const kap   = form.querySelector(".filtre-satirlari");
  const kopya = kap.querySelector(".filtre-satiri").cloneNode(true);
  kopya.querySelector("input").value = "";
  kopya.querySelector("select").selectedIndex = 0;
  kap.appendChild(kopya);
  filtreIpucuGuncelle(kopya.querySelector("select"));
  kopya.querySelector("input").focus();
}

/* Bir filtreyi kaldırır ve kalan filtreleri "Uygula"ya basmadan uygular */
function filtreKaldir(btn) {
  const form  = btn.closest("form");
  const kap   = form.querySelector(".filtre-satirlari");
  const satir = btn.closest(".filtre-satiri");
  if (kap.querySelectorAll(".filtre-satiri").length > 1) {
    satir.remove();
  } else {
    satir.querySelector("input").value = "";   // son satır: silmek yerine temizle
  }
  form.submit();
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".filtre-satiri select").forEach(filtreIpucuGuncelle);
  document.addEventListener("change", function (e) {
    if (e.target.matches(".filtre-satiri select")) filtreIpucuGuncelle(e.target);
  });
});
