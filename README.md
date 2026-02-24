# ⚡ FastClicker

<div align="center">

![Version](https://img.shields.io/badge/version-1.2-22dd77?style=for-the-badge)
![Language](https://img.shields.io/badge/python-3.8%2B-4a9eff?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-blue?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)

**Gelişmiş, ikili makro sistemi ile donatılmış modern bir auto-clicker uygulaması.**  
*An advanced auto-clicker with dual independent macro system.*

[📥 İndir / Download](#-kurulum--installation) · [🆕 Changelog](#-changelog) · [📖 Kullanım / Usage](#-kullanım--usage)

</div>

---

## 🇹🇷 Türkçe

FastClicker, klasik sürümün yapısını koruyarak tamamen yenilenmiş, modern bir görünüme kavuşturulmuş ve çok daha kullanışlı hâle getirilmiş bir versiyondur. Arayüz baştan sona düzenlendi, koyu tema benimsendi ve uygulama artık tamamen responsive yapıda çalışıyor. Pencere boyutu değiştikçe metinlerin, butonların ve genel görünümün otomatik olarak ölçeklenmesi sayesinde her çözünürlükte tutarlı bir deneyim sunuyor.

Uygulamada düzen; kullanım alışkanlıklarını bozmayacak şekilde, ancak çok daha anlaşılır bir formda yeniden tasarlandı. Artık uygulama **3 sayfalı sekme** yapısıyla çalışıyor:

- **Ana Sayfa:** Her iki makronun canlı CPS değeri, durum (aktif/bekliyor/pasif), atanan kısayollar ve toplam tıklama sayısı tek ekranda izlenebilir.
- **Sol Tık Makrosu:** Sol fare tuşuna ait tüm ayarlar buradan yönetilir.
- **Sağ Tık Makrosu:** Sağ fare tuşu için tamamen bağımsız, ayrı bir ayar sayfası.

Hotkey sistemi `keyboard` modülünü temel alıyor. Eğer bu modül kullanıcı cihazında yoksa uygulama otomatik olarak manuel hotkey girişine yönlendiriyor. Tıklama işlemleri `pyautogui` üzerinden gerçekleştiriliyor. Uygulamayı donmadan çalıştırabilmek için tıklama mekanizması, CPS hesaplaması ve zamanlayıcı birbirinden ayrı thread'ler üzerinde yönetiliyor.

> Açılış sırasında nadiren 2–3 saniyelik kısa bir bekleme yaşanabilir; bu tamamen normal bir yükleme sürecidir.

---

## 🇬🇧 English

FastClicker is a fully redesigned, modernized version of the classic auto-clicker. The interface has been rebuilt from scratch with a dark theme, responsive layout, and font scaling across all resolutions. The app now uses a **3-tab structure** for clear navigation between the dashboard and each macro's settings.

Hotkeys are handled via the `keyboard` module with automatic fallback to manual input. Clicking is performed through `pyautogui`. All operations (clicking, CPS monitoring, timer) run on independent daemon threads to keep the UI responsive at all times.

> A brief 2–3 second startup delay is normal and expected.

---

## ✨ Özellikler / Features

| Özellik / Feature | Açıklama / Description |
|---|---|
| 🖱️ **Dual Macro System** | Sol ve sağ tık için tamamen bağımsız makrolar / Independent left & right click macros |
| 🔥 **Humanized Jitter** | Her tıklamada rastgele fare kayması / Random micro mouse offsets per click |
| 🔥 **CPU Optimization** | `perf_counter` tabanlı hassas zamanlama / High-res timer with adaptive sleep |
| 🔥 **Burst Mode** | N tık → bekle → tekrar / N clicks → pause → repeat |
| 🔥 **Macro Scheduling** | Gecikmeli başlatma ve otomatik durdurma / Delayed start & auto-stop |
| 🔴 **Passive Mode** | Hotkey'i bozmadan makroyu anında devre dışı bırakma / Disable macro without unhooking |
| 🔒 **Mouse Safety** | Fare düğmeleri makro tetikleyemez / Mouse buttons cannot trigger macros |
| 🔒 **Debounce 350ms** | Çift tetiklenmeyi engeller / Prevents accidental double-fire |
| 🌐 **TR / EN** | Tam çift dil desteği / Full bilingual support |
| 📊 **Live Dashboard** | Anlık CPS, oturum ve toplam istatistikleri / Real-time CPS, session & total stats |

---

## 🆕 Changelog

### v1.2 — *Güncel / Current*

**Yeni / New:**
- 🌐 **TR / EN dil desteği** — Başlık barındaki butonla anlık dil değişimi
- 🔴 **Pasif Mod** — Her makro sayfasının üstünde ayrı pasif mod toggle'ı; aktifken hotkey'e basılsa bile tıklama gerçekleşmez
- 📊 **Ana Sayfa (Dashboard)** — İki makronun canlı istatistiklerini tek ekranda gösterir; pasif mod durumu da burada yansır
- 🖱️ **Bağımsız hotkey hook sistemi** — Her motor kendi `keyboard.on_press_key` hook'unu tutar; kısayol atama veya değiştirme diğer makroyu devre dışı bırakmaz
- 🔥 **Humanized Jitter** — Tıklama başına ayarlanabilir piksel aralığında rastgele fare kayması
- 🔥 **CPU Optimization** — `time.perf_counter` + adaptive spin-wait ile alt-milisaniye hassasiyeti
- 🔥 **Burst Mode** — N tık ardından P saniye bekleme döngüsü; aktif burst ilerleme barı
- 🔥 **Macro Scheduling** — Gecikmeli başlatma (saniye) + süreli otomatik durdurma

**İyileştirmeler / Improvements:**
- Sekme tabanlı (Tab) arayüz — her şey tek sayfada görünür, scroll gerekmez
- Her makro sayfasında büyük anlık CPS gösterimi (44pt)
- Varsayılan kısayol artık `NOT SET` — iki makro başlangıçta birbirini etkilemez
- Pencere boyutu `680×820`'ye büyütüldü, minimum `600×700`
- Fare butonu koruması hotkey kayıt ekranında da aktif

---

### v1.1

**Yeni / New:**
- 🖱️ **Dual Macro System** — Sol tık (R tuşu) ve sağ tık (F tuşu) için ayrı, bağımsız makrolar
- 🔒 **Mouse Safety** — Fare düğmeleri hiçbir şekilde makroyu tetikleyemez
- 🔒 **Debounce 350ms** — Yanlışlıkla çift tetiklenmeyi önler
- Sağ üstte yeşil `v1.1` rozeti

**İyileştirmeler / Improvements:**
- Thread-safe durum güncellemeleri (`after(0, ...)` ile UI'ya güvenli geri dönüş)
- Kapatma koruması — aktif makro varken çıkışta onay istenir

---

### v1.0 — *İlk Sürüm / Initial Release*

- Tek makro (sol tık), hotkey atama, CPS slider (1–100)
- Toggle / Hold mod, Tek / Çift tıklama
- Gerçek zamanlı CPS monitörü, oturum sayacı, timer
- Responsive dark UI, `FancyButton` (Canvas tabanlı yuvarlak butonlar)
- `pyautogui` + `keyboard` entegrasyonu, her ikisi de opsiyonel

---

## 📋 Gereksinimler / Requirements

```
python >= 3.8
pyautogui
keyboard
```

```bash
pip install pyautogui keyboard
```

> `keyboard` modülü Windows'ta administrator (yönetici) izni gerektirebilir.

---

## 📥 Kurulum / Installation

1. Sağ taraftaki **Releases** bölümünden `.py` dosyasını indirin.
2. Bağımlılıkları yükleyin:
   ```bash
   pip install pyautogui keyboard
   ```
3. Çalıştırın:
   ```bash
   python FastClicker_v1.2.py
   ```

---

## 📖 Kullanım / Usage

### TR
1. **Sol Tık** veya **Sağ Tık** sekmesine geçin.
2. **Kısayol Ata** butonuna tıklayın ve klavyeden bir tuşa basın (fare tuşları kabul edilmez).
3. **Hedef CPS** slider'ından veya preset butonlarından hız seçin.
4. **Mod** ve **Tık Türü** ayarlayın.
5. **BAŞLAT** butonuna tıklayın ya da atadığınız kısayola basın.
6. Makroyu devre dışı bırakmak için **Pasif Mod**'u aktif edin — kısayol atama bozulmaz.

### EN
1. Switch to the **Left Click** or **Right Click** tab.
2. Click **Set Hotkey** and press any keyboard key (mouse buttons are rejected).
3. Set speed via the **Target CPS** slider or preset chips.
4. Choose **Mode** (Toggle/Hold) and **Click Type** (Single/Double).
5. Click **START** or press your assigned hotkey.
6. Use **Passive Mode** to instantly disable a macro without losing its hotkey assignment.

---

## 🛡️ Güvenlik Notları / Safety Notes

- **Fare düğmeleri** hiçbir zaman makroyu tetikleyemez; bu hardcoded bir korumadır.
- **350ms debounce** sayesinde kısayola hızlı art arda basılsa bile makro yanlışlıkla açılıp kapanmaz.
- **Pasif Mod** aktifken motor tamamen kilitlenir — hotkey, START butonu ve loop içi kontrol hepsinde çalışır.
- Her iki makronun kısayolları tamamen bağımsız hook'larla yönetilir; birini değiştirmek diğerini etkilemez.

---

## 👨‍💻 Geliştirici / Developer

**McAllen** — 2025

---

<div align="center">
<sub>FastClicker v1.2 · Python · tkinter · pyautogui · keyboard</sub>
</div>
