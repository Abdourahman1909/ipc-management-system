# Windows Sunucu Laptopu — Kolay Kurulum

Bu paket, bölümdeki kullanıcıların Python veya programlama araçları kurmadan İPC Yönetim Sistemi'ni kullanabilmesi içindir.

## Çalışma şekli

- Bir Windows laptop **sunucu laptopu** olarak çalışır.
- Program yalnızca bu laptopta açılır ve açık tutulur.
- Aynı kurum ağına bağlı diğer laptoplar Chrome, Edge veya Firefox ile bağlanır.
- Diğer laptoplara program, Python veya veritabanı kurulmaz.
- Bu kurulum yalnızca güvenilir özel/kurum ağı içindir; doğrudan internete açılmamalıdır.

## İlk kurulum

1. `IPC_Yonetim_Sistemi_Windows.zip` dosyasını sunucu laptopta **Belgeler** klasörüne çıkarın.
2. Çıkan klasörü daha sonra taşımayın. Veriler programın yanındaki `data` klasöründe saklanır.
3. `Windows_Guvenlik_Duvari_Ac.bat` dosyasına çift tıklayın.
4. Windows yönetici izni sorarsa **Evet** seçin. Bu işlem yalnızca özel ağlarda TCP 5000 bağlantısına izin verir.
5. `IPC_Yonetim_Sistemi.exe` dosyasına çift tıklayın.
6. İlk çalıştırmada güçlü bir yönetici parolası girin ve güvenli bir yerde saklayın.
7. Windows Güvenlik Duvarı ayrıca izin sorarsa yalnızca **Özel ağlar** seçeneğine izin verin.

Python kurulmasına gerek yoktur. Gerekli Python çalışma ortamı ve kütüphaneler `.exe` dosyasının içindedir.

Bu proje için ticari bir Windows kod-imzalama sertifikası kullanılmıyorsa Windows
SmartScreen imzasız uygulama uyarısı gösterebilir. Paket yalnızca sorumlu proje
deposundan veya kurumun bilgi işlem biriminden alınmalıdır. Kurumun politikası
gerektiriyorsa `.exe` bilgi işlem birimi tarafından taranmalı ve dijital olarak
imzalanmalıdır.

## Her gün çalıştırma

1. Sunucu laptop aynı kurum ağına bağlanır.
2. `IPC_Yonetim_Sistemi.exe` açılır.
3. Siyah sunucu penceresinde iki adres görünür:

```text
Sunucu laptopu: http://127.0.0.1:5000
Diğer laptoplar: http://192.168.x.x:5000
```

4. Sunucu laptop kendi tarayıcısını otomatik açar.
5. Diğer kullanıcılar, ekranda yazan `http://192.168.x.x:5000` adresini tarayıcılarına yazar.
6. Sunucu penceresi çalışma boyunca açık kalır.

Programı kapatmak için siyah pencerede `Ctrl+C` tuşlarına basın. Pencere kapandığında diğer laptopların bağlantısı da kesilir.

## Aynı anda kullanım

Birden fazla personel aynı anda sistemi görüntüleyebilir ve kullanabilir. Sunucu, istekleri birden fazla iş parçacığıyla karşılar. SQLite yazma işlemlerini sıraya koyar ve kısa süreli çakışmalarda 30 saniyeye kadar bekler.

Bu küçük ofis kullanımı için uygundur. Aynı `data` klasörünü kullanan ikinci bir `.exe` kopyası açmayın ve aynı veritabanını iki farklı sunucu laptop üzerinden çalıştırmayın.

## Sunucu laptop ayarları

- Laptop prize takılı olmalıdır.
- Windows güç ayarlarında, prize takılıyken uyku modu kapatılmalıdır.
- Ağ profili **Özel ağ** olarak ayarlanmalıdır.
- Mümkünse kurumun bilgi işlem birimi sunucu laptopa sabit IP veya DHCP rezervasyonu vermelidir.
- IP değişirse programı yeniden açın ve ekranda gösterilen yeni adresi kullanın.

## Veriler nerede?

Programın yanında otomatik oluşan `data` klasörü şunları içerir:

```text
data/
  ipc.db       # Resmî kayıtlar ve kullanıcı hesapları
  uploads/     # Ek dosyalar
  backups/     # Excel aktarımı öncesi SQLite yedekleri
```

`.ipc-secret` dosyası da `data` klasöründedir ve oturum güvenliği için gereklidir. Silinmemelidir.

## Manuel yedek

1. Programı `Ctrl+C` ile kapatın.
2. `data` klasörünün tamamını tarih ekleyerek güvenli bir diske kopyalayın.
3. Yedekte `ipc.db`, `uploads`, `backups` ve `.ipc-secret` birlikte bulunmalıdır.

Yalnızca `ipc.db` dosyasını kopyalamak ek dosyaların eksik kalmasına neden olur.

## Bağlantı olmazsa

1. Sunucu programının açık olduğunu kontrol edin.
2. Her iki laptopun aynı Wi-Fi/Ethernet kurum ağına bağlı olduğunu kontrol edin.
3. Diğer laptopta siyah pencerede gösterilen IP adresini aynen yazın.
4. Sunucu laptopta ağ profilinin **Özel** olduğunu kontrol edin.
5. `Windows_Guvenlik_Duvari_Ac.bat` dosyasını tekrar çalıştırın.
6. Kurum ağında cihazlar arası bağlantı engelleniyorsa bilgi işlem biriminden TCP 5000 için yerel ağ izni isteyin.

## Güvenlik

- Sistemi modem üzerinden internete yönlendirmeyin.
- Yönetici parolasını paylaşmayın.
- Her personele ayrı kullanıcı hesabı açın.
- Sunucu laptop ve `data` yedekleri yetkisiz kişilerin erişemeyeceği yerde tutulmalıdır.
- Windows ve tarayıcı güncellemelerini düzenli uygulayın.
