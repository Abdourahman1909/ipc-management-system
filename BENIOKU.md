# İdari Para Cezaları (İPC) Yönetim Sistemi
T.C. Sanayi ve Teknoloji Bakanlığı — Kocaeli İl Müdürlüğü

> **Internship project contributors:** [Abdourahman Mohamed Ismail](AUTHORS.md), Jasmin Jandaulyet and Bokang Daniel Klaas. Full contributor and contact details are in [AUTHORS.md](AUTHORS.md).

## Proje yapısı (backend / frontend ayrımı)
```
backend/                 <- Sunucu tarafı (Python / Flask)
  app.py                 <- Tüm rotalar, veritabanı, doğrulama, PDF/Excel üretimi
  ornek_veri.py          <- Örnek veri yükleyici
  requirements.txt
  fonts/                 <- PDF'lerde Türkçe karakter için DejaVu fontları
  ipc.db                 <- (ilk çalıştırmada otomatik oluşur)
  uploads/               <- Kayıtlara eklenen belge, fotoğraf ve videolar

frontend/                <- İstemci tarafı (HTML / CSS / JS)
  templates/             <- Jinja2 HTML şablonları (sayfa başına bir dosya)
  static/
    css/style.css        <- Kurumsal tasarım sistemi ve duyarlı kayıt çalışma alanı
    css/auth.css         <- Giriş sayfaları stili (Türkiye haritalı arka plan)
    js/main.js           <- Türkçe doğrulama mesajları, toast, yükleme animasyonu
    js/dashboard.js      <- Pano grafikleri (Chart.js)
    js/sirketler.js      <- Filtre yönetimi (Kaldır -> otomatik uygula)
    js/sirket_form.js    <- Form hataları, çoklu ölçü aletleri ve dosya seçim özeti
    img/logo.png         <- Bakanlık logosu
    img/turkiye.svg      <- Dekoratif Türkiye haritası
    img/ipc-denetim-*.webp <- Ana paneldeki ölçü ve ayar denetimi görselleri
```

## Kurulum (yerel çalıştırma)
```bash
cd backend
pip install -r requirements.txt
export IPC_INITIAL_ADMIN_EMAIL="admin@example.local"
export IPC_INITIAL_ADMIN_PASSWORD="guclu-bir-tanitim-parolasi"
python app.py
```
Tarayıcıda: http://127.0.0.1:5000

İlk yönetici parolası kaynak kodunda bulunmaz. Boş veritabanının ilk
çalıştırılmasında `IPC_INITIAL_ADMIN_PASSWORD` ortam değişkeni açıkça verilmelidir.
Windows sunucu paketi bu parolayı ilk açılışta kullanıcıdan güvenli biçimde ister.

## Windows bölüm kurulumu — Python gerektirmez

Bölümde bir Windows laptop sunucu olarak çalışacak ve aynı özel ağa bağlı diğer
laptoplar tarayıcıyla bağlanacaksa, GitHub Actions tarafından üretilen
`IPC_Yonetim_Sistemi_Windows.zip` paketi kullanılmalıdır. Paket Python çalışma
ortamını ve gereken kütüphaneleri tek `.exe` içinde taşır.

Sunucu laptopta yalnızca `IPC_Yonetim_Sistemi.exe` çalıştırılır. Program
`0.0.0.0:5000` üzerinde yerel ağı dinler ve diğer kullanıcıların açacağı
`http://192.168.x.x:5000` adresini ekranda gösterir. Sunucu penceresi açık ve
laptop uyanık kaldığı sürece aynı ağdaki kullanıcılar eş zamanlı çalışabilir.

Kurulum, güvenlik duvarı, günlük kullanım ve yedekleme adımları için
[WINDOWS_KURULUM.md](WINDOWS_KURULUM.md) dosyasına bakın.

## Git ve üretime dağıtım

Depoya yalnızca kaynak kodu, şablonlar, statik varlıklar, testler ve veritabanını
oluşturan uygulama kodu eklenir. Gerçek İPC kayıtları, `ipc.db`, Excel kaynakları,
yüklenen belgeler, fotoğraflar, videolar, yedekler, `.env` ve yerel sanal ortam
`.gitignore` ile deponun dışında tutulur.

Üretim ortamı için kök dizindeki `Procfile` Gunicorn'u tek işlem ve dört iş parçacığı
ile başlatır. SQLite kullanıldığı için aynı veritabanına yazan birden fazla uygulama
kopyası çalıştırılmamalıdır.

Dağıtımdan önce hosting panelinde `.env.example` dosyasındaki değişkenleri tanımlayın:

- `IPC_SECRET_KEY`: uzun, rastgele ve gizli oturum anahtarı.
- `IPC_INITIAL_ADMIN_PASSWORD`: boş üretim veritabanında ilk yönetici hesabının
  güçlü parolası.
- `IPC_DB_PATH`, `IPC_UPLOAD_DIR`, `IPC_BACKUP_DIR`: kalıcı disk üzerindeki yollar.

Veritabanı ve yüklenen dosyalar birbirine bağlıdır. Hosting hizmetinde kalıcı disk
bağlanmalı; örneğin veritabanı `/data/ipc.db`, dosyalar `/data/uploads`, yedekler
`/data/backups` altında saklanmalıdır. Geçici/ephemeral diskte çalıştırılırsa yeniden
dağıtım sırasında kayıtlar ve dosyalar kaybolabilir.

Gerçek veriyi Git'e koymayın. İlk dağıtım boş veritabanıyla yapılabilir; daha sonra
yönetici hesabıyla güvenli Excel aktarım ekranından kayıtları içeri alın. Mevcut
`ipc.db` ve `uploads/` taşınacaksa Git yerine şifreli ve erişimi sınırlı bir aktarım
kanalı kullanın.

## Gerçek İPC Excel verisini aktarma

Yönetici hesabıyla giriş yaptıktan sonra sol menüdeki **Excel Verisini Aktar** ekranını
kullanın:

1. `.xlsx` veya `.xlsm` kaynak dosyasını seçip **Dosyayı Kontrol Et** düğmesine basın.
2. Program bu aşamada veritabanına kayıt yazmadan başlıkları, kayıt sayılarını, toplam
   ceza tutarını, sütun eşleştirmesini ve bozuk hücreleri gösterir.
3. Aynı Sıra No veritabanında zaten varsa mevcut kaydı korumayı veya Excel verisiyle
   güncellemeyi seçin.
4. Önizlemeyi kontrol edip **Yedeği Al ve Aktar** düğmesine basın.

Aktarım başlamadan önce mevcut SQLite veritabanının bir kopyası
`backend/backups/ipc-before-import-YYYYAAGG-SSDDSS.db` adıyla oluşturulur. Kaynak Excel
dosyası hiçbir zaman değiştirilmez. Okunamayan tarih/tutar hücreleri atılmaz; ham değer
`Kaynak Dosyadaki Not / Uyarı` alanında korunur. Aynı dosyanın daha önce aktarılmış
olması SHA-256 özetiyle algılanır ve önizlemede gösterilir.

Gerçek kurum dosyası ve bu dosyaya ait kayıt/tutar sonuçları açık kaynak depoda
bulunmaz. Aktarıcı, yalnızca Sıra No ve anlamlı İPC kanıtı taşıyan satırları gerçek
kayıt kabul eder; formül veya önceden doldurulmuş şablon değerlerinden oluşan
satırları önizlemede gösterir ancak veritabanına eklemez. Kurgusal bir tanıtım
dosyası oluşturmak için `python backend/demo_workbook.py` komutu kullanılabilir.

**Formu Düzenle** ekranı gerçek dosyanın 28 A–AB konumunu aynı sırada gösterir.
Excel'de `Defter Sıra No` başlığını taşıyan B sütunu gerçekte sorumlu personeli
belirttiği için sistemde `Sorumlu Personel` adıyla gösterilir. Yeni kayıtlarda bu
değer oturum açmış kullanıcıdan otomatik alınır; kullanıcı adını forma yeniden
yazmaz ve alanı değiştiremez. Başlıksız H sütunu `Kaynak Notu / Uyarısı` olarak
korunur; R sütunundaki kalan süre sistemde güncel tarihe göre yeniden hesaplanır.
Excel'e eşlenmiş alanlar yanlışlıkla silinemez. İşlemi yapan hesap gerektiğinde
veritabanının iç denetim bilgisinde tutulur; formda Sorumlu Personel'i tekrar eden
ikinci bir personel alanı gösterilmez.

Yeni İPC formunda her **Ölçü Aleti Kalemi**, bir alet cinsi ile ona ait pozitif
sayıyı birlikte tutar. **Başka ölçü aleti ekle** düğmesiyle aynı kayda birden
fazla cins ve her cins için ayrı sayı eklenebilir. Eski tek-cinsli kayıtlar
otomatik olarak tek kaleme dönüştürülür. Excel ve rapor uyumluluğu için F sütununda
kalemlerin toplamı, G sütununda ise `Taksimetre (3); Tanker sayacı (2)` biçimindeki
eşleştirilmiş özet kullanılır.

Kalan süre, tebliğ tarihinden itibaren **30 gün** olarak hesaplanır. Ödeme, kesinleşme,
itiraz veya vergi dairesine bildirim gerçekleştiğinde sayaç kapanır.

## Ek dosyalar

Şirket / ceza kaydı ekleme ve düzenleme formundaki **Ek Dosyalar** alanından aynı
işlemde en fazla 10 belge, fotoğraf veya video yüklenebilir. Her dosya için sınır
100 MB, tek istekteki toplam yükleme sınırı 300 MB'dir. Çalıştırılabilir dosyalar,
HTML ve SVG güvenlik nedeniyle kabul edilmez.

Seçilen yeni dosyalar kaydetmeden önce adları ve boyutlarıyla formda listelenir.
Dosya penceresi tekrar açılarak veya dosyalar seçim alanına sürüklenerek mevcut
seçime yeni dosyalar eklenebilir; tek bir dosya ya da tüm seçim kaldırılabilir.

Dosyanın kendisi `backend/uploads/` altında rastgele ve güvenli bir adla, dosya
bilgileri ise SQLite veritabanında saklanır. Personelin eklediği dosyalar talep
onaylanıncaya kadar bekleyen işleme bağlıdır; onayda kayda aktarılır, ret durumunda
diskten ve veritabanından silinir. Bir kayıt silindiğinde ona bağlı dosyalar da
silinir.

Yedek alırken yalnızca `backend/ipc.db` dosyasını değil, `backend/uploads/`
klasörünü de birlikte yedekleyin. Bunlardan biri eksik olursa kayıtlarla dosyalar
arasındaki bağlantı geri yüklenemez.

Aktarım testlerini çalıştırmak için:

```bash
cd backend
python -m unittest discover -s tests -v
```

## İlk yönetici

- Yerel geliştirme ve üretim: e-posta ve parola
  `IPC_INITIAL_ADMIN_EMAIL` ve `IPC_INITIAL_ADMIN_PASSWORD` ortam
  değişkenlerinden alınır.
- Kaynak kodda veya belgelerde kullanılabilir bir varsayılan parola bulunmaz.

## İsteğe bağlı: örnek veriler
```bash
export IPC_INITIAL_ADMIN_PASSWORD="guclu-bir-tanitim-parolasi"
python backend/ornek_veri.py
```

Bu komut yalnızca açıkça kurgusal şirket ve işlem bilgileri üretir.

## Kullanılan teknolojiler
Flask, SQLite, Jinja2, Bootstrap 5.3, Bootstrap Icons, Chart.js, sistem yazı tipleri,
openpyxl (Excel), ReportLab (PDF, DejaVu ile Türkçe karakter desteği), itsdangerous (şifre sıfırlama).

## Notlar
- Ana panel, dört kısa özet değeriyle birlikte yıllara göre kayıt/tutar eğilimini ve
  süreç durumunu gösterir. Veri yoksa boş grafik çizmez; veri aktarımını anlatan tek
  bir başlangıç durumu gösterir. Tanıtım görselleri yumuşak geçişle değişir ve hareket
  durdurulabilir.
- Okuma, düzenleme ve silme işlemleri **İPC Kayıtları** çalışma alanında birleştirilmiştir.
  Kayıt listeden açılır; düzenleme ve silme işlemleri kayıt ayrıntısı üzerinden yapılır.
- **İPC Kayıtları** operasyonel arama ve kayıt yönetimi içindir. **Raporlar** ise yönetim
  özeti, tam kayıt, tahsilat ve itiraz kapsamlarında PDF/Excel çıktısı üretir.
- **Tam Kayıt Raporu** PDF'de 28 sütunu tek tabloya sıkıştırmaz; her İPC kaydını
  başlıklı bölümler halinde okunabilir A4 yatay sayfada gösterir. Boş alanlar PDF'de
  yer kaplamaz, ancak Excel çıktısı 28 sütunun tamamını korur. Daha dar rapor
  kapsamları PDF'de tablo biçimini kullanmaya devam eder.
- Excel çıktılarında uzun başlıklar için ilk satır otomatik yükseltilir; sütunlar
  içeriğe göre genişletilir ve filtreler hazır gelir. Sütunların üzerinde kurum,
  rapor adı, dönem, oluşturma tarihi, kayıt sayısı ve toplam ceza tutarını gösteren
  birleşik bir bilgi başlığı bulunur; bilgi ve sütun başlıkları kaydırma sırasında
  sabit kalır.
- Tüm doğrulama mesajları Türkçedir; form hataları ilgili alanın hemen altında gösterilir.
- Para alanları boşluklu girişi kabul eder: "2 345 234" = "2345234".
- Şirket listesinde bir filtreye "Kaldır" denildiğinde kalan filtreler otomatik uygulanır.
- Personelin şirket ekleme/düzenleme/silme işlemleri yönetici onayı bekler; profil
  güncellemesi onay gerektirmez ama yöneticilere bildirim düşer.
- Şifremi Unuttum: yerel modda sıfırlama bağlantısı ekranda ve konsolda gösterilir
  (gerçek sunucuda SMTP eklenmelidir).

## Arama ve filtreleme

Kayıt araması, iş akışındaki iki gerçek ayırt edici değer olan **Tablet Tutanak No**
ve **Ceza Muhatabı (Kişi/Firma Adı)** üzerinden yapılır. Büyük/küçük harf ve Türkçe
İ/ı ayrımı gözetilmez. Sonuçlar ayrıca yıl, hukuki dayanak ve süreç durumuna göre
süzülebilir. Aynı filtreler rapor oluşturucuya aktarılabilir.

Altyapıdaki gelişmiş tarih ve sayı filtresi aralık ifadelerini de destekler:

| Yazdığınız | Anlamı |
|---|---|
| `02.04.2026` | Tam olarak o tarih (`2.4.2026` de kabul edilir) |
| `30.10.2024-02.04.2026` | İki tarih arası (sınırlar dahil) |
| `01.01.2026-` | O tarih ve sonrası |
| `-31.12.2025` | O tarih ve öncesi |
| `2025` | Tam olarak o yıl |
| `2025-2026` | İki yıl arası |
| `16000-51000` | İki tutar arası |
| `1 000 000-3 000 000` | Boşluklu tutar aralığı da kabul edilir |

Metin sütunlarında (firma adı, tutanak no vb.) içerik araması yapılır;
büyük/küçük harf ve Türkçe İ/ı ayrımı gözetilmez. EBYS gibi içinde tire
bulunan metin alanları yanlışlıkla aralık sanılmaz.
