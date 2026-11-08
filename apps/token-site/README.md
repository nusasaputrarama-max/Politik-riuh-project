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
| `main.js` | Satu perilaku saja: toggle navigasi mobile (progressive enhancement) |
| `checks.sh` | Checks lokal yang dapat direproduksi (rute, HTML, salinan, JS, kontras) |
| `screenshots.sh` | Refresh screenshot dengan headless Chrome |
| `nav-toggle-test.py` | Uji fungsional toggle navigasi via Chrome DevTools Protocol (stdlib saja) |
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
```

| Check | Hasil |
|---|---|
| Route smoke test (`curl`, server lokal) | **8/8 HTTP 200**: `index/about/token/launch/transparency/roadmap.html`, `styles.css`, `main.js` |
| HTML parse (python `html.parser`) | **6/6 halaman, tanpa error**; `lang="id"`; tepat satu `<h1>` per halaman; landmark `header/nav/main/footer` di setiap halaman; tanpa ID duplikat |
| Tautan internal | Semua target `href`/`src` resolve di disk (diperiksa per halaman) |
| Disiplin salinan | Tanpa nama kandidat lama (NENGOK/GORENG/DER); tanpa sisa salinan Inggris yang menghadap peserta; identitas REFORMASI ada; status "Belum diluncurkan" ada; `launch.html` menyatakan whitelist belum dibuka |
| Form / fetch / storage / dompet | **Tidak ada**: tanpa `<form>`, `fetch()`/XHR, `localStorage`, kode wallet/signing, atau pola secret di source situs |
| Sintaks JS | `node --check main.js` — lolos |
| Kontras (rasio WCAG yang dihitung) | Teks redup di bg **7,07:1**; headline **18,96:1**; aksen merah di bg **5,06:1**; tombol utama putih di `#C93338` **5,23:1**; hover **5,79:1** — semuanya lolos AA untuk teks normal (4,5:1) |
| Uji fungsional nav toggle (headless Chrome via CDP, lebar 390px) | `NAV-OPEN=true ARIA=true LABEL=Tutup menu` — lolos |
| Screenshot (headless Chrome 157) | `evidence/landing-desktop.png` (1280×2600 full page), `evidence/landing-mobile.png` (390×3800 full page), `evidence/{about,token,launch,transparency,roadmap}-desktop.png` (1280×1000 viewport) — dicek visual: landing desktop + mobile, token, launch, roadmap tampil benar |

### Koreksi dari screenshot dan checks PR-013

1. **Angka kontras tombol utama di README Fase 1 salah hitung.** Nilai yang tercatat (5,01:1 dan 5,55:1) tidak cocok dengan perhitungan ulang dari palet CSS; nilai yang benar adalah **5,23:1** dan **5,79:1** (keduanya tetap lolos AA). Tabel di atas memakai nilai yang sudah dikoreksi; `checks.sh` menghitung ulang rasio ini setiap kali dijalankan.
2. **Pola pemindai secret `sk-` sempat false positive** pada `risk-heading` (mengandung substring `sk-`). Pola diperketat menjadi `sk-` + 20+ karakter alfanumerik di `checks.sh`.

### Bug yang ditemukan screenshot dan diperbaiki (Fase 1)

1. **Hero terdorong ke bawah ~480px (desktop + mobile).** Penyebab: `.hero > * { position: relative; }` mengalahkan `position: absolute` milik `.glow`, sehingga glow memakan ruang flow. Diperbaiki menjadi `.hero > .wrap`.
2. **Pill status dompet meluber dari viewport di mobile.** Penyebab: `white-space: nowrap` pada pill 44 karakter. Diperbaiki: membungkus ke dua baris di bawah 720px.
3. **Kontras tombol utama gagal AA (3,75:1).** Putih di `#E5484D` di bawah 4,5:1 untuk teks normal. Diperbaiki: latar tombol digelapkan ke `#C93338` (5,23:1); hover `#BE2E33` (5,79:1).

## Disiplin fakta (mengikat)

- **Suplai ditampilkan sebagai "Diusulkan — menunggu persetujuan founder" TANPA angka.** Dua usulan yang bertentangan masih ada: `docs/token-design.md` merancang 1.000.000.000 sementara `docs/website-launch-spec.md` §10 mencatat 10.000.000.000 sebagai usulan. Konflik itu (D-05a) adalah keputusan founder yang masih terbuka; situs tidak menyelesaikannya.
- **Nama token REFORMASI sudah disetujui founder; simbol yang diusulkan REFORMASI** menunggu pemeriksaan kompatibilitas teknis — situs tidak menyatakan simbol itu kompatibel. Tidak ada alamat kontrak/mint, tanggal peluncuran, jumlah holder, volume, harga, atau metrik reward di mana pun di situs — semuanya belum ada.
- Status peluncuran adalah "Belum diluncurkan" / "Mainnet belum diluncurkan", tanpa hitung mundur. Gate mainnet 01 (konsep disetujui) ditandai Selesai karena nama REFORMASI disetujui; gate 02–05 masih Menunggu.
- **Whitelist adalah alur pendaftaran dan peninjauan GRATIS, bukan penjualan whitelist atau alokasi yang dijamin — dan pendaftaran belum dibuka.** Belum ada backend, basis data, atau deployment yang disetujui; situs statis ini tidak mengumpulkan data pendaftar.
- Tanpa counter palsu, waitlist, CTA mati, atau tautan placeholder yang disajikan sebagai fungsional.

## Target deployment (diusulkan, belum dikonfigurasi)

**GitHub Pages (diusulkan)** — keputusan D-01 masih terbuka (ChatGPT/Rama). Catatan feasibility lengkap ada di `docs/DEPLOYMENT_FEASIBILITY_TOKEN_SITE_2026-11-09.md`: artifact source harus tepat `apps/token-site/` (bukan root repo), opsi workflow GitHub Actions vs branch, domain kustom, HTTPS, implikasi env/keamanan, dan rollback. Situs berada di subdirektori (`apps/token-site/`), jadi Pages membutuhkan workflow yang memublikasikan direktori itu (atau branch khusus). **Belum ada yang di-deploy; tidak ada setting repo yang diubah.**

## Keterbatasan yang diketahui

- **Tanpa koneksi dompet.** Ditunda sesuai `docs/frontend-stack-decision.md` §2 (opsional di spec; menambah package wallet-adapter akan memperkenalkan dependensi untuk fitur opsional). Header hanya menampilkan status sebagai teks.
- **Tanpa backend, tanpa form, tanpa analitik.** Kanal kontak / pelaporan belum dikonfigurasi (dinyatakan sebagai teks biasa di footer).
- **Fakta token yang masih menunggu keputusan founder:** pemeriksaan kompatibilitas simbol, suplai (konflik 1B vs 10B), desimal, alokasi, venue (D-04), tanggal peluncuran, domain resmi, dan tautan sosial terverifikasi.
- **Whitelist belum diimplementasikan.** Situs saat ini tanpa form, backend, basis data, dasbor applicant, atau panel admin. Jangan kumpulkan data applicant nyata sampai arsitektur di `docs/whitelist-spec.md` disetujui.
- **Dukungan reduced-motion diverifikasi lewat inspeksi kode** (media query `prefers-reduced-motion` ada dan menonaktifkan transisi); belum diuji terhadap pengaturan reduced-motion di level OS yang live.
- **Screenshot adalah render lokal** (headless Chrome 157 terhadap server lokal), bukan tangkapan situs yang sudah di-deploy.
- Screenshot mobile founder dari Elysium **tidak ada** di repo dan tidak dipakai; desain bekerja dari deskripsi tertulis atas referensi saja, dan tidak mengkloning referensi mana pun.
