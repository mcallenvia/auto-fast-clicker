# FastClicker

![Version](https://img.shields.io/badge/version-1.2-22dd77?style=for-the-badge)
![Language](https://img.shields.io/badge/python-3.8%2B-4a9eff?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-blue?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)

FastClicker, sol ve sağ fare tuşu için bağımsız iki makro motoru barındıran, Python ile geliştirilmiş bir auto-clicker uygulamasıdır. Uygulama tkinter tabanlı bir arayüze, pyautogui tıklama motoruna ve keyboard modülü üzerinden çalışan kısayol sistemine sahiptir.

İlk sürümde tek makro ve temel kontroller yer alıyordu. v1.1 ile çift makro altyapısı ve güvenlik katmanları eklendi. v1.2, arayüzü sekme tabanlı bir yapıya taşıdı ve Humanized Jitter, Burst Modu, Macro Scheduling, Pasif Mod ve CPU Optimizasyonu gibi gelişmiş özellikleri sisteme entegre etti.

---

## İçindekiler

- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Arayüz](#arayüz)
- [Kullanım](#kullanım)
- [Özellikler](#özellikler)
- [Teknik Altyapı](#teknik-altyapı)
- [Changelog](#changelog)

---

## Gereksinimler

```
python >= 3.8
pyautogui
keyboard
```

`keyboard` modülü, Windows'ta global kısayol dinleyebilmek için yönetici yetkisi gerektirir. Yetki olmadan çalıştırıldığında uygulama otomatik olarak manuel kısayol girişine geçer; işlevsellik kaybolmaz.

---

## Kurulum

Releases bölümünden `.py` dosyasını indirin.

```
pip install pyautogui keyboard
python FastClicker_v1.2.py
```

Açılışta 2–3 saniyelik kısa bir bekleme yaşanabilir. Bu, keyboard ve pyautogui modüllerinin yüklenmesinden kaynaklanır ve normaldir.

---

## Arayüz

Uygulama üç sekmeden oluşur.

**Ana Sayfa**

Her iki makronun anlık CPS değeri, çalışma durumu, atanmış kısayollar, toplam tıklama ve pasif mod bilgisi tek ekranda görüntülenir. Makro sayfalarına geçmeden önce genel durumu buradan takip edebilirsiniz.

**Sol Tık Makrosu**

Sol fare tuşuna ait tüm ayarlar bu sayfada yönetilir. Kısayol ataması, hız kontrolü, mod seçimi ve gelişmiş özellikler burada yer alır.

**Sağ Tık Makrosu**

Sol tık sayfasıyla birebir aynı yapıda, tamamen bağımsız bir sayfa. İki makronun kısayolları, ayarları ve çalışma durumları birbirini hiçbir şekilde etkilemez.

---

## Kullanım

1. Sol Tık veya Sağ Tık sekmesine geçin.
2. "Kısayol Ata" butonuna tıklayın ve klavyeden bir tuşa basın. Fare düğmeleri kısayol olarak kabul edilmez, sistem bu girişi otomatik olarak reddeder.
3. Hedef CPS değerini slider veya hazır değer butonlarından (5, 10, 20, 50, 100) ayarlayın.
4. Çalışma modunu seçin: Toggle her basışta makroyu açıp kapatır, Hold ise tuş basılı tutulduğu sürece çalışır.
5. Tık türünü seçin: Tek veya Çift.
6. BAŞLAT butonuna ya da atadığınız kısayola basın.
7. Makroyu geçici devre dışı bırakmak için Pasif Mod'u açın. Kısayol ataması ve tüm ayarlar korunur.

---

## Özellikler

### Çift Makro Sistemi

Sol ve sağ tık için bağımsız iki motor çalışır. Her motorun kendi kısayolu, CPS değeri, modu, gelişmiş ayarları ve istatistikleri vardır. Motorlar birbirinden tamamen yalıtılmış keyboard hook'ları kullanır. Bir makronun kısayolunu değiştirmek veya sıfırlamak diğer makroyu etkilemez. İki makro aynı anda eş zamanlı çalışabilir.

### Humanized Jitter

Her tıklama öncesinde fare imleci piksel cinsinden ayarlanmış bir yarıçap içinde rastgele kayar, tıklama gerçekleştikten sonra orijinal konumuna geri döner. Yarıçap 1 ile 30 piksel arasında ayarlanabilir. Tekdüze tıklama koordinatlarından kaçınmak için kullanılır.

### Burst Modu

Makro, belirlenen sayıda tıklamayı hedef CPS'de gerçekleştirir, ardından belirtilen süre kadar bekler ve döngüyü yeniden başlatır. Hem tıklama sayısı hem bekleme süresi bağımsız olarak ayarlanır. Aktif burst sırasında makro sayfasında blok tipi bir ilerleme çubuğu gösterilir.

### Macro Scheduling

Makro, kısayol tuşuna basıldıktan belirli saniye sonra devreye girebilir. Ek olarak, çalışmaya başladıktan belirli saniye sonra otomatik olarak durabilir. Her iki değer de saniye cinsinden girilir; sıfır değeri sınırsız anlamına gelir. İki ayar birlikte kullanılabilir.

### Pasif Mod

Her makro sayfasının üst kısmında yer alır. Pasif Mod açıkken makro tamamen bloklanır; kısayol tuşuna basılsa, START butonuna tıklansa veya Hold modu aktif olsa bile hiçbir tıklama gerçekleşmez. Kapatmak için toggle'a bir kez daha tıklamak yeterlidir. Kısayol ataması ve tüm ayarlar korunur.

### CPU Optimizasyonu

Standart `time.sleep()` yerine `time.perf_counter()` tabanlı adaptif bekleme kullanılır. Belirlenen interval süresi yaklaştığında sistem spin-wait moduna geçer. Bu yöntem, özellikle 50 CPS'in üzerinde belirgin şekilde daha hassas zamanlama sağlar. Yavaş makinelerde adaptif bekleme devre dışı bırakılabilir.

### Fare Düğmesi Koruması

Fare düğmeleri hiçbir koşulda kısayol olarak atanamaz ve makroyu tetikleyemez. Bu kısıtlama hem kısayol kayıt ekranında hem de motor içinde ayrı ayrı uygulanır.

### Debounce (350ms)

Kısayol tuşuna hızlı art arda basıldığında makro istem dışı açılıp kapanmaz. İki toggle işlemi arasında geçmesi gereken minimum süre 350 milisaniyedir.

---

## Teknik Altyapı

Her makro motoru üç bağımsız daemon thread üzerinde çalışır: tıklama döngüsü, CPS monitörü ve zamanlayıcı. Bu yapı sayesinde hiçbir işlem UI thread'ini bloklamaz.

Keyboard hook'ları `keyboard.on_press_key()` ile her motor için ayrı ayrı tutulur. Kısayol değiştirildiğinde yalnızca o motora ait hook `keyboard.unhook()` ile temizlenir. Geçici kayıt hook'u ise atama tamamlanır tamamlanmaz serbest bırakılır.

UI güncellemeleri thread içinden doğrudan değil, `after(0, callback)` aracılığıyla UI thread'ine devredilerek yapılır. Bu, tkinter'ın thread-safe olmayan yapısından kaynaklanan olası çökmeleri önler.

---

## Changelog

### v1.2

- Sekme tabanlı arayüz eklendi. Ana Sayfa, Sol Tık ve Sağ Tık olmak üzere üç bölüm. Tüm içerik tek sayfada görünür, kaydırma gerekmez.
- Pasif Mod eklendi. Her makro sayfasının üst kısmında bağımsız toggle. Aktifken tüm tetikleyiciler motor düzeyinde engellenir.
- Ana Sayfa eklendi. Her iki makronun anlık CPS, kısayol, durum ve pasif mod bilgisi tek ekranda izlenebilir.
- Humanized Jitter eklendi. Piksel cinsinden ayarlanabilir yarıçapla her tıklamada rastgele fare kayması.
- Burst Modu eklendi. Tıklama sayısı ve bekleme süresi ayarlanabilir döngü; canlı ilerleme çubuğu.
- Macro Scheduling eklendi. Başlama gecikmesi ve otomatik durdurma süresi saniye cinsinden ayarlanabilir.
- CPU Optimizasyonu eklendi. perf_counter tabanlı adaptif bekleme; yüksek CPS değerlerinde hassas zamanlama.
- TR / EN dil desteği eklendi. Başlık çubuğundaki butonla anlık geçiş.
- Bağımsız keyboard hook sistemi uygulandı. Her motor kendi hook referansını tutar.
- Varsayılan kısayol NOT SET olarak değiştirildi.
- Pencere boyutu 680x820 olarak güncellendi.

### v1.1

- Sol ve sağ tık için bağımsız çift makro sistemi eklendi.
- Fare düğmesi koruması eklendi.
- 350ms debounce koruması eklendi.
- Aktif makro varken çıkışta kullanıcıya onay sorulur.
- Başlık alanına sürüm bilgisi eklendi.

### v1.0

- İlk sürüm.
- Tek makro, kısayol atama, CPS slider.
- Toggle ve Hold çalışma modları, tek ve çift tıklama seçeneği.
- Gerçek zamanlı CPS monitörü, oturum sayacı, zamanlayıcı.
- Koyu tema arayüz, Canvas tabanlı yuvarlak butonlar.
- pyautogui ve keyboard entegrasyonu; her ikisi de opsiyonel.

---

*Developed by McAllen — 2026*
