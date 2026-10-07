# termtoys 🖥️✨

**EN | 6 tiny terminal toys in one Python file — Matrix rain, fire, starfield, Game of Life, marquee, DVD bounce.**
**TR | Tek Python dosyasında 6 minik terminal oyuncağı — Matrix yağmuru, ateş, yıldız alanı, Yaşam Oyunu, kayan yazı, DVD sekmesi.**

Zero dependencies. Zero installs beyond Python itself. Just vibes / kurulum derdi yok, sadece keyif:

```bash
python termtoys.py            # menu / menü
python termtoys.py matrix     # Matrix rain / Matrix yağmuru
python termtoys.py fire       # cozy fire / ateş
python termtoys.py life       # Conway's Game of Life
python termtoys.py marquee --text "IYI KI DOGDUN AHMET"   # custom banner / özel yazı
python termtoys.py dvd        # bouncing logo / seken logo
```

Ctrl+C exits cleanly / Ctrl+C ile temiz çıkış.

---

## 🇬🇧 English

### Why?

Every dev secretly loves `cmatrix`. But installing a screensaver package for
one effect is overkill — and half of them don't run on Windows anyway.
**termtoys** is one Python file with six classic terminal animations that run
anywhere Python runs: Windows 10/11, macOS, Linux. ANSI colors are enabled
automatically on Windows.

### Toys

| Command | What you get |
|---|---|
| `matrix` | Falling green code rain with bright white heads |
| `fire` | Classic bottom-fed fire with a heat palette |
| `star` | Flying starfield (fly *through* the stars) |
| `life` | Conway's Game of Life, auto-reseeds, population counter |
| `marquee` | Rainbow scrolling banner — `--text` to customize |
| `dvd` | The legendary bouncing DVD logo (color changes on bounce) |

### Install

```bash
curl -LO https://raw.githubusercontent.com/Volvox6767/termtoys/main/termtoys.py
```

Python 3.8+ only. No pip, no deps, works offline.

### FAQ

**Does it work on the old cmd.exe?** On Windows 10/11, yes — ANSI mode is enabled via the Windows API automatically. On very old systems try Windows Terminal.

**Can I resize the window?** Yes — every frame re-reads the terminal size.

**Custom text?** `python termtoys.py marquee --text "HAPPY BIRTHDAY"` or the same flag on `dvd`.

---

## 🇹🇷 Türkçe

### Neden?

Her geliştirici `cmatrix`'ü sever. Ama tek efekt için ekran koruyucu paketi
kurmak gereksizdir — üstelik yarısı Windows'ta zaten çalışmaz. **termtoys**
tek Python dosyasında, Python'un çalıştığı her yerde koşan altı klasik
terminal animasyonudur: Windows 10/11, macOS, Linux. ANSI renkleri Windows'ta
otomatik açılır.

### Oyuncaklar

| Komut | Ne verir? |
|---|---|
| `matrix` | Beyaz kafalı, aşağı akan yeşil kod yağmuru |
| `fire` | Klasik alttan beslenen, isi paletli ateş |
| `star` | Uçan yıldız alanı (yıldızların *içinden* uçarsın) |
| `life` | Conway'in Yaşam Oyunu — otomatik yeniden doğar, nüfus sayacı var |
| `marquee` | Gökkuşağı kayan yazı — `--text` ile özelleştir |
| `dvd` | Efsanevi seken DVD logosu (her sekmede renk değiştirir) |

### Kurulum

```bash
curl -LO https://raw.githubusercontent.com/Volvox6767/termtoys/main/termtoys.py
```

Sadece Python 3.8+. pip yok, bağımlılık yok, çevrimdışı çalışır.

### SSS

**Eski cmd.exe'de çalışır mı?** Windows 10/11'de evet — ANSI modu Windows API
ile otomatik açılır. Çok eski sistemlerde Windows Terminal deneyin.

**Pencereyi yeniden boyutlandırabilir miyim?** Evet — her kare terminal
boyutunu yeniden okur.

**Özel yazı?** `python termtoys.py marquee --text "IYI KI DOGDUN"` — dvd için de aynı bayrak.

---

Made with ❤ by **Ahmet Gedik** — [instagram.com/ahmetgedik67](https://www.instagram.com/ahmetgedik67)
Follow on Instagram for more free everyday tools.
Daha fazla ücretsiz günlük araç için Instagram'da takip edin.

License / Lisans: [MIT](LICENSE)
