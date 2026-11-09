# POLITIK RIUH — Situs Peluncuran Token (Fase 1)

HTML/CSS/JS statis murni. **Tanpa dependensi**: tanpa package manager, tanpa build step, tanpa webfont, tanpa permintaan eksternal saat runtime. Hanya system font stack.

**Identitas:** POLITIK RIUH mempersembahkan **REFORMASI** — nama token REFORMASI sudah disetujui founder (issue #1, 2026-11-09); simbol yang diusulkan REFORMASI menunggu pemeriksaan kompatibilitas teknis. Seluruh salinan peserta berbahasa Indonesia (`lang="id"`).

## File

| File | Isinya |
|---|---|
| `index.html` | `/` — landing: identitas, status, token sekilas, pilar, pratinjau transparansi, pengungkapan risiko |
| `about.html` | Tujuan, posisi independen, risiko dan batasan |
| `token.html` | Gambaran token dan tabel fakta |
| `launch.html` | Status peluncuran ("Belum diluncurkan"), lima gate mainnet, dan penjelasan whitelist |
| `transparency.html` | Pengungkapan alokasi / treasury / dompet (semuanya belum tersedia) |
| `roadmap.html` | Milestone dengan label status yang didukung bukti repositori |
| `styles.css` | Sistem desain bersama (lihat di bawah) |
| `main.js` | Satu perilaku saja: toggle navigasi mobile (progressive enhancement) + Escape menutup menu yang terbuka dan mengembalikan fokus ke tombol |
| `checks.sh` | Checks lokal yang dapat direproduksi (rute, HTML, salinan, footer, JS, kontras) |
| `screenshots.sh` | Refresh screenshot dengan headless Chrome |
| `nav-toggle-test.py` | Uji fungsional toggle navigasi via Chrome DevTools Protocol (stdlib saja) |
| `cdp_helper.py` | Klien CDP stdlib bersama untuk `keyboard-test.py`, `reduced-motion-test.py`, `a11y-review.py` (`nav-toggle-test.py` lebih dulu dan menyimpan salinan inline-nya sendiri) |
| `keyboard-test.py` | Matriks keyboard-only via CDP: urutan Tab, skip link, fokus terlihat, Enter/Space, Escape + focus return, Shift+Tab — semua enam halaman, desktop + mobile |
| `reduced-motion-test.py` | Verifikasi `prefers-reduced-motion` via emulasi media CDP (kontrol vs reduce vs kembali) |
| `a11y-review.py` | Review aksesibilitas lebih luas: heading, alt text, landmark, label, fokus, + sapuan kontras terhitung per elemen; menulis `docs/accessibility-review-YYYY-MM-DD.md` |
| `evidence/` | Screenshot dari checks di bawah |

## Sistem desain

Basis nyaris-hitam `#0A0A0B`, permukaan `#121214`, border tipis `#26262A`, aksen merah secukupnya `#E5484D` (tombol utama memakai `#C93338` yang lebih gelap agar teks putih lolos WCAG AA), teks abu-abu redup `#9A9AA0`, micro-label monospace, headline editorial yang kuat, glow ambient secukupnya. HTML semantik, navigasi keyboard, fokus yang terlihat, dukungan `prefers-reduced-motion`. Responsive-first; mobile adalah layout utama.

## Setup lokal

```sh
cd apps/token-site
python3 -m http.server 8000 --bind 127.0.0.1
# buka http://127.0.0.1:8000/index.html
```

Tanpa build, tanpa install, tanpa environment variable.

## Checks yang dijalankan (2026-11-09, lokal, PR-013)

Perintah yang dapat direproduksi:

```sh
cd apps/token-site
bash checks.sh            # exit 0 = semua checks lolos
bash screenshots.sh       # exit 0 = semua screenshot ter-refresh
python3 nav-toggle-test.py  # exit 0 = toggle navigasi berfungsi
python3 keyboard-test.py    # exit 0 = matriks keyboard-only lolos (6 halaman)
python3 reduced-motion-test.py  # exit 0 = reduced-motion terbukti via emulasi CDP
python3 a11y-review.py      # exit 0 = review aksesibilitas tanpa defect keras
```

| Check | Hasil |
|---|---|
| Route smoke test (`curl`, server lokal) | **8/8 HTTP 200 + konten yang diharapkan per route**: `index/about/token/launch/transparency/roadmap.html`, `styles.css`, `main.js` — server memakai port dinamis yang dialokasikan bebas, readiness polling 15 detik, dan PID server terverifikasi memiliki listener (bukan port tetap 8000) |
| HTML parse (python `html.parser`) | **6/6 halaman, tanpa error**; `lang="id"`; tepat satu `<h1>`; urutan heading tidak melompat level; landmark `header/nav/main/footer`; tanpa ID duplikat |
| Tautan internal | Semua target `href`/`src` resolve di disk (diperiksa per halaman) |
| Disiplin salinan | Tanpa nama kandidat lama (NENGOK/GORENG/DER); tanpa sisa salinan Inggris yang menghadap peserta; identitas REFORMASI ada; status "Belum diluncurkan" ada; `launch.html` menyatakan whitelist belum dibuka |
| Regresi negatif (PR-013) | **Tidak ada**: tanpa elemen `.wallet-status` / frasa "Koneksi baca-saja direncanakan", tanpa nama personal founder di salinan publik, tanpa estimasi "0,02 SOL", tanpa klaim newsroom present-tense, Gate 01 hanya "Nama token disetujui" |
| Form / fetch / storage / dompet | **Tidak ada**: tanpa `<form>`, `fetch()`/XHR, `localStorage`, kode wallet/signing, atau pola secret di source situs |
| Sintaks JS | `node --check main.js` — lolos |
| Kontras (spot-check lima pasangan palet) | Teks redup di bg **7,07:1**; headline **18,96:1**; aksen merah di bg **5,06:1**; tombol utama putih di `#C93338` **5,23:1**; hover **5,79:1** — lima pasangan yang diuji lolos AA untuk teks normal (4,5:1); ini bukan audit semua kombinasi warna halaman |
| Uji fungsional nav toggle (headless Chrome via CDP, lebar 390px) | GitHub Actions run [#42572950950](https://github.com/nusasaputrarama-max/Politik-riuh-project/actions/runs/42572950950) pada head `4ee3cf8458ede948acd08aec9a3bdeab9ff6ca8d`: **3/3** run lulus; `INITIAL=true OPEN=true CLOSED=true`; memverifikasi state/ARIA, target URL, readiness server, dan cleanup. Tes memakai CDP `Input.dispatchMouseEvent` (mouse input), bukan DOM `.click()` dan **bukan** pengujian keyboard-only; keyboard diuji terpisah oleh `keyboard-test.py`. |
| Matriks keyboard-only (headless Chrome via CDP, input keyboard nyata) | `keyboard-test.py`, 2026-11-09 lokal, **exit 0**: urutan Tab 15–19 stop per halaman (set == elemen focusable DOM), skip link terlihat saat fokus (`top: 12px`) dan Enter memindahkan fokus ke `<main tabindex="-1">`, outline fokus 2px merah solid di semua stop, Space/Enter membuka-menutup toggle, Escape menutup + mengembalikan fokus ke toggle, Shift+Tab mundur, Enter pada tautan nav bernavigasi — semua enam halaman, desktop 1280px + mobile 390px. Log: `evidence/keyboard-2026-11-09.log`. |
| Reduced motion (emulasi media CDP) | `reduced-motion-test.py`, 2026-11-09 lokal, **exit 0**: kontrol `no-preference` (`scroll-behavior: smooth`, transisi skip-link `0.15s`) → emulasi `reduce` (`matchMedia` cocok, `scroll-behavior: auto`, transisi `0s`/`none`) → kembali ke `no-preference` (perilaku berbalik). Membuktikan media query bekerja di browser, bukan sekadar ada di CSS. Log: `evidence/reduced-motion-2026-11-09.log`. |
| Review aksesibilitas lebih luas | `docs/accessibility-review-2026-11-09.md` + `a11y-review.py`, 2026-11-09 lokal, **exit 0, tanpa defect keras**: `lang="id"` 6/6, satu `<h1>` 6/6, heading tanpa lompat level, landmark lengkap, tanpa ID duplikat, semua `aria-labelledby` resolve, tanpa elemen `<img>` (glow dekoratif adalah `<div aria-hidden>`), tanpa teks tautan samar/kosong, semua tombol bernama, skip link → `<main tabindex="-1">`. Sapuan kontras terhitung: **360 elemen teks, 0 di bawah ambang** (terendah 5,06:1 aksen merah, 5,23:1 tombol utama). **Bukan klaim konformansi WCAG** — tanpa pengujian screen reader; lihat celah terbuka di dokumen review. |
| Tautan footer repositori publik | **Dihapus dari footer keenam halaman** (2026-11-09, keputusan tim anonim; `checks.sh` kini gagal bila footer mengandung tautan repositori). Satu URL repositori tersisa di **isi** `transparency.html:82` (paragraf yang menjelaskan repositori sebagai catatan keputusan) — bukan footer, sengaja dipertahankan dan dilaporkan apa adanya; tidak dibuat URL/organisasi pengganti. |
| Screenshot (headless Chrome) | Run #42572950950 menghasilkan **12/12** capture baru: desktop 1280x3000 dan mobile 390x4500; script menghapus file lama, memeriksa exit code Chrome, ukuran file, dan dimensi PNG. Ini membuktikan capture berhasil, bukan audit visual menyeluruh. |
| Validasi PR (GitHub Actions, non-deploy) | Run [#42572950950](https://github.com/nusasaputrarama-max/Politik-riuh-project/actions/runs/42572950950) pada head `4ee3cf8458ede948acd08aec9a3bdeab9ff6ca8d` selesai **success**; semua 15 langkah workflow lulus, termasuk static checks, tiga run navigasi, keyboard matrix, reduced-motion, accessibility review, 12 screenshot, checksum, dan upload. Artifact #13654375770, 2.992.621 bytes; GitHub SHA-256 `807a432ec5242cf8a285af4224398d287b2afec339c54f83735d8d175224b285` (metadata GitHub; arsip terbaru belum diunduh ulang secara independen). Artifact sebelumnya #13651932929 pada head `870eed4` telah diverifikasi independen dengan **33/33** checksum entries PASS (PR comment `6733642680`). Ini bukti CI, bukan deployment. |
| Sidecar bukti | `evidence/SHA256SUMS.txt` — hash SHA-256 untuk 12 screenshot, 6 log run, dan 7 script checks |

### Koreksi dari screenshot dan checks PR-013

1. **Angka kontras tombol utama di README Fase 1 salah hitung.** Nilai yang tercatat (5,01:1 dan 5,55:1) tidak cocok dengan perhitungan ulang dari palet CSS; nilai yang benar adalah **5,23:1** dan **5,79:1** (keduanya tetap lolos AA). Tabel di atas memakai nilai yang sudah dikoreksi; `checks.sh` menghitung ulang rasio ini setiap kali dijalankan.
2. **Pola pemindai secret `sk-` sempat false positive** pada `risk-heading` (mengandung substring `sk-`). Pola diperketat menjadi `sk-` + 20+ karakter alfanumerik di `checks.sh`.
3. **Uji nav-toggle sempat false fail (timeout CDP) di 2026-11-09.** Penyebab: `ws_recv_msg` membuang sisa byte dalam satu segmen TCP ketika Chrome menggabungkan beberapa frame WebSocket (event + respons) — frame respons yang sudah tiba ikut terbuang, lalu recv berikutnya menunggu sampai timeout. Diperbaiki: sisa byte disimpan antar panggilan (juga untuk handshake). Uji kini lolos 3/3 run berurutan.

### Bug yang ditemukan screenshot dan diperbaiki (Fase 1)

1. **Hero terdorong ke bawah ~480px (desktop + mobile).** Penyebab: `.hero > * { position: relative; }` mengalahkan `position: absolute` milik `.glow`, sehingga glow memakan ruang flow. Diperbaiki menjadi `.hero > .wrap`.
2. **Pill status dompet meluber dari viewport di mobile.** Penyebab: `white-space: nowrap` pada pill 44 karakter. Diperbaiki: membungkus ke dua baris di bawah 720px.
3. **Kontras tombol utama gagal AA (3,75:1).** Putih di `#E5484D` di bawah 4,5:1 untuk teks normal. Diperbaiki: latar tombol digelapkan ke `#C93338` (5,23:1); hover `#BE2E33` (5,79:1).

## Disiplin fakta (mengikat)

- **Suplai ditampilkan sebagai "Diusulkan — menunggu persetujuan founder" TANPA angka.** Dua usulan yang bertentangan masih ada: `docs/token-design.md` merancang 1.000.000.000 sementara `docs/website-launch-spec.md` §10 mencatat 10.000.000.000 sebagai usulan. Konflik itu (D-05a) adalah keputusan founder yang masih terbuka; situs tidak menyelesaikannya.
- **Nama token REFORMASI sudah disetujui founder; simbol yang diusulkan REFORMASI** menunggu pemeriksaan kompatibilitas teknis — situs tidak menyatakan simbol itu kompatibel. Tidak ada alamat kontrak/mint, tanggal peluncuran, jumlah holder, volume, harga, atau metrik reward di mana pun di situs — semuanya belum ada.
- Status peluncuran adalah "Belum diluncurkan" / "Mainnet belum diluncurkan", tanpa hitung mundur. Gate mainnet 01 (nama token REFORMASI disetujui) ditandai Selesai; parameter token lainnya tetap belum diputuskan dan gate 02–05 masih Menunggu.
- **Whitelist adalah alur pendaftaran dan peninjauan GRATIS, bukan penjualan whitelist atau alokasi yang dijamin — dan pendaftaran belum dibuka.** Belum ada backend, basis data, atau deployment yang disetujui; situs statis ini tidak mengumpulkan data pendaftar.
- Tanpa counter palsu, waitlist, CTA mati, atau tautan placeholder yang disajikan sebagai fungsional.

## Target deployment (diusulkan, belum dikonfigurasi)

**GitHub Pages (diusulkan)** — keputusan D-01 masih terbuka (technical and founder decisions). Catatan feasibility lengkap ada di `docs/DEPLOYMENT_FEASIBILITY_TOKEN_SITE_2026-11-09.md`: artifact source harus tepat `apps/token-site/` (bukan root repo), opsi workflow GitHub Actions vs branch, domain kustom, HTTPS, implikasi env/keamanan, dan rollback. Situs berada di subdirektori (`apps/token-site/`), jadi Pages membutuhkan workflow yang memublikasikan direktori itu (atau branch khusus). **Belum ada yang di-deploy; tidak ada setting repo yang diubah.**

## Keterbatasan yang diketahui

- **Tanpa koneksi dompet.** Ditunda sesuai `docs/frontend-stack-decision.md` §2 (opsional di spec; menambah package wallet-adapter akan memperkenalkan dependensi untuk fitur opsional). Tidak ada elemen status dompet di header atau di halaman mana pun (dihapus PR-013; `checks.sh` menegaskan ketidakhadirannya).
- **Tanpa backend, tanpa form, tanpa analitik.** Kanal kontak / pelaporan belum dikonfigurasi (dinyatakan sebagai teks biasa di footer).
- **Fakta token yang masih menunggu keputusan founder:** pemeriksaan kompatibilitas simbol, suplai (konflik 1B vs 10B), desimal, alokasi, venue (D-04), tanggal peluncuran, domain resmi, dan tautan sosial terverifikasi.
- **Whitelist belum diimplementasikan.** Situs saat ini tanpa form, backend, basis data, dasbor applicant, atau panel admin. Jangan kumpulkan data applicant nyata sampai arsitektur di `docs/whitelist-spec.md` disetujui.
- **Dukungan reduced-motion terbukti lewat emulasi media browser** (`reduced-motion-test.py`, 2026-11-09): `prefers-reduced-motion: reduce` mengubah `scroll-behavior` menjadi `auto` dan transisi menjadi `none` di Chrome headless, lalu berbalik saat emulasi dilepas.
- **Keyboard-only terverifikasi** (`keyboard-test.py`, 2026-11-09): urutan Tab, skip link, Enter/Space, Escape + focus return, dan fokus terlihat — semua enam halaman, desktop + mobile, input keyboard nyata via CDP.
- **Tautan repositori publik dihapus dari footer** (2026-11-09, keputusan tim anonim). Satu URL tersisa di isi `transparency.html:82` (bukan footer); tidak ada URL/organisasi pengganti. `checks.sh` menegakkannya sebagai regresi.
- **Screenshot adalah render lokal** (headless Chrome 157 terhadap server lokal), bukan tangkapan situs yang sudah di-deploy.
- Screenshot mobile founder dari Elysium **tidak ada** di repo dan tidak dipakai; desain bekerja dari deskripsi tertulis atas referensi saja, dan tidak mengkloning referensi mana pun.
